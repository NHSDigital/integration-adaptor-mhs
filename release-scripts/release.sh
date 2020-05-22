#!/bin/bash 

export NEXT_BUILD_TAG=0.0.3

cd ..

./build.sh

docker tag local/mhs-inbound:latest nhsdev/nia-mhs-inbound:$NEXT_BUILD_TAG
docker tag local/mhs-outbound:latest nhsdev/nia-mhs-outbound:$NEXT_BUILD_TAG
docker tag local/mhs-route:latest nhsdev/nia-mhs-route:$NEXT_BUILD_TAG

docker tag nhsdev/nia-mhs-inbound:$NEXT_BUILD_TAG nhsdev/nia-mhs-inbound:latest
docker tag nhsdev/nia-mhs-outbound:$NEXT_BUILD_TAG nhsdev/nia-mhs-outbound:latest
docker tag nhsdev/nia-mhs-route:$NEXT_BUILD_TAG nhsdev/nia-mhs-route:latest

# docker push nhsdev/nia-mhs-inbound:$NEXT_BUILD_TAG
# docker push nhsdev/nia-mhs-outbound:$NEXT_BUILD_TAG
# docker push nhsdev/nia-mhs-route:$NEXT_BUILD_TAG
