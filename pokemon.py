import json
import requests
response = {}
def get_pokemon():
    global response
    params = {
        'offset':0,
        'limit':100000
    }
    url = ('https://pokeapi.co/api/v2/pokemon')
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        quit()
    else:
        #print(f'status code: {status}')
        response = requests.get(url, params = params).json()
        return format_names()

def format_names():
    global response
    results = response['results']
    names, ids = [], []
    for result in results:
        poke_id = int(str(result['url'])[34:-1])
        if poke_id < 10000:
            ids.append(poke_id)
            names.append(result['name'])
    array = [{'name':names[i], 'id':ids[i]} for i in range(len(names))]

    return array
