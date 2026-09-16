#!/bin/bash
set -euo pipefail
export CI_REGISTRY_IMAGE="gitlab.cs.uni-duesseldorf.de:5001/voelkel/ds-skript"
echo "Building and pushing: $CI_REGISTRY_IMAGE:latest"
docker build --network=host -t "$CI_REGISTRY_IMAGE:latest" .
docker push "$CI_REGISTRY_IMAGE:latest"
