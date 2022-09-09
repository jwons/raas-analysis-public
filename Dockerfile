FROM jupyter/scipy-notebook:4d9c9bd9ced0

COPY . /home/jovyan/work

RUN pip install tabulate plotly kaleido jupyter nbconvert pandoc-fignos pandoc-eqnos pandoc-tablenos pandoc-secnos

USER root

RUN cp /home/jovyan/work/make_paper_in_container.sh /home/jovyan/

RUN sudo chown -R jovyan:users /home/jovyan/work
