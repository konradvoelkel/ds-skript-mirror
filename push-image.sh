#!/bin/bash
# Notnagel fuer den Bau von Hand. Im Regelfall baut und pusht der CI-Job
# `build-image` (Kaniko) das Image, sobald sich Dockerfile oder requirements.txt
# auf main aendern; in jeder Pipeline auf main laesst er sich ausserdem von Hand starten.
set -euo pipefail
export CI_REGISTRY_IMAGE="gitlab.cs.uni-duesseldorf.de:5001/voelkel/ds-skript"
echo "Building and pushing: $CI_REGISTRY_IMAGE:latest"
docker build --network=host -t "$CI_REGISTRY_IMAGE:latest" .
docker push "$CI_REGISTRY_IMAGE:latest"
