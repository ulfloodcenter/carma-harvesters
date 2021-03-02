FROM debian:buster-slim
ENV PYTHONBUFFERED 1
RUN mkdir /tmp/data
RUN mkdir /tmp/bin
ADD ./bin /tmp/bin
ENV PATH="/tmp/bin:${PATH}"
RUN mkdir /tmp/code
ADD ./src /tmp/code/
WORKDIR /tmp/code

# Install CARMA depdendencies
RUN apt-get update -y \
    && apt-get install -y build-essential python3-pip p7zip-full \
        gdal-bin libgdal-dev python3-gdal libsqlite3-mod-spatialite \
    && python3 -m pip install -U pip \
    && python3 -m pip install https://files.pythonhosted.org/packages/05/0c/d7c2c7c370ea5368b813a44e772247ed1a461dc47de70c5d02e079abc7e0/pyproj-3.0.0.post1-cp37-cp37m-manylinux2010_x86_64.whl \
    && python3 -m pip install -r requirements.txt \
    && cd carma-schema \
    && python3 setup.py install \
    && cd .. \
    && python3 setup.py install
WORKDIR /tmp/data
