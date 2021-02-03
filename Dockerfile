FROM debian:buster-slim
ENV PYTHONBUFFERED 1
RUN mkdir /tmp/data
RUN mkdir /tmp/bin
ADD ./bin /tmp/bin
ENV PATH="/tmp/bin:${PATH}"
RUN mkdir /tmp/code
ADD ./src /tmp/code/
WORKDIR /tmp/code
RUN apt-get update -y \
    && apt-get install -y build-essential python3-pip p7zip-full \
        gdal-bin libgdal-dev python3-gdal libsqlite3-mod-spatialite \
    && pip3 install -r requirements.txt \
    && cd carma-schema \
    && python3 setup.py install \
    && cd .. \
    && python3 setup.py install
WORKDIR /tmp/data
