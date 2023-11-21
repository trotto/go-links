#!/bin/bash
build_images() {
  docker build --platform linux/amd64 --tag $1-docker.pkg.dev/$2/$3/$3:$4 .
}

deploy_images() {
  gcloud auth configure-docker us-central1-docker.pkg.dev
  docker push $1-docker.pkg.dev/$2/$3/$3:$4
}

if [ "$1" = false ]; then
  build_images $2 $3 $4 $5
elif [ "$1" = true ]; then
  build_images $2 $3 $4 $5
  deploy_images $2 $3 $4 $5
else
  echo "First arg must be a bool indicating whether to deploy or not."
  exit
fi