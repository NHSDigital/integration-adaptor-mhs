set -e
BASE_IMAGE_TAG="${BASE_IMAGE_TAG:-latest}"
BUILD_TAG="${BUILD_TAG:-latest}"
docker build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG -t local/mhs-inbound:${BUILD_TAG} -f mhs/inbound/Dockerfile .
docker build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG -t local/mhs-outbound:${BUILD_TAG} -f mhs/outbound/Dockerfile .
docker build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG -t local/mhs-route:${BUILD_TAG} -f mhs/spineroutelookup/Dockerfile .
