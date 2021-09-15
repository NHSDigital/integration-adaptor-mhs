#!/bin/bash 

export BUILD_TAG=1.0.3

cd ..

./build.sh

docker tag local/mhs-inbound:${BUILD_TAG} nhsdev/nia-mhs-inbound:${BUILD_TAG}
docker tag local/mhs-outbound:${BUILD_TAG} nhsdev/nia-mhs-outbound:${BUILD_TAG}
docker tag local/mhs-route:${BUILD_TAG} nhsdev/nia-mhs-route:${BUILD_TAG}

if [ "$1" == "-y" ];
then

    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [[ "$BRANCH" != "develop" ]]; then
        echo 'Can only run this on the develop branch';
        exit 1;
    fi

    echo "Tagging and pushing Docker image and git tag"
    docker push nhsdev/nia-mhs-inbound:${BUILD_TAG}
    docker push nhsdev/nia-mhs-outbound:${BUILD_TAG}
    docker push nhsdev/nia-mhs-route:${BUILD_TAG}
    git tag -a ${BUILD_TAG} -m "Release ${BUILD_TAG}"
    git push origin ${BUILD_TAG}
fi
