FROM python:3.9-alpine

RUN pip install --upgrade pip

# needed for grpcio and protobuf
RUN pip install --upgrade setuptools==49.6.0

# needed for grpcio and protobuf
RUN apk add gcc g++ linux-headers

RUN pip install grpcio protobuf flask

WORKDIR /app

# copy proto folder to access gRPC info
RUN mkdir -p proto

# copy frontend folder since running from src/
RUN mkdir -p frontend

COPY ./src/proto /app/proto

COPY ./src/front-end /app/frontend

ENTRYPOINT ["python3", "-u", "frontend/frontend.py"]
