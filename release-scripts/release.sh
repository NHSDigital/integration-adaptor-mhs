#!/bin/bash

set -e

export BUILD_TAG=1.3.0

git fetch
git checkout $BUILD_TAG

cd ..

# These are buildx versions of what is inside of `build.sh`
docker buildx build -f docker/inbound/Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag nhsdev/nia-mhs-inbound:${BUILD_TAG} --push
docker buildx build -f docker/outbound/Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag nhsdev/nia-mhs-outbound:${BUILD_TAG} --push
docker buildx build -f docker/spineroutelookup/Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag nhsdev/nia-mhs-route:${BUILD_TAG} --push