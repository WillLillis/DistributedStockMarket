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
catalog_host = os.getenv('CATALOG_HOST', 'catalog')
port = 5000
stock_names = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo']
base_url = f'http://{host}:{port}'

catalog_channel = grpc.insecure_channel(f'{catalog_host}:50053')
catalog_stub = bazaar_pb2_grpc.BazaarStub(catalog_channel)

# testing framework for lookup functions
# tests lookup with incorrect and correct name
# tests gRPC lookup call with incorrect and correct name
class Test_Lookup(unittest.TestCase):
    def test_lookup(self):
        for stock_name in stock_names:
            resp = requests.get(f'{base_url}/stocks/{stock_name}')
            json_resp = json.loads(resp.text)
            self.assertTrue('data' in json_resp)
            self.assertEqual(json_resp['data']['name'], stock_name)

    def test_stock_not_found(self):
        expected_resp = {
            'error': {
                'code': 404,
                'message': 'Stock not found'
            }
        }
        resp = requests.get(f'{base_url}/stocks/FakeStockName')
        json_resp = json.loads(resp.text)
        self.assertEqual(json_resp, expected_resp)

    def test_grpc_lookup(self):
        # lookup with invalid name first
        req = bazaar_pb2.LookupRequest(stock_name='FakeName')
        try:
            resp = catalog_stub.Lookup(req)
        except grpc.RpcError as error:
            self.assertEqual(error.code(), grpc.StatusCode.NOT_FOUND)

        # now test with valid name
        req = bazaar_pb2.LookupRequest(stock_name=stock_names[0])
        try:
            resp = catalog_stub.Lookup(req)
        except grpc.RpcError as error:
            self.assertIsNone(error)

        self.assertEqual(type(resp), bazaar_pb2.LookupResponse)
        self.assertEqual(type(resp.price), float)
        self.assertEqual(type(resp.quantity), int)
        self.assertGreater(resp.price, 0)
        self.assertGreater(resp.quantity, 0)

if __name__ == '__main__':
    unittest.main()