FROM python:3.9-slim-buster

WORKDIR /code

ARG OAUTH_TOKEN
ARG URL_PATH

RUN apt-get update \
&& apt-get install -y --no-install-recommends git build-essential gcc autoconf automake libtool python-dev pkg-config curl \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/openvenues/libpostal \
    && cd libpostal \
    && ./bootstrap.sh \
    && mkdir datadir \
    && ./configure --datadir=/datadir \
    && make \
    && make install \
    && ldconfig \
    && export LD_LIBRARY_PATH=/usr/local/lib

RUN git clone https://${OAUTH_TOKEN}:x-oauth-basic@github.com/${URL_PATH} \
    && cd graph-location \
    && pip install --no-cache-dir -r requirements.txt \
	&& python setup.py install_docker

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn","--app-dir=app", "main:app", "--host", "0.0.0.0", "--port", "8000"]