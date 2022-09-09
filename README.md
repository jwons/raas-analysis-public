# Data analysis for [RaaS](https://github.com/jwons/raas) 

## To execute the analysis

On a system with Docker installed run the `compile_paper.sh` bash script.

Or, using windows with Docker, execute these two commands in PowerShell:

```{bash}
docker build . -t raas-eval

docker run --rm --name raas-eval-make --mount type=bind,source="$(pwd)",target=/home/jovyan/work  raas-eval bash make_paper_in_container.sh
```
This will generate a Docker container with all necessary dependencies for the analysis/paper; then will run the data analysis from start to finish. In our full, not currently public repository, this would also generate the paper. The results of our analysis our saved to two directories, either md_inserts for text/tables, or figures for figures. 

