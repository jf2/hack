#!/bin/bash

# Taken from https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
# Assumes container cluster already exists

PROJECT_ID=$1

if [ -z "$1" ]; then
    echo "Usage: $0 PROJECT_ID"
    exit -1
fi

set -e
set -x

GIT_COMMIT_HASH=$(git rev-parse --short HEAD)

echo $GIT_COMMIT_HASH > commit_hash.txt

docker build . -t gcr.io/${PROJECT_ID}/hack-zurich:latest
gcloud docker -- push gcr.io/${PROJECT_ID}/hack-zurich:latest

gcloud config set project $PROJECT_ID
gcloud config set compute/zone europe-west2-b

gcloud container clusters get-credentials hello-world-cluster


kubectl delete deployment/hello-web
kubectl run hello-web --image=gcr.io/${PROJECT_ID}/hack-zurich:latest --port 5000

# Assumes external port is already exposed