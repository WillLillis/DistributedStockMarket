import grpc
import json
import os
import requests
import sys
sys.path.append('..')
import unittest

from proto import bazaar_pb2 # auto-generated grpc file
from proto import bazaar_pb2_grpc # auto-generated grpc file


host = '127.0.0.1'
order_host = os.getenv('ORDER_HOST', 'order')
port = 5000
stock_names = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo']
base_url = f'http://{host}:{port}'
replicas = [50054, 50055, 50056]

order_channel = grpc.insecure_channel(f'{order_host}:50056')
order_stub = bazaar_pb2_grpc.BazaarStub(order_channel)

# testing framework for lookup functions
# test order with correct information, trigger all possible errors
# test gRPC order (which calls update in catalog service) with 
# correct and incorrect information
class Test_Order(unittest.TestCase):
    def test_order(self):
        for stock_name in stock_names:
            values = {
                'name': stock_name,
                'quantity': 1,
                'type': 'buy'
            }
            order_url = f'{base_url}/orders'
            resp = requests.post(order_url, json=values)
            json_resp = json.loads(resp.text)
            self.assertTrue('data' in json_resp)
            self.assertTrue('transaction_number' in json_resp['data'])

    def test_get_order(self):
        order_number = 2
        order_url = f'{base_url}/orders/{order_number}'
        resp = requests.get(order_url)
        json_resp = json.loads(resp.text)
        self.assertTrue('data' in json_resp)
        self.assertEqual(json_resp['data']['order'], order_number)

    def test_stock_not_found(self):
        expected_resp = {
            'error': {
                'code': 404,
                'message': 'Stock not found'
            }
        }
        values = {
            'name': 'FakeStockName',
            'quantity': 1,
            'type': 'buy'
        }
        order_url = f'{base_url}/orders'
        resp = requests.post(order_url, json=values)
        json_resp = json.loads(resp.text)
        self.assertEqual(json_resp, expected_resp)

    def test_invalid_trade_quantity(self):
        expected_resp = {
            'error': {
                'code': 400,
                'message': 'Invalid trade quantity'
            }
        }
        values = {
            'name': stock_names[0],
            'quantity': -20,
            'type': 'buy'
        }
        order_url = f'{base_url}/orders'
        resp = requests.post(order_url, json=values)
        json_resp = json.loads(resp.text)
        self.assertEqual(json_resp, expected_resp)

    def test_trade_past_max_trade_volume(self):
        actions = ['buy', 'sell']
        expected_resp = {
            'error': {
                'code': 429,
                'message': 'Trade exceeds max trading volume'
            }
        }
        for action in actions:
            values = {
                'name': stock_names[0],
                'quantity': 1000,
                'type': action
            }
            order_url = f'{base_url}/orders'
            resp = requests.post(order_url, json=values)
            json_resp = json.loads(resp.text)
            self.assertEqual(json_resp, expected_resp)

    def test_insufficient_volume(self):
        expected_resp = {
            'error': {
                'code': 429,
                'message': 'Insufficient volume available'
            }
        }
        values = {
            'name': stock_names[0],
            'quantity': 101,
            'type': 'buy'
        }
        order_url = f'{base_url}/orders'
        resp = requests.post(order_url, json=values)
        json_resp = json.loads(resp.text)
        self.assertEqual(json_resp, expected_resp)

    def test_grpc_order(self):
        # first test for error
        req = bazaar_pb2.OrderRequest(
            stock_name='FakeStockName',
            quantity=8,
            type=bazaar_pb2.Action.BUY
        )
        try:
            resp = order_stub.Order(req)
        except grpc.RpcError as err:
            self.assertEqual(err.code(), grpc.StatusCode.NOT_FOUND)

        # now test for success
        req = bazaar_pb2.OrderRequest(
            stock_name=stock_names[0],
            quantity=8,
            type=bazaar_pb2.Action.BUY
        )
        try:
            resp = order_stub.Order(req)
        except grpc.RpcError as err:
            self.assertIsNone(err)

        self.assertEqual(type(resp), bazaar_pb2.OrderResponse)
        self.assertEqual(type(resp.transaction_number), int)
        self.assertGreaterEqual(resp.transaction_number, 0)

    def test_grpc_get_order(self):
        # first test for error
        req = bazaar_pb2.GetOrderRequest(
            order_number=1000
        )
        try:
            resp = order_stub.GetOrder(req)
        except grpc.RpcError as err:
            self.assertEqual(err.code(), grpc.StatusCode.INVALID_ARGUMENT)

        # now test for success
        req = bazaar_pb2.GetOrderRequest(
            order_number=1
        )
        try:
            resp = order_stub.GetOrder(req)
        except grpc.RpcError as err:
            self.assertIsNone(err)

        self.assertEqual(type(resp), bazaar_pb2.GetOrderResponse)
        self.assertEqual(type(resp.order_number), int)
        self.assertEqual(resp.order_number, 1)

    def test_grpc_health_check(self):
        try:
            resp = order_stub.HealthCheck(bazaar_pb2_grpc.google_dot_protobuf_dot_empty__pb2.Empty())
        except grpc.RpcError as err:
            self.assertIsNone(err)

        self.assertEqual(type(resp), bazaar_pb2.HealthCheckResponse)
        self.assertEqual(type(resp.success), bool)
        self.assertEqual(resp.success, True)

    def test_grpc_signal_order_leader(self):
        # test for each replica to mimic real flow
        for replica in replicas:
            replica_channel = grpc.insecure_channel(f'{order_host}:{replica}')
            replica_stub = bazaar_pb2_grpc.BazaarStub(replica_channel)
            req = bazaar_pb2.SignalOrderLeaderRequest(leader_port=replica)
            try:
                resp = replica_stub.SignalOrderLeader(req)
            except grpc.RpcError as err:
                self.assertIsNone(err)

            self.assertEqual(type(resp), bazaar_pb2.SignalOrderLeaderResponse)
            self.assertEqual(type(resp.success), bool)
            self.assertEqual(resp.success, True)

    def test_grpc_follower_update(self):
        # first do a regular order to mimic real flow
        req = bazaar_pb2.OrderRequest(
            stock_name=stock_names[2],
            quantity=1,
            type=bazaar_pb2.Action.BUY
        )
        try:
            resp = order_stub.Order(req)
        except grpc.RpcError as err:
            self.assertIsNone(err)

        self.assertEqual(type(resp), bazaar_pb2.OrderResponse)
        self.assertEqual(type(resp.transaction_number), int)
        self.assertGreaterEqual(resp.transaction_number, 0)

        # then update replicas to mimic real flow
        follower_replicas = [
            {
                'host': host,
                'port': 50054
            },
            {
                'host': host,
                'port': 50055
            },
        ]
        for replica in follower_replicas:
            replica_channel = grpc.insecure_channel(f"{replica['host']}:{replica['port']}")
            replica_stub = bazaar_pb2_grpc.BazaarStub(replica_channel)
            req = bazaar_pb2.FollowerUpdateRequest(stock_name=stock_names[2], quantity=1, type=bazaar_pb2.Action.BUY)
            try:
                resp = replica_stub.FollowerUpdate(req)
            except grpc.RpcError as err:
                self.assertIsNone(err)

            self.assertEqual(type(resp), bazaar_pb2.FollowerUpdateResponse)
            self.assertEqual(type(resp.success), bool)
            self.assertEqual(resp.success, True)

    def test_grpc_order_log_recover(self):
        # we want to contact the leader to get the most updated log
        replica_channel = grpc.insecure_channel(f"{host}:50056")
        replica_stub = bazaar_pb2_grpc.BazaarStub(replica_channel)

        log_file_name = "transaction_log_50056.csv"
        if 'order' in order_host:
            path = '/order'
        else:
            path = '../order'

        file_name = os.path.join(path, log_file_name)

        with open(file_name, 'r') as log_file:
            content = log_file.readlines()
            num_rows = len(content)

        # we then call order log recover for all the logs
        req = bazaar_pb2.OrderLogRecoverRequest(transaction_number=-1)
        try:
            resp = replica_stub.OrderLogRecover(req)
        except grpc.RpcError as err:
            self.assertIsNone(err)
        
        self.assertEqual(type(resp), bazaar_pb2.OrderLogRecoverResponse)
        # check for num_rows - 1 since we don't want to count the categories row
        self.assertEqual(len(resp.entries), num_rows-1)

if __name__ == '__main__':
    unittest.main()