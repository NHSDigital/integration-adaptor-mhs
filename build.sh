set -e
BUILD_TAG="${BUILD_TAG:-latest}"
docker build -t local/mhs-inbound:${BUILD_TAG} -f docker/inbound/Dockerfile .
docker build -t local/mhs-outbound:${BUILD_TAG} -f docker/outbound/Dockerfile .
docker build -t local/mhs-route:${BUILD_TAG} -f docker/spineroutelookup/Dockerfile .
