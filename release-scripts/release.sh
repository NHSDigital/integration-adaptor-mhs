#!/bin/bash 

export BUILD_TAG=latest

cd ..

./build.sh

docker tag local/mhs-inbound:latest nhsdev/nia-mhs-inbound:0.0.2
docker tag local/mhs-outbound:latest nhsdev/nia-mhs-outbound:0.0.2
docker tag local/mhs-route:latest nhsdev/nia-mhs-route:0.0.2

docker push nhsdev/nia-mhs-inbound:0.0.2
docker push nhsdev/nia-mhs-outbound:0.0.2
docker push nhsdev/nia-mhs-route:0.0.2
