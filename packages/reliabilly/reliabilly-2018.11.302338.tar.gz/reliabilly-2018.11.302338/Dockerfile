FROM python:3.6-alpine3.6
LABEL maintainer="jblouse@corpseware.com"

RUN apk --update add curl bash

RUN pip install --upgrade pip

RUN apk add --no-cache --virtual .build-deps gcc libc-dev python-dev git libffi-dev openssl-dev && \
    pip install --no-cache-dir reliabilly && \
    apk del .build-deps

RUN mkdir /src
