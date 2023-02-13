#!/bin/bash

docker build . -t raas-eval
#
#docker run \
#  --rm \
#  -e JUPYTER_ENABLE_LAB=yes \
#  -p 8888:8888 \
#  raas-eval

docker run \
  --rm \
  -e JUPYTER_ENABLE_LAB=yes \
  -p 8888:8888 \
  --name raas-eval \
  --mount type=bind,source="$(pwd)",target=/home/jovyan/work \
  raas-eval
