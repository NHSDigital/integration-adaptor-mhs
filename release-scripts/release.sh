#!/bin/bash

set -e

export BUILD_TAG=1.2.7

git fetch
git checkout $BUILD_TAG

cd ..

# These are buildx versions of what is inside of `build.sh`
BASE_IMAGE_TAG="${BASE_IMAGE_TAG:-latest}"
docker buildx build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG  -f mhs/inbound/Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag nhsdev/nia-mhs-inbound:${BUILD_TAG} --push
docker buildx build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG  -f mhs/outbound/Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag nhsdev/nia-mhs-outbound:${BUILD_TAG} --push
docker buildx build --build-arg BASE_IMAGE_TAG=$BASE_IMAGE_TAG  -f mhs/spineroutelookup/Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag nhsdev/nia-mhs-route:${BUILD_TAG} --push