FROM continuumio/miniconda3

RUN mkdir /opt/drugcell

COPY assets/drugcell /opt/drugcell

RUN conda install -y pytorch torchvision cpuonly -c pytorch

RUN mkdir /tmp/drugcell
COPY dist/*.whl /tmp/drugcell/

RUN pip install /tmp/drugcell/drugcellfindcell*whl

COPY assets/*.yml /tmp/drugcell/

RUN conda env create -f /tmp/drugcell/environment_cpu_linux.yml

RUN rm -rf /tmp/drugcell

ENTRYPOINT ["/opt/conda/bin/drugcellfindcellcmd.py"]
CMD ["--help"]
