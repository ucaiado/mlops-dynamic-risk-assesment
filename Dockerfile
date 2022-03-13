FROM continuumio/miniconda3:latest

# change user
USER root


# install linux dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim  wget curl gnupg2\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


# Install additional python packages
COPY environment.yml /tmp/
RUN conda env create -f tmp/environment.yml && \
    rm -rf /root/.cache