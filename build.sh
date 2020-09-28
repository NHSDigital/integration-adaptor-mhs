set -e
docker build -t local/mhs-inbound:${BUILD_TAG} -f mhs/inbound/Dockerfile .
docker build -t local/mhs-outbound:${BUILD_TAG} -f mhs/outbound/Dockerfile .
docker build -t local/mhs-route:${BUILD_TAG} -f mhs/spineroutelookup/Dockerfile .
