from concurrent import futures
from time import sleep
from flask import Flask, request, jsonify
import http.server as http
import json
import os
import sys
# to add access to proto folder
sys.path.append('..')
# for docker to register
sys.path.append('/app')
from proto import bazaar_pb2 # auto-generated grpc file
from proto import bazaar_pb2_grpc # auto-generated grpc file
import grpc # using grpc for client-server communication
from threading import Thread

# grab environment variable(s)
frontend_host = os.getenv('FRONTEND_HOST', 'frontend')
catalog_host = os.getenv('CATALOG_HOST', 'catalog')
order_host = os.getenv('ORDER_HOST', 'order')
order_host_2 = os.getenv('ORDER_HOST_2', 'order1')
order_host_3 = os.getenv('ORDER_HOST_3', 'order2')
order_port_1 = os.getenv('ORDER_PORT_1', 50054)
order_port_2 = os.getenv('ORDER_PORT_2', 50055)
order_port_3 = os.getenv('ORDER_PORT_3', 50056)
order_channel = None
order_stub = None

enable_cache = True if (os.getenv('DISABLE_CACHE') == None) else False # check if the DISABLE_CACHE environment variable is set
if enable_cache == False:
    print('Cache disabled')

# keys are names of stock
# value is another dictionary, ex.
# {
#   'price': 100,
#   'quantity': 40,
# }
g_cache = {}

def start_leader_election():
    global order_stub
    replica_hosts = [order_host, order_host_2, order_host_3]
    replicas = [order_port_1, order_port_2, order_port_3]
    replicas.sort()

    index = len(replicas) - 1
    while True:
        order_channel = grpc.insecure_channel(f'{replica_hosts[index]}:{replicas[index]}')
        order_stub = bazaar_pb2_grpc.BazaarStub(order_channel)
        resp, err = health_check()
        if err == None:
            leader_host = replica_hosts[index]
            leader_port = replicas[index]
            break
        index = index - 1 if index >= 1 else len(replicas) - 1

    print(f"Selected {leader_port} as the order service leader")

    # (attempt to) inform all replicas of the leader
    req = bazaar_pb2.SignalOrderLeaderRequest(
        leader_port=int(leader_port)
    )
    for idx in range(len(replicas)):
        order_channel = grpc.insecure_channel(f'{replica_hosts[idx]}:{replicas[idx]}')
        order_stub = bazaar_pb2_grpc.BazaarStub(order_channel)
        _, err = signal_order_leader(req)
        if err != None:
            print(f"Failed to inform replica {replicas[idx]} of the leader replica! ({leader_port})\n{err=}")
        else:
            print(f"Informed replica {replicas[idx]} of the leader replica ({leader_port})")
    
    # once leader has been informed, set the channel and stub as the leader
    order_channel = grpc.insecure_channel(f'{leader_host}:{leader_port}')
    order_stub = bazaar_pb2_grpc.BazaarStub(order_channel)

catalog_channel = grpc.insecure_channel(f'{catalog_host}:50053')
catalog_stub = bazaar_pb2_grpc.BazaarStub(catalog_channel)
def lookup(req):
    try:
        resp = catalog_stub.Lookup(req)
    except grpc.RpcError as error: # if there's an error...
        error_resp = handle_error(error)
        return None, error_resp
    json_resp = { # otherwise return the requested information
        'data': {
            'name': req.stock_name,
            'price': resp.price,
            'num_avail': resp.quantity,
            'volume': resp.volume,
            'max_volume': resp.max_volume
        }
    }
    # add to cache
    if req.stock_name not in g_cache:
        g_cache[req.stock_name] = {
            'price': resp.price,
            'quantity': resp.quantity,
            'num_avail': resp.quantity,
            'volume': resp.volume,
            'max_volume': resp.max_volume
        }
    return json_resp, None


def order(req):
    try:
        resp = order_stub.Order(req)
    except grpc.RpcError as err: # if there's an error...
        error_resp = handle_error(err)
        return None, error_resp
    json_resp = { # otherwise return the requested information
        'data': {
            'transaction_number': resp.transaction_number
        }
    }
    return json_resp, None

def get_orders(req):
    try:
        resp = order_stub.GetOrder(req)
    except grpc.RpcError as err:
        error_resp = handle_error(err)
        return None, error_resp
    if resp.type == bazaar_pb2.Action.SELL:
        action = 'sell'
    elif resp.type == bazaar_pb2.Action.BUY:
        action = 'buy'
    else:
        resp = {
            'error': {
                'code': 404,
                'message': 'Invalid URL'
            }
        }
        return jsonify(resp), 404
    json_resp = {
        'data': {
            'order': req.order_number,
            'name': resp.name,
            'type': action,
            'quantity': resp.quantity
        }
    }
    return json_resp, None

def health_check():
    try:
        resp = order_stub.HealthCheck(bazaar_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty())
    except grpc.RpcError as err: # if there's an error...
        error_resp = {
            'code': err.code(),
            'message': err.details()
        }
        return None, error_resp
    json_resp = { # otherwise return the expected data
        'data': {
            'status': resp.success
        }
    }
    return json_resp, None

