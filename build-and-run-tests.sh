#!/bin/bash

set -e
export BUILD_TAG="latest"

PASSED_UNIT_TESTS=()
FAILED_UNIT_TESTS=()
PASSED_COMPONENT_TESTS=()
FAILED_COMPONENT_TESTS=()

run_unit_test_module() {
  local module_path="$1"

  echo
  echo "===================================="
  echo " Running '$module_path' tests"
  echo "===================================="

  if (
    cd "$module_path" && \
    pipenv install --dev --deploy --ignore-pipfile && \
    pipenv run unittests-cov && \
    pipenv run coverage-report
  ); then
    echo "[🟢 ]: '$module_path' tests PASSED."
    PASSED_UNIT_TESTS+=("$module_path")
  else
    echo "[🔴 ]: '$module_path' tests FAILED."
    FAILED_UNIT_TESTS+=("$module_path")
  fi
}

build_component_test_docker() {
  echo
  echo "[🟠 ]: Starting building component tests docker image..."
  docker build \
    -t local/mhs-componenttest:${BUILD_TAG} \
    -f ./component-test.Dockerfile \
    .
  echo
  echo "[🟢 ]: Completed building component tests docker image"
}

setup_fake_spine_environment_variables() {
  echo
  echo "[🟠 ]: Starting setup environment variables for fake spine..."
      cd ./integration-tests || exit 1
      chmod +x setup_component_test_env.sh
      ./setup_component_test_env.sh
      source component-test-source.sh
      rm component-test-source.sh
      cd ..
  echo
  echo "[🟢 ]: Completed setup environment variables for fake spine"
}

build_component_test_dependencies() {
  echo
  echo "[🟠 ]: Starting building 'mhs-outbound' docker image..."
  docker build \
    -t local/mhs-outbound:${BUILD_TAG} \
    -f docker/outbound/Dockerfile \
    .
  echo
  echo "[🟢 ]: Completed building 'mhs-outbound' docker image"

  echo
  echo "[🟠 ]: Starting building 'mhs-inbound' docker image..."
   docker build \
      -t local/mhs-inbound:${BUILD_TAG} \
      -f docker/inbound/Dockerfile \
      .
  echo
  echo "[🟢 ]: Completed building 'mhs-inbound' docker image"

  echo
  echo "[🟠 ]: Started building 'mhs-route' docker image..."
  docker build \
    -t local/mhs-route:${BUILD_TAG} \
    -f docker/spineroutelookup/Dockerfile \
    .
  echo
  echo "[🟢 ]: Completed building 'mhs-route' docker image"

  echo
  echo "[🟠 ]: Started building 'fake-spine' docker image..."
  docker build \
  -t local/fake-spine:${BUILD_TAG} \
  -f integration-tests/fake_spine/Dockerfile \
  .
  echo
  echo "[🟢 ]: Completed building 'fake-spine' docker image"
}

run_spine_route_lookup_docker() {
  echo
  echo "[🟠 ]: Started running docker images for component tests..."
  docker compose \
    -f docker-compose.yml \
    -f docker-compose.component.override.yml \
    build
  docker compose \
    -f docker-compose.yml \
    -f docker-compose.component.override.yml \
    -p ${BUILD_TAG} \
    up -d
  echo
  echo "[🟢 ]: Completed running docker images for component tests"
}

run_sds_component_docker() {
  echo
  echo "[🟠 ]: Started running docker images for component tests..."
  docker-compose \
    -f docker-compose.yml \
    -f docker-compose.component.override.yml \
    -f docker-compose.component-sds.override.yml \
    build
  docker-compose \
    -f docker-compose.yml \
    -f docker-compose.component.override.yml \
    -f docker-compose.component-sds.override.yml \
    -p ${BUILD_TAG} \
    up -d
  echo
   echo "[🟢 ]: Completed running docker images for component tests"
}

run_component_tests() {
  local component_name="$1"
  echo
  echo "==============================================="
  echo " Running '$component_name' component tests"
  echo "==============================================="

   if (
    docker run --network "${BUILD_TAG}_default" \
      --env "MHS_ADDRESS=http://outbound" \
      --env "AWS_ACCESS_KEY_ID=test" \
      --env "AWS_SECRET_ACCESS_KEY=test" \
      --env "MHS_DB_ENDPOINT_URL=http://dynamodb:8000" \
      --env "FAKE_SPINE_ADDRESS=http://fakespine" \
      --env "MHS_INBOUND_QUEUE_BROKERS=amqp://rabbitmq:5672" \
      --env "MHS_INBOUND_QUEUE_NAME=inbound" \
      --env "SCR_ADDRESS=http://scradaptor" \
      --name "component-tests" \
      local/mhs-componenttest:$BUILD_TAG
  ); then
    echo "[🟢 ]: '$component_name' component tests PASSED."
    PASSED_COMPONENT_TESTS+=("$component_name")
  else
    echo "[🔴 ]: '$component_name' component tests FAILED."
    FAILED_COMPONENT_TESTS+=("$component_name")
  fi

  docker container rm component-tests
}

