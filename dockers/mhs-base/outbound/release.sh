# Enables 'set -ex' options for the shell to exit immediately on error and print commands as
# they are executed. Increments the version number using the 'treeder/bump' Docker container.
# Builds a Docker image for both ARM64 and AMD64 architectures, tags the image with 'latest'
# and the new version number, and pushes the images to Docker Hub under the specified username.

set -ex
USERNAME=nhsdev
IMAGE=nia-mhs-outbound-base
docker run --rm -v "$PWD":/app treeder/bump patch
version=`cat VERSION`
echo "version: $version"
docker buildx build -f Dockerfile . --platform linux/arm64/v8,linux/amd64 --tag $USERNAME/$IMAGE:latest --tag $USERNAME/$IMAGE:$version --push