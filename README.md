# Paper and Data analysis for [RaaS](https://github.com/jwons/raas) 

## To generate the Word document that serves as our submission

On a system with Docker installed run the `compile_paper.sh` bash script.
This will generate a Docker container with all necessary dependencies for the analysis/paper; then will run the data analysis from start to finish; insert all the tables, figures, and values referenced into the paper; and then will compile the paper. 
While all this will execute in the container environment, all the results (most importantly the main.docx) will be saved to the current working directory on the host machine, NOT the Docker container environment. 

## To work on the paper and analysis, 
You will need the following python packages (which we recommend installing in a new conda environment):

```{bash}
pip install tabulate plotly kaleido jupyter nbconvert pandoc-fignos pandoc-eqnos pandoc-tablenos pandoc-secnos
```

Once that python environment is setup to:
 - generate the full paper run `make main.docx`
 - generate the markdown that is ultimately compiled into the final Word doc run `make complete_paper.md`

Since this workflow uses make, if any changes are made to the data analysis, figures, or macros then the data analysis will be re-executed as necessary. 

