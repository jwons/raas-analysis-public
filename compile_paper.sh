#!/bin/bash

docker build . -t raas-eval

docker run --rm --name raas-eval-make --mount type=bind,source="$(pwd)",target=/home/jovyan/work  raas-eval bash make_paper_in_container.sh
