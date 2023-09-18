set -ex
# SET THE FOLLOWING VARIABLES
# docker hub username
USERNAME=nhsdev
# image name
IMAGE=nia-mhs-outbound-base
# bump version
docker run --rm -v "$PWD":/app treeder/bump patch
version=`cat VERSION`
echo "version: $version"

# Build, tag, push
docker buildx build -f Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag $USERNAME/$IMAGE:latest --tag $USERNAME/$IMAGE:$version --push