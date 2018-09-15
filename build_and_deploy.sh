#!/bin/bash

# Taken from https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app
# Assumes container cluster already exists

PROJECT_ID=$1

if [ -z "$1"]; then
    echo "Usage: $0 PROJECT_ID"
    exit -1
fi

docker build . -t gcr.io/${PROJECT_ID}/hack-zurich:latest
gcloud docker -- push gcr.io/${PROJECT_ID}/hack-zurich:latest

gcloud container clusters get-credentials hello-world-cluster

kubectl delete deployment/hello-web
kubectl run hello-web --image=gcr.io/${PROJECT_ID}/hack-zurich:latest --port 5000

# Assumes external port is already exposed