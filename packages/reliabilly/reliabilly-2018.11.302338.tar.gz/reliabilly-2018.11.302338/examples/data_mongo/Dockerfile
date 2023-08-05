FROM corpseware/reliabilly:latest

RUN mkdir /src/data_mongo
ADD requirements.txt /src/data_mongo

RUN pip install -r /src/data_mongo/requirements.txt

COPY . /src/data_mongo

WORKDIR /src

EXPOSE 8000
HEALTHCHECK --interval=2s CMD curl -f http://localhost:8000/data_mongo/ping/ || exit 1
ENTRYPOINT nameko run data_mongo.service