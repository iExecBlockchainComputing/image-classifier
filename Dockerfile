FROM ubuntu:20.04

RUN  apt-get update \
    && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh && \
    bash Miniconda3-py38_4.10.3-Linux-x86_64.sh -b -p /root/miniconda

ENV CONDA_AUTO_UPDATE_CONDA="false"
ENV PATH=/root/miniconda/bin:$PATH

RUN conda install -c conda-forge tensorflow==2.7.0
RUN conda install -c conda-forge matplotlib

COPY ./src /app

ENTRYPOINT ["/root/miniconda/bin/python3.8", "/app/app.py"]
