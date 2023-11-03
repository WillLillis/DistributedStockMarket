#!/bin/bash

docker build -f src/front-end/Dockerfile -t frontend .

docker build -f src/catalog/Dockerfile -t catalog .

docker build -f src/order/Dockerfile -t order .
