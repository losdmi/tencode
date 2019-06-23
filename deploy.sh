#!/usr/bin/env bash

source ./.env

IMAGE_NAME=${DOCKER_IMAGES_PREFIX}'_bot'
TAR_NAME='container.tar'
ZIP_NAME='deploy.zip'

docker-compose build
docker save ${IMAGE_NAME} > ${TAR_NAME}
zip ${ZIP_NAME} .env ${TAR_NAME} docker-compose.yml
rm ${TAR_NAME}
rsync -rvzxh --no-p --no-o --no-g --partial --ignore-errors --progress \
    ${ZIP_NAME} \
    ${DEPLOY_HOST}:${DEPLOY_PATH}
rm ${ZIP_NAME}

ssh ${DEPLOY_HOST} 'cd '${DEPLOY_PATH}'; \
    unzip -o '${ZIP_NAME}'; \
    rm '${ZIP_NAME}'; \
    docker-compose down; \
    docker rmi '${IMAGE_NAME}'; \
    docker load -i '${TAR_NAME}'; \
    rm '${TAR_NAME}'; \
    docker-compose up -d'
