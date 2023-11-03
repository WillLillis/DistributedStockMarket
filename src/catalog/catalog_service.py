from copy import deepcopy
from concurrent import futures
import sys
sys.path.append('..')
sys.path.append('/app')
from proto import bazaar_pb2 # auto-generated grpc file
from proto import bazaar_pb2_grpc # auto-generated grpc file
import grpc # using grpc for client-server communication
import requests
from threading import Lock
import os
import os.path
import csv

# grab environment variable(s)
host = os.getenv('CATALOG_HOST', 'catalog')
frontend_host = os.getenv('FRONTEND_HOST', 'frontend')
frontend_port = os.getenv('FRONTEND_PORT', 5000)

default_stock_volume = 100
default_stock_init_vol = 100
g_market_mtx = Lock()
g_market = {}

# "returns 0 if the name is found, but trading is suspended due to excessive meme stock trading"
# ret: price as a float
def lookup(stock_name: str):
    g_market_mtx.acquire()
    if stock_name not in g_market: # if an invalid stock name is passed
        err = {
            'code': grpc.StatusCode.NOT_FOUND,
            'message': 'Stock not found'
        }
        g_market_mtx.release()
        return None, None, None, None, err
    price = g_market[stock_name]['stock_price'] # otherwise grab the relevant information...
    num_avail = g_market[stock_name]['num_avail']
    volume = g_market[stock_name]['volume']
    max_volume = g_market[stock_name]['max_trading_volume']
    g_market_mtx.release()
    return price, num_avail, volume, max_volume, None # ...and return it

# update global market based on action and quantity, if valid
# returns different grpc errors based on issue (invalid name, invalide quantity, max trading limit)
# returns 0 if successful
def update(stock_name: str, quantity: int, action: bazaar_pb2.Action):
    global g_market

    g_market_mtx.acquire()
    if action == bazaar_pb2.Action.SELL: # handle SELL requests
        g_market[stock_name]['num_avail'] +=  quantity # otherwise the order is valid, enact it
    elif action == bazaar_pb2.Action.BUY: # handle BUY requests
        g_market[stock_name]['num_avail'] -=  quantity # otherwise the order is valid, enact it

    g_market[stock_name]['volume'] += quantity
    write_market_to_disk() # write market contents to disk
    err = invalidate_cache(stock_name)
    if err != None:
        return None, err
    g_market_mtx.release()
    
    return 0, None # return 0 to indicate success

# make http request to frontend to invalidate cache
def invalidate_cache(stock_name):
    json_req = {
        'name': stock_name
    }
    resp = requests.post(f'http://{frontend_host}:{frontend_port}/invalidate_cache', json=json_req)
    # check if successfully invalidated
    if resp.status_code != 200:
        err_resp = {
            'error': {
                'code': 429,
                'message': 'Unable to invalidate cache'
            }
        }
        return err_resp
    return None

# grpc class implementation
class Bazaar(bazaar_pb2_grpc.BazaarServicer):
    def Lookup(self, request, context):
        price, avail_volume, volume, max_volume, err = lookup(request.stock_name)
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return err
        return bazaar_pb2.LookupResponse(
            price=price,
            quantity=avail_volume,
            volume=volume,
            max_volume=max_volume
        )
    def Update(self, request, context):
        ret_status, err = update(request.stock_name, request.quantity, request.action)
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return err
        return bazaar_pb2.UpdateResponse(
            status=ret_status,
        )

def server():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5)) # utilize the builtin threadpool, 5 workers is arbitrary
   bazaar_pb2_grpc.add_BazaarServicer_to_server(Bazaar(), server)
   server.add_insecure_port(f'{host}:50053')
   print("Catalog gRPC starting")
   server.start()
   try:
       server.wait_for_termination() # host the service until the user enters Control+C...
   except KeyboardInterrupt:
        print("Shutting down the catalog service...")

# must be called when you already own the lock!
# for the sake of simplicity (and because our market is relatively small), we'll just rewrite the entire thing every time
def write_market_to_disk(data_base_file_name="market_persistent.csv"):
    global g_market

    field_names = ['stock_name', 'stock_price', 'num_avail', 'max_trading_volume', 'volume']
    if host != 'catalog':
        path = ''
    else:
        if not os.path.exists('/catalog'):
            os.makedirs('/catalog')
        path = '/catalog'

    file_name = os.path.join(path, data_base_file_name) 
    with open(file_name, 'w', newline='') as csv_file: # open with write perissions (overwrite existing contents)
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_writer.writeheader() 
        tmp_dict = {}
        stocks = list(g_market.keys()) # grab the stock names
        for stock in stocks:
            tmp_dict = {} # create a temporary dictionary object with the stock information AND the name
            tmp_dict = deepcopy(g_market[stock])
            tmp_dict['stock_name'] = stock 
            csv_writer.writerow(tmp_dict) # write the dictionary object to the file


# create market csv if it doesnt exist already
def create_market_file(data_base_file_name: str = "market_persistent.csv"):
    # initialize the global structure with our arbitrary starting values
    default_stock_volume = 100
    default_stock_init_vol = 100
    global g_market
    global g_market_mtx

    g_market_mtx.acquire()
    g_market = {
        'GameStart': {
            'stock_price': 100000.0, # arbitrary starting price
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500, # arbitrary max trading volume, configured at start time
            'volume': default_stock_volume, # tracks total trade volume for this stock
        },
        'FishCo': {
            'stock_price': 20.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'BoarCo': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'MenhirCo': {
            'stock_price': 175.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'Tulsa': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'Haha': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'Funny': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'Humerous': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'Humerus': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
        'Bookface': {
            'stock_price': 100.0,
            'num_avail' : default_stock_init_vol, # amount of the stock available to trade
            'max_trading_volume': 500,
            'volume': default_stock_volume,
        },
    }
    # must be called only when you own the lock
    write_market_to_disk(data_base_file_name)
    g_market_mtx.release()

# returns True on success, False on failure
def load_market_from_disk(data_base_file_name: str) -> bool:
    # check if the file is there - local vs docker
    if host != 'catalog': # if we're running locally
        file_list = os.listdir(os.getcwd())
        if data_base_file_name not in file_list:
            return False
        path = ''
    else: # we're running in a docker container
        if not os.path.exists(f'/catalog/{data_base_file_name}'):
            return False
        path = '/catalog'

    # no one should be accessing the market but we'll grab the lock just to be sure...
    g_market_mtx.acquire()

    # if the file exists open it
    file_name = os.path.join(path, data_base_file_name)
    with open(file_name) as raw_data_file: 
        data_reader = csv.reader(raw_data_file)
        market_data = list(data_reader)
    market_data.pop(0) # don't need the csv header
    
    for stock_entry in market_data:
        g_market[stock_entry[0]] = { # stock name is the first entry in a given row
        'stock_price': float(stock_entry[1]), # stock price
        'num_avail' : int(stock_entry[2]), # amount of the stock available to trade
        'max_trading_volume': int(stock_entry[3]), # arbitrary max trading volume
        'volume': int(stock_entry[4]), # tracks total trade volume for this stock
        }
    g_market_mtx.release()
    return True # return True to indicate success

# initialize global market
def catalog_service_init():
    # initialize the globals
    global g_market_mtx 
    g_market_mtx = Lock()
    global g_market 
    g_market = {}

    # read from csv into local market
    # if no csv is detected in the expected location (cwd most likely), create one 
    if load_market_from_disk("market_persistent.csv") == False:
        print(f"Database file not found. Creating new database storage with default values...")
        create_market_file()

if __name__ == "__main__":
    catalog_service_init()
    server()
