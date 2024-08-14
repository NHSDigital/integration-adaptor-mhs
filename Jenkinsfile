pipeline {
    agent{
        label 'jenkins-workers'
    }

    environment {
        BUILD_TAG = sh label: 'Generating build tag', returnStdout: true, script: 'python3 pipeline/scripts/tag.py ${GIT_BRANCH} ${BUILD_NUMBER} ${GIT_COMMIT}'
        BUILD_TAG_LOWER = sh label: 'Lowercase build tag', returnStdout: true, script: "echo -n ${BUILD_TAG} | tr '[:upper:]' '[:lower:]'"
        ENVIRONMENT_ID = "build"
        MHS_INBOUND_QUEUE_NAME = "${ENVIRONMENT_ID}-inbound"
        LOCAL_INBOUND_IMAGE_NAME = "local/mhs-inbound:${BUILD_TAG}"
        LOCAL_OUTBOUND_IMAGE_NAME = "local/mhs-outbound:${BUILD_TAG}"
        LOCAL_ROUTE_IMAGE_NAME = "local/mhs-route:${BUILD_TAG}"
        LOCAL_FAKE_SPINE_IMAGE_NAME = "local/fake-spine:${BUILD_TAG}"
        INBOUND_IMAGE_NAME = "${DOCKER_REGISTRY}/mhs/inbound:${BUILD_TAG}"
        OUTBOUND_IMAGE_NAME = "${DOCKER_REGISTRY}/mhs/outbound:${BUILD_TAG}"
        ROUTE_IMAGE_NAME = "${DOCKER_REGISTRY}/mhs/route:${BUILD_TAG}"
        FAKE_SPINE_IMAGE_NAME = "${DOCKER_REGISTRY}/fake-spine:${BUILD_TAG}"
    }

    stages {
        stage('Determine python version') {
            steps {
                script {
                    def python_version = sh(script: "python3 --version", returnStdout: true).trim()
                    echo "Current Python version: ${python_version}"
                }
            }
        }
        stage('Prepare and download Python 3.9') {
            steps {
                sh 'apt update –fix-missing -y | echo'
                sh 'apt install -y build-essential libssl-dev libffi-dev zlib1g-dev libbz2-dev wget curl xz-utils'
                sh 'wget https://www.python.org/ftp/python/3.9.19/Python-3.9.19.tgz'
                sh 'tar -xvzf Python-3.9.19.tgz'
            }
        }
        stage('Compile and install Python 3.9') {
            steps {
                dir('Python-3.9.19') {
                    sh './configure --enable-optimizations'
                    sh 'make altinstall'
                }
            }
        }
        stage('Build & test Common') {
            steps {
                dir('common') {
                    buildModules('Installing common dependencies')
                    executeUnitTestsWithCoverage()
                }
            }
        }
        stage('Build & test MHS Common') {
            steps {
                dir('mhs/common') {
                    buildModules('Installing mhs common dependencies')
                    executeUnitTestsWithCoverage()
                }
            }
        }
        stage('Build MHS') {
            parallel {
                stage('Inbound') {
                    stages {
                        stage('Build') {
                            steps {
                                dir('mhs/inbound') {
                                    buildModules('Installing inbound dependencies')
                                }
                            }
                        }
                        stage('Unit test') {
                            steps {
                                dir('mhs/inbound') {
                                    executeUnitTestsWithCoverage()
                                }
                            }
                        }
                        stage('Build and Push image') {
                            when {
                                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
                            }
                            steps {
                                buildAndPushImage('${LOCAL_INBOUND_IMAGE_NAME}', '${INBOUND_IMAGE_NAME}', 'mhs/inbound/Dockerfile')
                            }
                        }
                    }
                }
                stage('Outbound') {
                    stages {
                        stage('Build') {
                            steps {
                                dir('mhs/outbound') {
                                    buildModules('Installing outbound dependencies')
                                }
                            }
                        }
                        stage('Unit test') {
                            steps {
                                dir('mhs/outbound') {
                                    executeUnitTestsWithCoverage()
                                }
                            }
                        }
                        stage('Build and Push image') {
                          when {
                              expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
                          }
                          steps {
                              buildAndPushImage('${LOCAL_OUTBOUND_IMAGE_NAME}', '${OUTBOUND_IMAGE_NAME}', 'mhs/outbound/Dockerfile')
                          }
                        }
                    }
                }
                stage('Route') {
                    stages {
                        stage('Build') {
                            steps {
                                dir('mhs/spineroutelookup') {
                                    buildModules('Installing route lookup dependencies')
                                }
                            }
                        }
                        stage('Unit test') {
                            steps {
                                dir('mhs/spineroutelookup') {
                                    executeUnitTestsWithCoverage()
                                }
                            }
                        }
                        stage('Build and Push image') {
                            when {
                                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
                            }
                            steps {
                                buildAndPushImage('${LOCAL_ROUTE_IMAGE_NAME}', '${ROUTE_IMAGE_NAME}', 'mhs/spineroutelookup/Dockerfile')
                            }
                        }
                    }
                }
                stage('Fake Spine') {
                    stages {
                        stage('Build and Push image') {
                            steps {
                                buildAndPushImage('${LOCAL_FAKE_SPINE_IMAGE_NAME}', '${FAKE_SPINE_IMAGE_NAME}', 'integration-tests/fake_spine/Dockerfile')
                            }
                        }
                    }
                }
            }
        }

        stage('Test') {
            // NIAD-189: Parallel component and integration tests disabled due to intermittent build failures
            //parallel {
            stages {
                stage('Run Component Tests (SpineRouteLookup)') {
                    stages {
                        stage('Deploy component locally (SpineRouteLookup)') {
                            steps {
                                sh label: 'Setup component test environment', script: './integration-tests/setup_component_test_env.sh'
                                sh label: 'Start containers', script: '''
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml down -v
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -p custom_network down -v
                                    . ./component-test-source.sh
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml build
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -p ${BUILD_TAG_LOWER} up -d'''
                            }
                        }
                        stage('Component Tests (SpineRouteLookup)') {
                            steps {
                                sh label: 'Run component tests', script: '''docker build -t local/mhs-componenttest:$BUILD_TAG -f ./component-test.Dockerfile .'''
                                sh label: 'Run component tests', script:'''

                                    docker run --network "${BUILD_TAG_LOWER}_default" \
                                        --env "MHS_ADDRESS=http://outbound" \
                                        --env "AWS_ACCESS_KEY_ID=test" \
                                        --env "AWS_SECRET_ACCESS_KEY=test" \
                                        --env "MHS_DB_ENDPOINT_URL=http://dynamodb:8000" \
                                        --env "FAKE_SPINE_ADDRESS=http://fakespine" \
                                        --env "MHS_INBOUND_QUEUE_BROKERS=amqp://rabbitmq:5672" \
                                        --env "MHS_INBOUND_QUEUE_NAME=inbound" \
                                        --env "SCR_ADDRESS=http://scradaptor" \
                                        --name "${BUILD_TAG_LOWER}_component_test" \
                                        local/mhs-componenttest:$BUILD_TAG
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            sh label: 'Docker status', script: 'docker ps --all'
                            sh label: 'Dump container logs to files', script: '''
                                mkdir -p logs
                                docker logs ${BUILD_TAG_LOWER}_route_1 > logs/route_1.log
                                docker logs ${BUILD_TAG_LOWER}_outbound_1 > logs/outbound_1.log
                                docker logs ${BUILD_TAG_LOWER}_inbound_1 > logs/inbound_1.log
                                docker logs ${BUILD_TAG_LOWER}_fakespine_1 > logs/fakespine_1.log
                                docker logs ${BUILD_TAG_LOWER}_rabbitmq_1 > logs/rabbitmq_1.log
                                docker logs ${BUILD_TAG_LOWER}_redis_1 > logs/redis_1.log
                                docker logs ${BUILD_TAG_LOWER}_dynamodb_1 > logs/dynamodb_1.log
                                docker logs ${BUILD_TAG_LOWER}_mongodb_1 > logs/mongodb_1.log
                            '''
                            archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
                            sh label: 'Docker compose down', script: 'docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -p ${BUILD_TAG_LOWER} down -v'
                        }
                    }
                }

                stage('Run Component Tests (SDS API)') {
                    stages {
                        stage('Deploy component locally (SDS API)') {
                            steps {
                                sh label: 'Setup component test environment', script: './integration-tests/setup_component_test_env.sh'
                                sh label: 'Start containers', script: '''
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -f docker-compose.component-sds.override.yml down -v
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -f docker-compose.component-sds.override.yml -p custom_network down -v
                                    . ./component-test-source.sh
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -f docker-compose.component-sds.override.yml build
                                    docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -f docker-compose.component-sds.override.yml -p ${BUILD_TAG_LOWER} up -d
                                    '''
                            }
                        }
                        stage('Component Tests (SDS API)') {
                            steps {
                                sh label: 'Run component tests', script: '''
                                    docker build -t local/mhs-componenttest:$BUILD_TAG -f ./component-test.Dockerfile .
                                    docker run --rm --network "${BUILD_TAG_LOWER}_default" \
                                        --env "MHS_ADDRESS=http://outbound" \
                                        --env "AWS_ACCESS_KEY_ID=test" \
                                        --env "AWS_SECRET_ACCESS_KEY=test" \
                                        --env "MHS_DB_ENDPOINT_URL=http://dynamodb:8000" \
                                        --env "FAKE_SPINE_ADDRESS=http://fakespine" \
                                        --env "MHS_INBOUND_QUEUE_BROKERS=amqp://rabbitmq:5672" \
                                        --env "MHS_INBOUND_QUEUE_NAME=inbound" \
                                        --env "SCR_ADDRESS=http://scradaptor" \
                                        local/mhs-componenttest:$BUILD_TAG
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            sh label: 'Docker status', script: 'docker ps --all'
                            sh label: 'Docker inspect network', script: 'docker network inspect ${BUILD_TAG_LOWER}_default'
                            sh label: 'Dump container logs to files', script: '''
                                mkdir -p logs
                                docker logs ${BUILD_TAG_LOWER}_outbound_1 > logs/outbound_2.log
                                docker logs ${BUILD_TAG_LOWER}_inbound_1 > logs/inbound_2.log
                                docker logs ${BUILD_TAG_LOWER}_fakespine_1 > logs/fakespine_2.log
                                docker logs ${BUILD_TAG_LOWER}_rabbitmq_1 > logs/rabbitmq_2.log
                                docker logs ${BUILD_TAG_LOWER}_dynamodb_1 > logs/dynamodb_2.log
                                docker logs ${BUILD_TAG_LOWER}_sds-api-mock_1 > logs/sdsapimock_2.log

                            '''
                            archiveArtifacts artifacts: 'logs/*.log', fingerprint: true
                            sh label: 'Docker compose down', script: 'docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -f docker-compose.component-sds.override.yml -p ${BUILD_TAG_LOWER} down -v'
                        }
                    }
                }

                stage('Run Integration Tests (SpineRouteLookup)') {
                    options {
                        lock('exemplar-test-environment')
                    }
                    stages {
                        stage('Updating Terraform Binary') {
                            steps {
                                sh label: 'Updating Terraform Binary', script: """
                                            wget -O terraform.zip https://releases.hashicorp.com/terraform/0.12.31/terraform_0.12.31_linux_amd64.zip && \
                                            unzip -o terraform.zip -d /usr/bin/ && \
                                            rm terraform.zip
                                """
                            }
                        }
                        stage('Deploy MHS (SpineRouteLookup)') {
                            steps {
                                dir('pipeline/terraform/mhs-environment') {
                                    sh label: 'Initialising Terraform', script: """
                                            terraform init \
                                            -backend-config="bucket=${TF_STATE_BUCKET}" \
                                            -backend-config="region=${TF_STATE_BUCKET_REGION}" \
                                            -backend-config="key=${ENVIRONMENT_ID}-mhs.tfstate" \
                                            -backend-config="dynamodb_table=${ENVIRONMENT_ID}-${TF_MHS_LOCK_TABLE_NAME}" \
                                            -input=false -no-color
                                        """
                                    sh label: 'Applying Terraform configuration', script: """
                                            terraform apply -no-color -auto-approve \
                                            -var environment_id=${ENVIRONMENT_ID} \
                                            -var build_id=${BUILD_TAG} \
                                            -var supplier_vpc_id=${SUPPLIER_VPC_ID} \
                                            -var opentest_vpc_id=${OPENTEST_VPC_ID} \
                                            -var internal_root_domain=${INTERNAL_ROOT_DOMAIN} \
                                            -var mhs_outbound_service_minimum_instance_count=3 \
                                            -var mhs_outbound_service_maximum_instance_count=9 \
                                            -var mhs_inbound_service_minimum_instance_count=3 \
                                            -var mhs_inbound_service_maximum_instance_count=9 \
                                            -var mhs_route_service_minimum_instance_count=3 \
                                            -var mhs_route_service_maximum_instance_count=9 \
                                            -var task_role_arn=${TASK_ROLE} \
                                            -var execution_role_arn=${TASK_EXECUTION_ROLE} \
                                            -var task_scaling_role_arn=${TASK_SCALING_ROLE} \
                                            -var ecr_address=${DOCKER_REGISTRY} \
                                            -var mhs_outbound_validate_certificate=${MHS_OUTBOUND_VALIDATE_CERTIFICATE} \
                                            -var mhs_log_level=DEBUG \
                                            -var mhs_outbound_spineroutelookup_verify_certificate="False" \
                                            -var mhs_outbound_http_proxy=${MHS_OUTBOUND_HTTP_PROXY} \
                                            -var mhs_state_table_read_capacity=5 \
                                            -var mhs_state_table_write_capacity=5 \
                                            -var mhs_sync_async_table_read_capacity=5 \
                                            -var mhs_sync_async_table_write_capacity=5 \
                                            -var mhs_spine_org_code=${SPINE_ORG_CODE} \
                                            -var inbound_queue_brokers="${MHS_INBOUND_QUEUE_BROKERS}" \
                                            -var inbound_queue_name="${MHS_INBOUND_QUEUE_NAME}" \
                                            -var inbound_queue_username_arn=${INBOUND_QUEUE_USERNAME_ARN} \
                                            -var inbound_queue_password_arn=${INBOUND_QUEUE_PASSWORD_ARN} \
                                            -var party_key_arn=${PARTY_KEY_ARN} \
                                            -var client_cert_arn=${CLIENT_CERT_ARN} \
                                            -var client_key_arn=${CLIENT_KEY_ARN} \
                                            -var ca_certs_arn=${CA_CERTS_ARN} \
                                            -var route_ca_certs_arn=${ROUTE_CA_CERTS_ARN} \
                                            -var outbound_alb_certificate_arn=${OUTBOUND_ALB_CERT_ARN} \
                                            -var route_alb_certificate_arn=${ROUTE_ALB_CERT_ARN} \
                                            -var mhs_resynchroniser_max_retries=${MHS_RESYNC_RETRIES} \
                                            -var mhs_resynchroniser_interval=${MHS_RESYNC_INTERVAL} \
                                            -var spineroutelookup_service_sds_url=${SPINEROUTELOOKUP_SERVICE_LDAP_URL} \
                                            -var spineroutelookup_service_search_base=${SPINEROUTELOOKUP_SERVICE_SEARCH_BASE} \
                                            -var spineroutelookup_service_disable_sds_tls=${SPINEROUTELOOKUP_SERVICE_DISABLE_TLS} \
                                            -var elasticache_node_type="cache.t2.micro" \
                                            -var mhs_forward_reliable_endpoint_url=${MHS_FORWARD_RELIABLE_ENDPOINT_URL} \
                                            -var mhs_outbound_routing_lookup_method="SPINE_ROUTE_LOOKUP" \
                                            -var mhs_sds_api_url="" \
                                            -var mhs_sds_api_key_arn=${MHS_SDS_API_KEY_ARN} \
                                        """
                                    script {
                                        env.MHS_ADDRESS = sh (
                                            label: 'Obtaining outbound LB DNS name',
                                            returnStdout: true,
                                            script: "echo \"https://\$(terraform output outbound_lb_domain_name)\""
                                        ).trim()
                                        env.MHS_OUTBOUND_TARGET_GROUP = sh (
                                            label: 'Obtaining outbound LB target group ARN',
                                            returnStdout: true,
                                            script: "terraform output outbound_lb_target_group_arn"
                                        ).trim()
                                        env.MHS_INBOUND_TARGET_GROUP = sh (
                                            label: 'Obtaining inbound LB target group ARN',
                                            returnStdout: true,
                                            script: "terraform output inbound_lb_target_group_arn"
                                        ).trim()
                                        env.MHS_ROUTE_TARGET_GROUP = sh (
                                            label: 'Obtaining route LB target group ARN',
                                            returnStdout: true,
                                            script: "terraform output route_lb_target_group_arn"
                                        ).trim()
                                        env.MHS_STATE_TABLE_NAME = sh (
                                            label: 'Obtaining the table name used for the MHS state',
                                            returnStdout: true,
                                            script: "terraform output mhs_state_table_name"
                                        ).trim()
                                        env.MHS_SYNC_ASYNC_TABLE_NAME = sh (
                                            label: 'Obtaining the table name used for the MHS sync/async state',
                                            returnStdout: true,
                                            script: "terraform output mhs_sync_async_table_name"
                                        ).trim()
                                    }
                                }
                            }
                        }
                    }
                }
                stage('Run Integration Tests (SDS API)') {
                    options {
                        lock('exemplar-test-environment')
                    }
                    stages {
                        stage('Deploy MHS (SDS API)') {
                            steps {
                                dir('pipeline/terraform/mhs-environment') {
                                    sh label: 'Initialising Terraform', script: """
                                            terraform init \
                                            -backend-config="bucket=${TF_STATE_BUCKET}" \
                                            -backend-config="region=${TF_STATE_BUCKET_REGION}" \
                                            -backend-config="key=${ENVIRONMENT_ID}-mhs.tfstate" \
                                            -backend-config="dynamodb_table=${ENVIRONMENT_ID}-${TF_MHS_LOCK_TABLE_NAME}" \
                                            -input=false -no-color
                                        """
                                    sh label: 'Applying Terraform configuration', script: """
                                            terraform apply -no-color -auto-approve \
                                            -var environment_id=${ENVIRONMENT_ID} \
                                            -var build_id=${BUILD_TAG} \
                                            -var supplier_vpc_id=${SUPPLIER_VPC_ID} \
                                            -var opentest_vpc_id=${OPENTEST_VPC_ID} \
                                            -var internal_root_domain=${INTERNAL_ROOT_DOMAIN} \
                                            -var mhs_outbound_service_minimum_instance_count=3 \
                                            -var mhs_outbound_service_maximum_instance_count=9 \
                                            -var mhs_inbound_service_minimum_instance_count=3 \
                                            -var mhs_inbound_service_maximum_instance_count=9 \
                                            -var mhs_route_service_minimum_instance_count=3 \
                                            -var mhs_route_service_maximum_instance_count=9 \
                                            -var task_role_arn=${TASK_ROLE} \
                                            -var execution_role_arn=${TASK_EXECUTION_ROLE} \
                                            -var task_scaling_role_arn=${TASK_SCALING_ROLE} \
                                            -var ecr_address=${DOCKER_REGISTRY} \
                                            -var mhs_outbound_validate_certificate=${MHS_OUTBOUND_VALIDATE_CERTIFICATE} \
                                            -var mhs_log_level=DEBUG \
                                            -var mhs_outbound_spineroutelookup_verify_certificate="False" \
                                            -var mhs_outbound_http_proxy=${MHS_OUTBOUND_HTTP_PROXY} \
                                            -var mhs_state_table_read_capacity=5 \
                                            -var mhs_state_table_write_capacity=5 \
                                            -var mhs_sync_async_table_read_capacity=5 \
                                            -var mhs_sync_async_table_write_capacity=5 \
                                            -var mhs_spine_org_code=${SPINE_ORG_CODE} \
                                            -var inbound_queue_brokers="${MHS_INBOUND_QUEUE_BROKERS}" \
                                            -var inbound_queue_name="${MHS_INBOUND_QUEUE_NAME}" \
                                            -var inbound_queue_username_arn=${INBOUND_QUEUE_USERNAME_ARN} \
                                            -var inbound_queue_password_arn=${INBOUND_QUEUE_PASSWORD_ARN} \
                                            -var party_key_arn=${PARTY_KEY_ARN} \
                                            -var client_cert_arn=${CLIENT_CERT_ARN} \
                                            -var client_key_arn=${CLIENT_KEY_ARN} \
                                            -var ca_certs_arn=${CA_CERTS_ARN} \
                                            -var route_ca_certs_arn=${ROUTE_CA_CERTS_ARN} \
                                            -var outbound_alb_certificate_arn=${OUTBOUND_ALB_CERT_ARN} \
                                            -var route_alb_certificate_arn=${ROUTE_ALB_CERT_ARN} \
                                            -var mhs_resynchroniser_max_retries=${MHS_RESYNC_RETRIES} \
                                            -var mhs_resynchroniser_interval=${MHS_RESYNC_INTERVAL} \
                                            -var spineroutelookup_service_sds_url=${SPINEROUTELOOKUP_SERVICE_LDAP_URL} \
                                            -var spineroutelookup_service_search_base=${SPINEROUTELOOKUP_SERVICE_SEARCH_BASE} \
                                            -var spineroutelookup_service_disable_sds_tls=${SPINEROUTELOOKUP_SERVICE_DISABLE_TLS} \
                                            -var elasticache_node_type="cache.t2.micro" \
                                            -var mhs_forward_reliable_endpoint_url=${MHS_FORWARD_RELIABLE_ENDPOINT_URL} \
                                            -var mhs_outbound_routing_lookup_method="SDS_API" \
                                            -var mhs_sds_api_url=${MHS_SDS_API_URL} \
                                            -var mhs_sds_api_key_arn=${MHS_SDS_API_KEY_ARN} \
                                        """
                                    script {
                                        env.MHS_ADDRESS = sh (
                                            label: 'Obtaining outbound LB DNS name',
                                            returnStdout: true,
                                            script: "echo \"https://\$(terraform output outbound_lb_domain_name)\""
                                        ).trim()
                                        env.MHS_OUTBOUND_TARGET_GROUP = sh (
                                            label: 'Obtaining outbound LB target group ARN',
                                            returnStdout: true,
                                            script: "terraform output outbound_lb_target_group_arn"
                                        ).trim()
                                        env.MHS_INBOUND_TARGET_GROUP = sh (
                                            label: 'Obtaining inbound LB target group ARN',
                                            returnStdout: true,
                                            script: "terraform output inbound_lb_target_group_arn"
                                        ).trim()
                                        env.MHS_ROUTE_TARGET_GROUP = sh (
                                            label: 'Obtaining route LB target group ARN',
                                            returnStdout: true,
                                            script: "terraform output route_lb_target_group_arn"
                                        ).trim()
                                        env.MHS_STATE_TABLE_NAME = sh (
                                            label: 'Obtaining the table name used for the MHS state',
                                            returnStdout: true,
                                            script: "terraform output mhs_state_table_name"
                                        ).trim()
                                        env.MHS_SYNC_ASYNC_TABLE_NAME = sh (
                                            label: 'Obtaining the table name used for the MHS sync/async state',
                                            returnStdout: true,
                                            script: "terraform output mhs_sync_async_table_name"
                                        ).trim()
                                    }
                                }
                            }
                        }
                    }
                }
            } // parallel
        }
    }
    post {
        always {
            cobertura coberturaReportFile: '**/coverage.xml'
            junit '**/test-reports/*.xml'
            sh 'docker-compose -f docker-compose.yml -f docker-compose.component.override.yml -p ${BUILD_TAG_LOWER} down -v'
            sh 'docker volume prune --force'
            // Prune Docker images for current CI build.
            // Note that the * in the glob patterns doesn't match /
            sh 'docker image rm -f $(docker images "*/*:*${BUILD_TAG}" -q) $(docker images "*/*/*:*${BUILD_TAG}" -q) || true'
        }
    }
}

void executeUnitTestsWithCoverage() {
    sh label: 'Running unit tests', script: 'pipenv run unittests-cov'
    sh label: 'Displaying code coverage report', script: 'pipenv run coverage-report'
    sh label: 'Exporting code coverage report', script: 'pipenv run coverage-report-xml'
//     SonarQube disabled as atm it's not set up on AWS
//     sh label: 'Running SonarQube analysis', script: "sonar-scanner -Dsonar.host.url=${SONAR_HOST} -Dsonar.login=${SONAR_TOKEN}"
}

void buildModules(String action) {
    sh label: action, script: 'pipenv install --dev --deploy --ignore-pipfile'
}

int ecrLogin(String aws_region) {
    String dockerLogin = "aws ecr get-login-password --region ${aws_region} | docker login -u AWS --password-stdin \"https://\$(aws sts get-caller-identity --query 'Account' --output text).dkr.ecr.${aws_region}.amazonaws.com\""
    return sh(label: "Logging in with Docker", script: dockerLogin, returnStatus: true)
}

void buildAndPushImage(String localImageName, String imageName, String dockerFile, String context = '.') {
    sh label: 'Running docker build', script: 'docker build -t ' + localImageName + ' -f ' + dockerFile + ' ' + context
    if (ecrLogin(TF_STATE_BUCKET_REGION) != 0 )  { error("Docker login to ECR failed") }
    sh label: 'Tag ecr image', script: 'docker tag ' + localImageName + ' ' + imageName
    String dockerPushCommand = "docker push " + imageName
    if (sh (label: "Pushing image", script: dockerPushCommand, returnStatus: true) !=0) { error("Docker push image failed") }
    sh label: 'Deleting local ECR image', script: 'docker rmi ' + imageName
}
