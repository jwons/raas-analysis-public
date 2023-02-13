#!/bin/bash

docker build . -t raas-analysis

docker run --rm --name raas-analysis-container --mount type=bind,source="$(pwd)",target=/home/jovyan/work  raas-analysis bash __run_analysis_in_container.sh
