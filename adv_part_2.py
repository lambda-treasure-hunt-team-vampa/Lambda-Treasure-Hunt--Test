from decouple import config
import requests
import json
import random
from time import sleep, time
import os
import hashlib
import io
from contextlib import redirect_stdout

from cpu import *

dirname = os.path.dirname(os.path.abspath(__file__))
movement_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
my_name = config('MY_NAME')


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Traversal_Graph_Complete:
    def __init__(self):
        self.vertices = {}

    def get_neighbors(self, room_id):
        return set(self.vertices[room_id]['exits'].values())

    def bfs(self, init_response, key_to_search, value_to_search):
        # Create a queue/stack as appropriate
        queue = Queue()
        # Put the starting point in that
        # Enstack a list to use as our path
        queue.enqueue([init_response['room_id']])
        # Make a set to keep track of where we've been
        visited = set()
        # While there is stuff in the queue/stack
        while queue.size() > 0:
        #   Pop the first item
            path = queue.dequeue()
            vertex = path[-1]
        #   If not visited
            if vertex not in visited:
                if key_to_search == 'room_id':
                    if vertex == value_to_search:
                        # Do the thing!
                        directions = []
                        for i in range(1, len(path)):
                            for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                if traversal_graph.vertices[path[i - 1]]['exits'][
                                    option] == path[i]:
                                    directions.append(option)
                        return(directions)
                    visited.add(vertex)
                if key_to_search == 'title':
                    if self.vertices[vertex][key_to_search] == value_to_search:
                        # Do the thing!
                        directions = []
                        for i in range(1, len(path)):
                            for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                if traversal_graph.vertices[path[i - 1]]['exits'][
                                    option] == path[i]:
                                    directions.append(option)
                        return(directions)
                    visited.add(vertex)
                if key_to_search in ['items', 'description']:
                    if value_to_search in self.vertices[vertex][key_to_search]:
                        # Do the thing!
                        directions = []
                        for i in range(1, len(path)):
                            for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                if traversal_graph.vertices[path[i - 1]]['exits'][
                                    option] == path[i]:
                                    directions.append(option)
                        return(directions)
                    visited.add(vertex)
        #       For each edge in the item
                for next_vert in self.get_neighbors(vertex):
                # Copy path to avoid pass by reference bug
                    new_path = list(path) # Make a copy of path rather than reference
                    new_path.append(next_vert)
                    queue.enqueue(new_path)


def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    # init_endpoint = "http://127.0.0.1:8000/api/adv/init/"
    init_headers = {"Authorization": f"Token {config('SECRET_KEY')}"}
    # init_headers = {"Authorization": f"Token {config('TEST_KEY')}"}
    init_response = json.loads(requests.get(init_endpoint, headers=init_headers).content)

    sleep(init_response['cooldown'])

    return init_response

def make_wise_move(move, init_response, traversal_graph_complete):
    move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    # move_endpoint = "http://127.0.0.1:8000/api/adv/move/"
    move_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # move_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    next_room_id = traversal_graph_complete.vertices[init_response['room_id']]['exits'][move]
    move_payload = {"direction": move, "next_room_id": str(next_room_id)}
    move_response = json.loads(requests.post(move_endpoint, data=json.dumps(move_payload), headers=move_headers).content)

    sleep(move_response['cooldown'])

    return move_response

def examine_item(item):
    examine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/"
    # examine_endpoint = "http://127.0.0.1:8000/api/adv/examine/"
    examine_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # examine_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    examine_payload = {"name": item}
    examine_response = json.loads(requests.post(examine_endpoint, data=json.dumps(examine_payload), headers=examine_headers).content)

    sleep(examine_response['cooldown'])

    return examine_response

def take_item(item):
    take_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/"
    # take_endpoint = "http://127.0.0.1:8000/api/adv/take/"
    take_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # take_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    take_payload = {"name": item}
    take_response = json.loads(requests.post(take_endpoint, data=json.dumps(take_payload), headers=take_headers).content)

    sleep(take_response['cooldown'])

    return take_response

def drop_item(item):
    drop_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/"
    # drop_endpoint = "http://127.0.0.1:8000/api/adv/drop/"
    drop_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # drop_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    drop_payload = {"name": item}
    drop_response = json.loads(requests.post(drop_endpoint, data=json.dumps(drop_payload), headers=drop_headers).content)

    sleep(drop_response['cooldown'])

    return drop_response

def sell_item(item):
    sell_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/"
    # sell_endpoint = "http://127.0.0.1:8000/api/adv/sell/"
    sell_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # sell_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    sell_payload = {"name": item, "confirm": "yes"}
    sell_response = json.loads(requests.post(sell_endpoint, data=json.dumps(sell_payload), headers=sell_headers).content)

    sleep(sell_response['cooldown'])

    return sell_response

