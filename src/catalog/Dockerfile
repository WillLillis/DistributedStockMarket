FROM python:3.9-alpine

RUN pip install --upgrade pip

# needed for grpcio and protobuf
RUN pip install --upgrade setuptools==49.6.0

# needed for grpcio and protobuf
RUN apk add gcc g++ linux-headers

RUN pip install grpcio protobuf requests

WORKDIR /app

# copy proto folder to access gRPC info
RUN mkdir -p proto

# copy catalog folder for persistent csv
RUN mkdir -p catalog

COPY ./src/proto /app/proto

COPY ./src/catalog /app/catalog

ENTRYPOINT ["python3", "-u", "catalog/catalog_service.py"]
