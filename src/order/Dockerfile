FROM python:3.9-alpine

RUN pip install --upgrade pip

# needed for grpcio and protobuf
RUN pip install --upgrade setuptools==49.6.0

# needed for grpcio and protobuf
RUN apk add gcc g++ linux-headers

RUN pip install grpcio protobuf

WORKDIR /app

# copy proto folder to access gRPC info
RUN mkdir -p proto

# copy order folder for persistent csv
RUN mkdir -p order

COPY ./src/proto /app/proto

COPY ./src/order /app/order

CMD ["python3", "-u", "order/order_service.py"]