def check_status():
    status_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/"
    # status_endpoint = "http://127.0.0.1:8000/api/adv/status/"
    status_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # status_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    status_response = json.loads(requests.post(status_endpoint, headers=status_headers).content)

    sleep(status_response['cooldown'])

    return status_response

def change_name(name):
    change_name_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/"
    # change_name_endpoint = "http://127.0.0.1:8000/api/adv/change_name/"
    change_name_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # change_name_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    change_name_payload = {"name": name, "confirm": "aye"}
    change_name_response = json.loads(requests.post(change_name_endpoint, data=json.dumps(change_name_payload), headers=change_name_headers).content)

    sleep(change_name_response['cooldown'])

    return change_name_response

def pray():
    pray_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/"
    # pray_endpoint = "http://127.0.0.1:8000/api/adv/pray/"
    pray_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # pray_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    pray_response = json.loads(requests.post(pray_endpoint, headers=pray_headers).content)

    sleep(pray_response['cooldown'])

    return pray_response

def get_last_proof():
    last_proof_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/"
    # last_proof_endpoint = "http://127.0.0.1:8000/api/bc/last_proof/"
    last_proof_headers = {"Authorization": f"Token {config('SECRET_KEY')}"}
    # last_proof_headers = {"Authorization": f"Token {config('TEST_KEY')}"}
    last_proof_response = json.loads(requests.get(last_proof_endpoint, headers=last_proof_headers).content)

    sleep(last_proof_response['cooldown'])

    return last_proof_response

def mine(proof):
    mine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"
    # mine_endpoint = "http://127.0.0.1:8000/api/bc/mine/"
    mine_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('SECRET_KEY')}"}
    # mine_headers = {"Content-Type": "application/json", "Authorization": f"Token {config('TEST_KEY')}"}
    mine_payload = {"proof": proof}
    mine_response = json.loads(requests.post(mine_endpoint, data=json.dumps(mine_payload), headers=mine_headers).content)

    sleep(mine_response['cooldown'])

    return mine_response

def get_lambda_coin_balance():
    lambda_coin_balance_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/"
    # lambda_coin_balance_endpoint = "http://127.0.0.1:8000/api/bc/get_balance/"
    lambda_coin_balance_headers = {"Authorization": f"Token {config('SECRET_KEY')}"}
    # lambda_coin_balance_headers = {"Authorization": f"Token {config('TEST_KEY')}"}
    lambda_coin_balance_response = json.loads(requests.get(lambda_coin_balance_endpoint, headers=lambda_coin_balance_headers).content)

    sleep(lambda_coin_balance_response['cooldown'])

    return lambda_coin_balance_response

# Fill out graph vertices
traversal_graph = Traversal_Graph_Complete()
with open(os.path.join(dirname, 'traversal_graph_complete.txt')) as json_file:
    traversal_graph.vertices = json.load(json_file)

# Fix issue with int/string keys
cleaned_traversal_graph_vertices = {}
for vertex in traversal_graph.vertices:
    cleaned_traversal_graph_vertices[int(vertex)] = traversal_graph.vertices[vertex]
traversal_graph.vertices = cleaned_traversal_graph_vertices

# Fill out exits
for vertex in traversal_graph.vertices:
    exits = {}
    for direction in traversal_graph.vertices[vertex]['exits']:
        exits[direction] = int(traversal_graph.vertices[vertex]['exits'][direction])
    traversal_graph.vertices[vertex]['exits'] = exits

# Log player stats out
check_status_response = check_status()
print(f'CHECK STATUS RESPONSE: {check_status_response}')

# Get player stats/room info
name = check_status_response['name']
gold = check_status_response['gold']
encumbrance = check_status_response['encumbrance']
init_response = get_init_response()
traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']

counter = 0
start_time = time()

