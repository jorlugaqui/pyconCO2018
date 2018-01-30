FROM alpine:latest
MAINTAINER Jorge Galvis <jorlugaqui@gmail.com>

COPY requirements.txt requirements.txt

RUN apk add --no-cache libstdc++ lapack-dev \
        python3 ca-certificates postgresql-client && \
    apk add --no-cache \
        --virtual=.build-dependencies \
        g++ gfortran musl-dev \
        python3-dev \
        postgresql-dev && \ 
    pip3 install -U pip && \
    pip3 install --no-cache-dir -Ur requirements.txt &&\
    rm -r /root/.cache && \
    apk del .build-dependencies

WORKDIR /app
COPY . /app
