# These are all the macros defined from the data analysis that will get inserted into the final paper
md_inserts := $(wildcard md_inserts/*.md)

# These are all the figures created from the data analysis or by hand that will be referenced in the final paper
figures := $(wildcard figures/*.png)

scripts/generate_figures_plots.py: scripts/generate_figures_plots.ipynb
	cd scripts && jupyter nbconvert generate_figures_plots.ipynb --to python && python generate_figures_plots.py

complete_paper.md: scripts/analysis_completed.py scripts/generate_figures_plots.py $(md_inserts) $(figures)
	python scripts/analysis_completed.py