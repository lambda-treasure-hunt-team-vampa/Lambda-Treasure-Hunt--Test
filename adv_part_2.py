from decouple import config
import requests
import json
import random
from time import sleep, time
import os

dirname = os.path.dirname(os.path.abspath(__file__))
movement_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


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
                if key_to_search == 'items':
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

traversal_graph = Traversal_Graph_Complete()
with open(os.path.join(dirname, 'traversal_graph_complete.txt')) as json_file:
    traversal_graph.vertices = json.load(json_file)

cleaned_traversal_graph_vertices = {}
for vertex in traversal_graph.vertices:
    cleaned_traversal_graph_vertices[int(vertex)] = traversal_graph.vertices[vertex]
traversal_graph.vertices = cleaned_traversal_graph_vertices

for vertex in traversal_graph.vertices:
    exits = {}
    for direction in traversal_graph.vertices[vertex]['exits']:
        exits[direction] = int(traversal_graph.vertices[vertex]['exits'][direction])
    traversal_graph.vertices[vertex]['exits'] = exits

check_status_response = check_status()
print(f'CHECK STATUS RESPONSE: {check_status_response}')
gold = check_status_response['gold']
encumbrance = check_status_response['encumbrance']
init_response = get_init_response()
traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']

counter = 0
start_time = time()
while gold < 1000:
    while encumbrance < 7:
        to_treasure = traversal_graph.bfs(init_response, 'items', 'small treasure')
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
    to_shop = traversal_graph.bfs(init_response, 'title', 'Shop')
    for move in to_shop:
        make_wise_move(move, init_response, traversal_graph)
        counter += 1
        print(f'{counter} moves made in {time() - start_time} seconds.')
        init_response = get_init_response()
        traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']
    if init_response['title'] == 'Shop':
        check_status_response = check_status()
        for item in check_status_response['inventory']:
            if 'treasure' in item:
                sell_item_response = sell_item(item)
                print(f'SELL ITEM RESPONSE: {sell_item_response}')
                check_status_response = check_status()
                print(f'CHECK STATUS RESPONSE: {check_status_response}')
                encumbrance = check_status_response['encumbrance']
