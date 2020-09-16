FROM osgeo/gdal
ENV PYTHONBUFFERED 1
RUN mkdir /tmp/data
RUN mkdir /tmp/bin
ADD ./bin /tmp/bin
ENV PATH="/tmp/bin:${PATH}"
RUN mkdir /tmp/code
ADD ./src /tmp/code/
WORKDIR /tmp/code
RUN apt-get update -y \
    && apt-get install -y python3-pip p7zip-full \
    && pip3 install -r requirements.txt \
    && python setup.py install
WORKDIR /tmp/data
