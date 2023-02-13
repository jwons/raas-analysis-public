# Data analysis for [RaaS](https://github.com/jwons/raas) 

The data analysis for RaaS is tightly coupled with the (currently under submission) paper. This repository represents just the data analysis portion of our entire pipeline that would normally end with compiling a Word document. All of the paper sections have been removed from this repository, so it is just the data and our analysis. 

## To execute the analysis

On a system with Docker installed run the `run_analysis.sh` bash script.

Or, using windows with Docker, execute these two commands in PowerShell:

```{bash}
docker build . -t raas-analysis

docker run --rm --name raas-analysis-container --mount type=bind,source="$(pwd)",target=/home/jovyan/work  raas-analysis bash __run_analysis_in_container.sh
```
This will generate a Docker container with all necessary dependencies for the analysis/paper; then will run the data analysis from start to finish. In our full, not currently public repository, this would also generate the paper. The results of our analysis our saved to two directories, either md_inserts for text/tables, or figures for figures. 