clean_docker_containers() {
  echo
  echo "[🟠 ]: Starting docker container cleanup..."
  docker compose \
      -f docker-compose.yml \
      -f docker-compose.component.override.yml \
      -f docker-compose.component-sds.override.yml \
      -p "${BUILD_TAG}" \
      down -v --remove-orphans 2>/dev/null || true

  docker compose \
      -f docker-compose.yml \
      -f docker-compose.component.override.yml \
      -p "${BUILD_TAG}" \
      down -v --remove-orphans 2>/dev/null || true
  echo "[🟢 ]: Completed docker container cleanup."
}

print_test_summary() {
  if [ ${#FAILED_UNIT_TESTS[@]} -gt 0 ] || [ ${#PASSED_UNIT_TESTS[@]} -gt 0 ]; then
    print_unit_test_summary
  fi
  if [ ${#FAILED_COMPONENT_TESTS[@]} -gt 0 ] || [ ${#PASSED_COMPONENT_TESTS[@]} -gt 0 ]; then
    print_component_test_summary
  fi
}

print_component_test_summary() {
  echo
  echo "================================="
  echo "     Component Test Summary"
  echo "================================="
  if [ ${#FAILED_COMPONENT_TESTS[@]} -gt 0 ]; then
    echo "[🔴 ]: FAILED MODULES:"
    for test_name in "${FAILED_COMPONENT_TESTS[@]}"; do
      echo "      * $test_name"
    done
    echo "---------------------------------"
  fi
  echo "[🟢 ]: PASSED MODULES"
  if [ ${#PASSED_COMPONENT_TESTS[@]} -eq 0 ]; then
    echo "  (None)"
  else
    for test_name in "${PASSED_COMPONENT_TESTS[@]}"; do
      echo "      * $test_name"
    done
  fi
  echo "================================="
}

print_unit_test_summary() {
  echo
  echo "================================="
  echo "      Unit Test Summary"
  echo "================================="
  if [ ${#FAILED_UNIT_TESTS[@]} -gt 0 ]; then
    echo "[🔴 ]: FAILED MODULES:"
    for test_name in "${FAILED_UNIT_TESTS[@]}"; do
      echo "      * $test_name"
    done
    echo "---------------------------------"
  fi
  echo "[🟢 ]: PASSED MODULES"
  if [ ${#PASSED_UNIT_TESTS[@]} -eq 0 ]; then
    echo "  (None)"
  else
    for test_name in "${PASSED_UNIT_TESTS[@]}"; do
      echo "      * $test_name"
    done
  fi
  echo "================================="
}

run_unit_tests() {
  run_unit_test_module "common"
  run_unit_test_module "mhs/common"
  run_unit_test_module "mhs/inbound"
  run_unit_test_module "mhs/outbound"
  run_unit_test_module "mhs/spineroutelookup"
}

run_component_test_sds() {
  clean_docker_containers
  setup_fake_spine_environment_variables
  build_component_test_dependencies
  build_component_test_docker
  run_sds_component_docker
  run_component_tests "SDS"
}

run_component_test_fake_spine() {
  clean_docker_containers
  setup_fake_spine_environment_variables
  build_component_test_dependencies
  build_component_test_docker
  run_spine_route_lookup_docker
  run_component_tests "Fake Spine"
}

run_all_tests() {
  run_unit_tests
  run_component_test_fake_spine
  run_component_test_sds
}

show_menu() {
  clear
  echo
  echo "=========================================="
  echo " Please select an option (press 1-5)"
  echo "=========================================="
  echo " (1) Run unit tests"
  echo " (2) Run fake-spine component tests"
  echo " (3) Run SDS component tests"
  echo " (4) Run all tests"
  echo " (5) Exit"
  echo "=========================================="
}

while true; do
  show_menu
  read -r -n 1 key
  clear

  case $key in
    '1')
      run_unit_tests
      break
      ;;
    '2')
      run_component_test_fake_spine
      clean_docker_containers
      break
      ;;
    '3')
      run_component_test_sds
      clean_docker_containers
      break
      ;;
    '4')
      run_all_tests
      clean_docker_containers
      break
      ;;
    '5')
      echo "Exiting."
      break
      ;;
    *)
      echo
      echo "Invalid option '$key'. Please press a number from 1-5."
      sleep 1
      ;;
  esac
done

print_test_summary
exit 0