#################################################
## Pick up treasure and sell to shop until you ##
## have 1000 gold, then go change your name #####
#################################################
while name != my_name:
    while gold < 1000:
        while encumbrance < 7:

            # Get path to treasure
            to_treasure = traversal_graph.bfs(init_response, 'items', 'small treasure')

            # Go to it
            for move in to_treasure:
                make_wise_move(move, init_response, traversal_graph)
                counter += 1
                print(f'{counter} moves made in {time() - start_time} seconds.')
                init_response = get_init_response()
                traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']

                for item in init_response['items']:
                    if 'treasure' in item:
                        examine_response = examine_item(item)

                        print(f'EXAMINE RESPONSE: {examine_response}')

                        take_item_response = take_item(item)
                        init_response = get_init_response()
                        traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']
                        check_status_response = check_status()

                        print(f'CHECK STATUS RESPONSE: {check_status_response}')

                        encumbrance = check_status_response['encumbrance']

                        if encumbrance >= 7:
                            break
                if encumbrance >= 7:
                    break

        # Get path to shop
        to_shop = traversal_graph.bfs(init_response, 'title', 'Shop')

        # Go to it
        for move in to_shop:
            make_wise_move(move, init_response, traversal_graph)
            counter += 1
            print(f'{counter} moves made in {time() - start_time} seconds.')
            init_response = get_init_response()
            traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']

        # Get there and sell stuff
        if init_response['title'] == 'Shop':
            check_status_response = check_status()
            for item in check_status_response['inventory']:
                if 'treasure' in item:
                    sell_item_response = sell_item(item)
                    print(f'SELL ITEM RESPONSE: {sell_item_response}')
                    check_status_response = check_status()
                    print(f'CHECK STATUS RESPONSE: {check_status_response}')
                    gold = check_status_response['gold']
                    encumbrance = check_status_response['encumbrance']

    # Get path to name changer room
    to_name_changer = traversal_graph.bfs(init_response, 'description', "change_name")

    # Go to it and change name
    for move in to_name_changer:
        make_wise_move(move, init_response, traversal_graph)
        counter += 1
        print(f'{counter} moves made in {time() - start_time} seconds.')
        init_response = get_init_response()
        traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']
    if "change_name" in init_response['description']:
        change_name_response = change_name('spmcdonnell')
        print(f"CHANGE NAME RESPONSE: {change_name_response}")
        check_status_response = check_status()
        print(f'CHECK STATUS RESPONSE: {check_status_response}')

# to_shrine = traversal_graph.bfs(init_response, 'description', "shrine")
# for move in to_shrine:
#     make_wise_move(move, init_response, traversal_graph)
#     counter += 1
#     print(f'{counter} moves made in {time() - start_time} seconds.')
#     init_response = get_init_response()
#     traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']
# if 'shrine' in init_response['description']:
#     pray_response = pray()
#     print(f"PRAY RESPONSE: {pray_response}")
#     check_status_response = check_status()
#     print(f'CHECK STATUS RESPONSE: {check_status_response}')

##############################################
## Go to well/mining area and submit proofs ##
##############################################
while True:

    # Get path to well
    to_wishing_well = traversal_graph.bfs(init_response, 'title', "Wishing Well")

    # Move to it
    for move in to_wishing_well:
        make_wise_move(move, init_response, traversal_graph)
        counter += 1

        print(f'{counter} moves made in {time() - start_time} seconds.')

        init_response = get_init_response()
        traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']

    # Check well, get binary room #, convert it
    if init_response['title'] == 'Wishing Well':    
        examine_response = examine_item('Wishing Well')

        print(f'EXAMINE RESPONSE: {examine_response}')

        check_status_response = check_status()

        print(f'CHECK STATUS RESPONSE: {check_status_response}')

        faint_pattern = examine_response['description'].split('...\n\n')[1]
        with open(os.path.join(dirname, 'faint_pattern.ls8'), 'w') as outfile:
            outfile.write(faint_pattern)
        cpu = CPU()
        cpu.load(os.path.join(dirname, 'faint_pattern.ls8'))
        f = io.StringIO()
        with redirect_stdout(f):
            cpu.run()
        faint_pattern = f.getvalue().replace('\n', '')

        print(f'FAINT PATTERN: {faint_pattern}')

        room_id = int(faint_pattern.replace('Mine your coin in room ', ''))

    # Get path to specified room found above
    to_mining_location = traversal_graph.bfs(init_response, 'room_id', room_id)

    # Move to it
    for move in to_mining_location:
        make_wise_move(move, init_response, traversal_graph)
        counter += 1

        print(f'{counter} moves made in {time() - start_time} seconds.')

        init_response = get_init_response()
        traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']

    # Stop at room, generate and submit proof
    if init_response['room_id'] == room_id:
        last_proof_response = get_last_proof()

        print(f'GET LAST PROOF RESPONSE: {last_proof_response}')
        
        last_proof = last_proof_response['proof']
        difficulty = last_proof_response['difficulty']

        while True:
            proof = random.randint(0, 9999999999)
            guess = f"{last_proof}{proof}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash[:difficulty] == ''.join(['0' for _ in range(difficulty)]):
                break

        print(f'NEW PROOF: {proof}')
        mine_response = mine(proof)
        print(f'MINE RESPONSE: {mine_response}')
        lambda_coin_balance_response = get_lambda_coin_balance()
        print(f'LAMBDA COIN BALANCE RESPONSE: {lambda_coin_balance_response}')
        check_status_response = check_status()
        print(f'CHECK STATUS RESPONSE: {check_status_response}')

        ##############################################
        ## Uncomment to stop after getting one coin ##
        ##############################################

        # if lambda_coin_balance_response['messages'][0] != 'You have a balance of 0 Lambda Coins':
        #     break
