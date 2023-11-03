from ast import Pass
from concurrent import futures
import csv
import os
import sys
from threading import Lock
sys.path.append('..')
sys.path.append('/app')
from proto import bazaar_pb2 # auto-generated grpc file
from proto import bazaar_pb2_grpc # auto-generated grpc file
import grpc # using grpc for client-server communication

# grab environment variable(s)
order_host = os.getenv('ORDER_HOST', 'order')
catalog_host = os.getenv('CATALOG_HOST', 'catalog')
replica_host_1 = os.getenv('REPLICA_HOST_1', '127.0.0.1')
replica_host_2 = os.getenv('REPLICA_HOST_2', '127.0.0.1')

# hardcoded ports we are using for replicas
ports = [50054, 50055, 50056]
order_port = os.getenv('ORDER_PORT', 50054)
ports.remove(int(order_port))
replica_port_1 = ports[0]
replica_port_2 = ports[1]

g_restart = False if (os.getenv('RESTART') == None) else True # check if the RESTART environment variable is set

g_leader = False
g_leader_port = -1

g_transaction_num = 0
g_log_mtx = Lock()

# create log entry to store in csv
# return transaction number if successful
def log_transaction(
    stock_name: str,
    quantity: int,
    action: bazaar_pb2.Action,
    transaction_num = -1
) -> int:
    global g_transaction_num
    global g_log_mtx

    log_file_name = f"transaction_log_{order_port}.csv"
    file_list = os.listdir(os.getcwd())
    
    g_log_mtx.acquire() # acquire the lock protecting the log and g_transaction_num
    # Prepare the log entry we're about to write to the file
    log_entry = list()
    if transaction_num == -1:
        log_entry.append(g_transaction_num)
    else:
        log_entry.append(transaction_num)
    log_entry.append(stock_name)
    if action == bazaar_pb2.Action.BUY:
        log_entry.append("BUY")
    elif action == bazaar_pb2.Action.SELL:
        log_entry.append("SELL")

    log_entry.append(quantity)

    # check if the file is there
    file_exists = True
    if 'order' in order_host:
        if not os.path.exists(f'/order/{log_file_name}'):
            file_exists = False
        path = '/order'
    else:
        file_list = os.listdir(os.getcwd())
        if log_file_name not in file_list:
            file_exists = False
        path = ''

    file_name = os.path.join(path, log_file_name)
    
    # check if the file is there
    if not file_exists: # if the log doesn't exist yet, open with write permissions
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Transaction Number", "Stock Name", "Order Type", "Quantity"])
            csv_writer.writerow(log_entry)
    else: # if the log does exist, open with append permissions
        with open(file_name, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(log_entry)
    tmp_trans_num = g_transaction_num # grab the current transaction number before incrementing
    if transaction_num == -1:
        g_transaction_num += 1 # increment
    else:
        g_transaction_num = transaction_num + 1
    g_log_mtx.release()
    return tmp_trans_num 

# stub to access catalog service for update and lookup
channel = grpc.insecure_channel(f'{catalog_host}:50053')
stub = bazaar_pb2_grpc.BazaarStub(channel)
def update(req):
    try:
        resp = stub.Update(req)
    except grpc.RpcError as err: # if there's an error...
        error_resp = {
            'code': err.code(),
            'message': err.details()
        }
        return None, error_resp
    json_resp = { # otherwise return the expected data
        'data': {
            'status': resp.status
        }
    }
    return json_resp, None

def lookup(req):
    try:
        resp = stub.Lookup(req)
    except grpc.RpcError as err: # if there's an error...
        error_resp = {
            'code': err.code(),
            'message': err.details()
        }
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
    return json_resp, None

# helper method to make call to lookup, check if the order if valid, and if so call update
def order(stock_name: str, quantity: int, action: bazaar_pb2.Action):
    # Check for valid trading quantity
    if quantity <= 0:
        err = {
                'code': grpc.StatusCode.INVALID_ARGUMENT,
                'message': 'Invalid trade quantity'
            }
        return None, err
    req = bazaar_pb2.LookupRequest(stock_name=stock_name)
    resp, err = lookup(req)
    if err != None: # if there's an error...
        return None, err # return it to the caller and DONT log the transaction
    resp = resp['data'] # unwrap the response object
    # Make sure we won't exceed the maximum trading volume
    if quantity + resp['volume'] > resp['max_volume']:
        err = {
                'code': grpc.StatusCode.RESOURCE_EXHAUSTED,
                'message': 'Trade exceeds max trading volume'
            }
        return None, err
    # no special checks for selling action (yet)
    if action == bazaar_pb2.Action.SELL:
        pass
    # if we're buying, making sure there's enough to fill the order
    elif action == bazaar_pb2.Action.BUY:
        if quantity > resp['num_avail']:
            # if this trade exceeds it, release the lock and return an error
            err = {
                'code': grpc.StatusCode.RESOURCE_EXHAUSTED,
                'message': 'Insufficient volume available'
            }
            return None, err
    # no error? we're fine to proceed with the update request
    # realistically we should hold a lock this entire time
        # as things can change in between the lookup and update calls
        # but Dr. Shenoy said during lecture that this wasn't necessary for the assignment
    req = bazaar_pb2.UpdateRequest(stock_name=stock_name, quantity=quantity, action=action)
    resp, err = update(req)
    if err != None: # if there's an error...
        return None, err # return it to the caller and DONT log the transaction
    trans_num = log_transaction(stock_name, quantity, action) # otherwise add it to the log...
    # on successful trade, propogate info to replicas
    _, err = update_replicas(stock_name, quantity, action, trans_num)
    if err != None:
        return None, err
    return trans_num, None # and return the corresponding transaction number

# sent from leader
# updates replicas to add transaction to log file after successful leader update
def update_replicas(stock_name: str, quantity: int, action: bazaar_pb2.Action, trans_num: int):
    replicas = [
        {
            'host': replica_host_1 if replica_host_1 != '127.0.0.1' else order_host,
            'port': replica_port_1
        },
        {
            'host': replica_host_2 if replica_host_2 != '127.0.0.1' else order_host,
            'port': replica_port_2
        },
    ]

    replica_errors = {}
    for replica in replicas:
        replica_channel = grpc.insecure_channel(f"{replica['host']}:{replica['port']}")
        replica_stub = bazaar_pb2_grpc.BazaarStub(replica_channel)
        req = bazaar_pb2.FollowerUpdateRequest(stock_name=stock_name, \
            quantity=quantity, type=action, transaction_number=trans_num)
        try:
            resp = replica_stub.FollowerUpdate(req)
        except grpc.RpcError as err: # if there's an error...
            error_resp = {
                'code': err.code(),
                'message': err.details()
            }
            replica_errors[replica['port']] = error_resp
            continue

    # unique error handling because we dont want to return in the middle of the loop
    if len(replica_errors) == len(replicas):
        # they all errored, so we want to return an error
        error_resp = {
            'code': replica_errors[replicas[0]['port']],
            'message': 'Failed to update all replicas'
        }
        return None, error_resp
    else: # otherwise at least one succeeded, good to proceed
        for port, error in replica_errors.items():
            print(f'Failed to update replica {port} with error {error["code"]}: {error["message"]}')
    return None, None

# open this replica's csv, (make sure to grab the lock)
# look for the request transaction number log
# if it can be found, great
# if not, return an error
def get_order(transaction_number: int):
    global g_log_mtx
    
    log_file_name = f"transaction_log_{order_port}.csv"
    if 'order' in order_host:
        path = '/order'
    else:
        path = ''

    file_name = os.path.join(path, log_file_name)

    g_log_mtx.acquire()
    with open(file_name, 'r', newline='') as csv_file:
        data_reader = csv.reader(csv_file)
        log = list(data_reader)
    g_log_mtx.release()
    found_entry = False
    order = []
    for index in range(1, len(log)):
        if int(log[index][0]) == transaction_number:
            found_entry = True
            order = log[index]
            break
    if found_entry == True:
        return {
            'order_number': int(order[0]),
            'stock_name': order[1],
            'type': order[2],
            'quantity': int(order[3])
        }, None
    else:
        err = {
                'code': grpc.StatusCode.INVALID_ARGUMENT,
                'message': 'Invalid transaction number'
            }
        return None, err

def health_check():
    return True, None

def signal_order_leader(leader_port: int):
    global g_leader
    global g_leader_port

    g_leader_port = leader_port
    if leader_port == order_port:
        g_leader = True
    else:
        g_leader = False

    return True, None

def follower_update(stock_name: str, quantity: int, action: bazaar_pb2.Action, transaction_number: int):
    log_transaction(stock_name, quantity, action, transaction_num=transaction_number)
    return True, None

def order_log_recover(transaction_number: int):
    global g_log_mtx
    log_file_name = f"transaction_log_{order_port}.csv"
    if 'order' in order_host:
        path = '/order'
    else:
        path = ''

    file_name = os.path.join(path, log_file_name)

    missing_logs = []

    g_log_mtx.acquire()
    with open(file_name, 'r', newline='') as csv_file:
        data_reader = csv.reader(csv_file)
        log = list(data_reader)
    g_log_mtx.release()
    for index in range(1, len(log)): # skip column labels in row 0
        if transaction_number < int(log[index][0]):
            trans_tmp = bazaar_pb2.OrderLogRecoverResponse.OrderLogRecoverEntry(
                transaction_number = int(log[index][0]),
                stock_name = log[index][1],
                type = bazaar_pb2.Action.BUY if log[index][2] == "BUY" else bazaar_pb2.Action.SELL, # more error checking here?
                quantity = int(log[index][3])
                )
            missing_logs.append(trans_tmp)

    resp = bazaar_pb2.OrderLogRecoverResponse(entries=missing_logs)
    return resp, None

# grpc class implementation
class Bazaar(bazaar_pb2_grpc.BazaarServicer):
    def Order(self, request, context):
        transaction_number, err = order(request.stock_name, request.quantity, request.type)
        if err != None: # if there's an error...
            context.set_code(err['code']) # use gRPC's builtin error passing 
            context.set_details(err['message'])
            return None
        return bazaar_pb2.OrderResponse( # otherwise return the transaction number to the stub
            transaction_number=transaction_number,
        )
    
    def GetOrder(self, request, context):
        resp, err = get_order(request.order_number)
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return None
        return bazaar_pb2.GetOrderResponse(
            order_number=request.order_number,
            name=resp['stock_name'],
            type=resp['type'],
            quantity=resp['quantity']
        )
    
    def HealthCheck(self, request, context):
        resp, err = health_check()
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return None
        return bazaar_pb2.HealthCheckResponse(
            success=resp
        )

    def SignalOrderLeader(self, request, context):
        resp, err = signal_order_leader(request.leader_port)
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return None
        return bazaar_pb2.SignalOrderLeaderResponse(
            success=resp
        )
    
    def FollowerUpdate(self, request, context):
        resp, err = follower_update(request.stock_name, request.quantity, request.type, request.transaction_number)
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return None
        return bazaar_pb2.FollowerUpdateResponse(
            success=resp
        )
    def OrderLogRecover(self, request, context):
        resp, err = order_log_recover(request.transaction_number)
        if err != None:
            context.set_code(err['code'])
            context.set_details(err['message'])
            return None
        return resp

# Performs some cleanup on the transaction log file if necessary
# Contacts replicas and receives missing transactions logs 
    # (anything with a transaction number greater than its highest recorded transaction)
def recover():
    global g_log_mtx

    log_file_name = f"transaction_log_{order_port}.csv"
    if 'order' in order_host:
        path = '/order'
    else:
        path = ''

    file_name = os.path.join(path, log_file_name)

    replicas = [
        {
            'host': replica_host_1 if replica_host_1 != '127.0.0.1' else order_host,
            'port': replica_port_1,
        },
        {
            'host': replica_host_2 if replica_host_2 != '127.0.0.1' else order_host,
            'port': replica_port_2,
        },
    ]

    g_log_mtx.acquire()
    #trans_log_file_clean(log_file_name)
    with open(file_name, 'r', newline='') as csv_file:
        data_reader = csv.reader(csv_file)
        log = list(data_reader)
    
    # dealing with extra lines at the end of the file...
    extra_lines = False
    if len(log) > 0:
        while len(log[-1]) == 0:
            extra_lines = True
            log.pop(-1)
            if len(log) == 0:
                break
    
    # rewrite the file without the extra lines
    if extra_lines == True:
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for entry in log:
                csv_writer.writerow(entry)

    last_trans_num = -1
    if len(log) == 1:
        pass
    else:
        for index in range(1, len(log)): # skip column labels in row 0
            last_trans_num = int(log[index][0]) if int(log[index][0]) > last_trans_num else last_trans_num
    
    update_success = False
    for replica in replicas:
        replica_channel = grpc.insecure_channel(f"{replica['host']}:{replica['port']}")
        replica_stub = bazaar_pb2_grpc.BazaarStub(replica_channel)
        req = bazaar_pb2.OrderLogRecoverRequest(transaction_number=last_trans_num)
        try:
            resp = replica_stub.OrderLogRecover(req)
            update_success = True
            break
        except grpc.RpcError as err: # if there's an error...
            print(f"Recovery Error! Failed to update the transaction log with replica {replica['host']:replica['port']}!")
            continue # if a replica errors out, we can still try another one
    g_log_mtx.release()
    if update_success == True:
        for entry in resp.entries:
            log_transaction(entry.stock_name, entry.quantity, entry.type, transaction_num=entry.transaction_number)
        print("Successfully recovered the transaction log!")
        return True
    else:
        print("Failed to recover the transaction log!")
        return False

# start order service
def server():
   global g_log_mtx
   global g_transaction_num

   server = grpc.server(futures.ThreadPoolExecutor(max_workers=5)) # utilize the builtin threadpool, 5 workers is arbitrary
   bazaar_pb2_grpc.add_BazaarServicer_to_server(Bazaar(), server)
   server.add_insecure_port(f'{order_host}:{order_port}')
   print(f"Order gRPC starting ({order_host}:{order_port})")
   server.start()
   
   if g_restart == True:
       if recover() == False:
           print("Failed to recover the transaction log from the order replicas! Shutting down this replica")
           return
       else: # recovery succeeded! clean up the transaction log before starting
           g_log_mtx.acquire()
           g_transaction_num = trans_log_file_clean(f"transaction_log_{order_port}.csv") + 1
           g_log_mtx.release()
   try:
        server.wait_for_termination() # host the service until the user enters Control+C...
   except KeyboardInterrupt:
        print("Shutting down the order service...")

# re-orders log by transaction number if found to be out of order
# if there are empty lines at the end of the file, it removes them
# should only be called when the caller already owns the g_log_mtx lock
# returns largest transaction number in the file for the convenience of the caller
def trans_log_file_clean(log_file_name: str):
    if 'order' in order_host:
        path = '/order'
    else:
        path = ''

    file_name = os.path.join(path, log_file_name)
    
    with open(file_name, 'r', newline='') as csv_file:
        data_reader = csv.reader(csv_file)
        log = list(data_reader)
    column_labels = log.pop(0)

    in_order = True
    empty_entries = False
    has_dups = False
    dups = {}
    last_num = float('-inf')
    
    for entry in log:
        if len(entry) != 0: # blank lines at the end of the file lead to empty entries that can be problematic
            entry[0] = int(entry[0])
            if entry[0] < last_num:
                in_order = False
            if entry[0] in dups:
                has_dups = True
                dups[entry[0]] += 1
            else:
                dups[entry[0]] = 1
            last_num = entry[0]
        else:
            empty_entries = True

    if empty_entries == True:
        while len(log[-1]) == 0: # Remove empty entries 
            log.pop(-1)
            if len(log) == 0:
                break

    if len(log) == 0: # if there aren't any entries, no need to clean them
        return -1

    dups = {key:val for key, val in dups.items() if val != 1} # remove all entries with value '1'

    if in_order == False: # sort the log if it's out of order
        log.sort(key=lambda x: x[0]) # sort according to transaction number in column 0
    for num in dups: # for all entries with 1 or more duplicates
        for index in range(len(log)): 
                if log[index][0] == num: # find where the duplicates start (the list is sorted, they're all adjacent)
                    for _ in range(1, dups[num]): # remove the duplicates
                        log.pop(index)
                    break
    if (empty_entries == True) or (in_order == False) or (has_dups == True): # rewrite the files if there's fixes
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(column_labels)
            for entry in log:
                csv_writer.writerow(entry)

    return log[-1][0] # return the highest recorded transaction number

# create transaction log csv if not found
# else read from log 
def order_service_init():
    global g_transaction_num
    global g_log_mtx
    transaction_log_file_name = f"transaction_log_{order_port}.csv"

    # check if the file is there
    file_exists = True
    if "order" in order_host:
        if not os.path.exists(os.path.join('/order', transaction_log_file_name)):
            file_exists = False
        path = '/order'
    else:
        file_list = os.listdir(os.getcwd())
        if transaction_log_file_name not in file_list:
            file_exists = False
        path = ''
    file_name = os.path.join(path, transaction_log_file_name)
    g_log_mtx.acquire()
    # if file does not exist, create it
    if not file_exists:
        g_transaction_num = 0 # if there's no previous log, the transaction number starts at 0
        print("No previous transaction log found. Creating one")
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Transaction Number", "Stock Name", "Order Type", "Quantity"])
    else: # otherwise we'll base our transaction number off of the log
        with open(file_name, 'r') as raw_data_file: 
            data_reader = csv.reader(raw_data_file)
            transaction_log = list(data_reader)
        if len(transaction_log) <= 1: # check for an empty log (just column headers)
            print(f"Previous transaction log found, but is empty. Starting with Transaction ID#{g_transaction_num}")
            g_transaction_num = 0
        else: # clean up the file if necessary and grab the last entry in the log and base the transaction number off of that
            g_transaction_num = trans_log_file_clean(file_name) + 1
            print(f"Previous transaction log found, starting with Transaction ID #{g_transaction_num}")
    g_log_mtx.release()


if __name__ == "__main__":
    order_service_init()
    server()