FROM alpine:latest
MAINTAINER Jorge Galvis <jorlugaqui@gmail.com>

RUN apk add --no-cache python3 ca-certificates python3-dev postgresql-client\
  postgresql-dev build-base\
  && pip3 install -U pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -Ur requirements.txt && rm -r /root/.cache

COPY . /app

RUN chown -R nobody:nobody /app
USER nobody