def signal_order_leader(req):
    try:
        resp = order_stub.SignalOrderLeader(req)
    except grpc.RpcError as err: # if there's an error...
        error_resp = {
            'code': err.code(),
            'message': err.details()
        }
        return None, error_resp
    json_resp = { # otherwise return the expected data
        'data': {
            'status': resp.success
        }
    }
    return json_resp, None

# generic error handler for gRPC's RpcError
# maps gRPC error codes to HTML codes we can send to the client
def handle_error(err: grpc.RpcError):
    error_resp = {
        'error': {
            'message': err.details() # details beyond the gRPC code passed back this way
        }
    }
    # handle different error codes
    if err.code() == grpc.StatusCode.NOT_FOUND:
        error_resp['error']['code'] = 404
    elif err.code() == grpc.StatusCode.INVALID_ARGUMENT:
        error_resp['error']['code'] = 400
    elif err.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
        error_resp['error']['code'] = 429
    # generic error handling
    else:
        error_resp['error']['code'] = 503
        error_resp['error']['message'] = 'Unknown error'
    return error_resp


# /stocks/<stock_name> - GET
# /orders - POST
# /orders/<order_number> - GET
# if invalid URL, return 404 error
app = Flask(__name__)


# get stockname from query string
# pass stock name to backend
# parse response from backend into JSON object
# {
#     "data": {
#         "name": "GameStart",
#         "price": 15.99,
#         "quantity": 100
#     }
# }
@app.route('/stocks/<stock_name>', methods=['GET'])
def lookup_stock(stock_name):
    # check cache before making gRPC call, if enabled
    if enable_cache == True:
        if stock_name in g_cache:
            stock = g_cache[stock_name]
            resp = {
                'data': {
                    'name': stock_name,
                    'price': stock['price'],
                    'num_avail': stock['quantity'],
                    'volume': stock['volume'],
                    'max_volume': stock['max_volume']
                }
            }
            return jsonify(resp)
    req = bazaar_pb2.LookupRequest(stock_name=stock_name)
    resp, err = lookup(req) # make the call on the client's behalf
    if err != None:
        return jsonify(err), err['error']['code']
    return jsonify(resp)


# request is json in form
# {
#     "name": "GameStart",
#     "quantity": 1,
#     "type": "sell"
# }
# parse JSON request, pass fields to backend
# receive response from backend, send back JSON object in form
# {
#     "data": {
#         "transaction_number": 10
#     }
# } 
@app.route('/orders', methods=['POST'])
def order_stock():
    input_req = request.get_json()
    if input_req['type'] == 'sell':
        action = bazaar_pb2.Action.SELL
    elif input_req['type'] == 'buy':
        action = bazaar_pb2.Action.BUY
    else:
        resp = {
            'code': 404,
            'error': 'Invalid URL'
        }
        return jsonify(resp), 404
    
    req = bazaar_pb2.OrderRequest(
        stock_name=input_req['name'],
        quantity=input_req['quantity'],
        type=action
    )
    
    while True:
        resp, err = order(req)
        if err != None: # if there's an error...
            if err['error']['code'] == 503: # if the error requires electing a new leader
                start_leader_election() # select a new leader
                continue # and retry the operation
            else: # otherwise just return the error to the caller
                return jsonify(err), err['error']['code']
        else: # if there isn't an error we're free to return
            return jsonify(resp)
    

# get order number from query string
# pass order number to backend
# parse response from backend into JSON object
# {
#     "data": {
#         "order_number": 1,
#         "name": "GameStart",
#         "type": "buy",
#         "quantity": 100
#     }
# }
@app.route('/orders/<int:order_number>', methods=['GET'])
def get_order(order_number):
    req = bazaar_pb2.GetOrderRequest(order_number=order_number)
    while True:
        resp, err = get_orders(req)
        if err != None:
            if err['error']['code'] == 503: # if the error requires electing a new leader
                start_leader_election() # select a new leader
                continue # and retry the operation
            else: # otherwise just return the error to the caller
                return jsonify(err), err['error']['code']
        else:
            return jsonify(resp)


# removes stock from cache after update is completed
@app.route('/invalidate_cache', methods=['POST'])
def invalidate_cache():
    # If the data isn't cached there's no need to remove it
    input_req = request.get_json()
    stock_name = input_req['name']

    # if stock isn't in cache, we can just return
    if stock_name not in g_cache:
        return jsonify({})
    # else remove stock from the cache
    stock = g_cache.pop(stock_name)
    # Sanity check
    if stock is None:
        err = {
            'code': 429,
            'message': 'Stock data not found'
        }
        return jsonify(err)
    return jsonify({})


# for invalid URLs
@app.errorhandler(404)
def invalid_url(error):
    return {
        'error': {
            'code': 404,
            'message': 'URL Not Found.'
        }
    }, 404

if __name__ == '__main__':
    start_leader_election()
    app.run(host=frontend_host, debug=False, threaded=True)
