import csv
import json
import os 
import random
import requests
import sys # command line aguments 
import time # benchmarking

# grab environment variable(s)
frontend_host = os.getenv('FRONTEND_HOST', '127.0.0.1')
#frontend_host = "ec2-54-165-251-199.compute-1.amazonaws.com"

# for manual testing
def main():
    if len(sys.argv) != 2:
        print("Error! Usage: python3 client.py <probability>")
        return
    try: # try to convert the argument to a float...
        probability = float(sys.argv[1])
        if (probability < 0) or (probability > 1): # make sure it's in the proper range
            print(f"Error! Argument <probability> must be in the range [0,1]. Erroneous Input: {sys.argv[1]}")
            return
    except ValueError: # and catch the exception if it fails...
        print(f"Error! Argument <probability> must be a number. Erroneous Input: {sys.argv[1]}")
        return

    # open a HTTP connection with frontend
    # randomly look up a stock
    # if quantity > 0, send an order with probability p
    port = 5000
    stock_names = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo', 'Tulsa', 'Haha', 'Funny', 'Humerous', 'Humerus', 'Bookface']
    base_url = f'http://{frontend_host}:{port}'

    # for i in range(10): # configure how many test requests you want to run...
    stock_index = random.randrange(0, 10) # randomly select a stock to interact with
    stock_data = lookup(base_url, stock_names[stock_index])
    order_history = {}
    # stock_data = get_order(base_url, 1)
    if 'error' in stock_data:
        # error displayed within lookup function
        return
    if stock_data['data']['num_avail'] > 0:
        prob = random.random() # grab a random number in [0,1]
        if prob <= probability:
            if random.choice([0, 1]) == 1: # random decide whether we're buying or selling something
                action = 'buy'
            else:
                action = 'sell'
            values = {
                'name': stock_names[stock_index],
                'quantity': random.randrange(0, 10 + 1), # random quantity between 0 and 10, Note that ordering 0 results in an error
                'type': action
            }
            transaction = order(base_url, values)
            if 'error' in transaction:
                # error displayed within order function
                return
            order_history[transaction['data']['transaction_number']] = values
    for trans_num, recorded_order in order_history.items():
        service_order = get_order(base_url, trans_num)
        if 'error' in service_order:
            return
        for key, value in recorded_order.items():
            if recorded_order[key] != service_order['data'][key]:
                print('not same')

# This is how we gathered data for the performance testing portion of the submission
# We are leaving it in for the sake of clarity
def test():
    if len(sys.argv) != 2:
        print("Error! Usage: python3 client.py <probability>")
        return
    try: # try to convert the argument to a float...
        probability = float(sys.argv[1])
        if (probability < 0) or (probability > 1): # make sure it's in the proper range
            print(f"Error! Argument <probability> must be in the range [0,1]. Erroneous Input: {sys.argv[1]}")
            return
    except ValueError: # and catch the exception if it fails...
        print(f"Error! Argument <probability> must be a number. Erroneous Input: {sys.argv[1]}")
        return

    # open a HTTP connection with frontend
    # randomly look up a stock
    # if quantity > 0, send an order with probability p
    port = 5000
    stock_names = ['GameStart', 'FishCo', 'BoarCo', 'MenhirCo', 'Tulsa', 'Haha', 'Funny', 'Humerous', 'Humerus', 'Bookface']
    base_url = f'http://{frontend_host}:{port}'

    order_history = {}
    num_reqs = 100
    lookup_latency = 0
    order_latency = 0
    get_order_latency = 0

    for i in range(num_reqs): # configure how many test requests you want to run...
        stock_index = random.randrange(0, 10) # randomly select a stock to interact with
        start_time = time.time()
        stock_data = lookup(base_url, stock_names[stock_index])
        lookup_latency += time.time() - start_time
        if 'error' in stock_data:
            # error displayed within lookup function
            continue
        if stock_data['data']['num_avail'] > 0:
            prob = random.random() # grab a random number in [0,1]
            if prob <= probability:
                if random.choice([0, 1]) == 1: # random decide whether we're buying or selling something
                    action = 'buy'
                else:
                    action = 'sell'
                values = {
                    'name': stock_names[stock_index],
                    'quantity': random.randrange(0, 10 + 1), # random quantity between 0 and 10, Note that ordering 0 results in an error
                    'type': action
                }
                transaction = order(base_url, values)
                order_latency += time.time() - start_time
                if 'error' in transaction:
                    # error displayed within order function
                    continue
                order_history[transaction['data']['transaction_number']] = values
    
    num_orders = 0
    for trans_num, recorded_order in order_history.items():
        num_orders += 1
        start_time = time.time()
        service_order = get_order(base_url, trans_num)
        get_order_latency += time.time() - start_time
        if 'error' in service_order:
            return
        for key, value in recorded_order.items():
            if recorded_order[key] != service_order['data'][key]:
                print('not same')
    
    with open(f"results_{os. getpid()}.txt", 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([f"Lookup average latency: {(lookup_latency / num_reqs) if num_reqs != 0 else 'N/A'}", \
                f"Order average latency: {(order_latency / num_orders) if num_orders != 0 else 'N/A'}", \
                f"Get Order average latency: {(get_order_latency / num_orders) if num_orders != 0 else 'N/A'}"])
    #print(f"Lookup average latency: {lookup_latency / num_reqs}")
    #print(f"Order average latency: {order_latency / num_reqs}")
    #print(f"Get Order average latency: {get_order_latency / num_reqs}")



# lookup get method
def lookup(base_url, stock_name):
    resp = requests.get(f'{base_url}/stocks/{stock_name}')
    json_resp = json.loads(resp.text)
    print(json_resp) # Display error to client
    return json_resp


#order post method
def order(base_url, values):
    order_url = f'{base_url}/orders'
    resp = requests.post(order_url, json=values)
    json_resp = json.loads(resp.text)
    print(json_resp) # Display error to client
    return json_resp

# order get method
def get_order(base_url, order_number):
    resp = requests.get(f'{base_url}/orders/{order_number}')
    json_resp = json.loads(resp.text)
    print(json_resp) # Display error to client
    return json_resp


if __name__ == '__main__':
    #main()
    test()
