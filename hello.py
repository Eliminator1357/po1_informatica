from flask import Flask, render_template, request
import pokemon
import requests
pokemons = pokemon.get_pokemon()
app = Flask(__name__)


def is_pokemon(s: str):
    global pokemons
    for pokemon in pokemons:
        if pokemon['name'] == s:
            return True
    return False

def get_moves(pokemon):
    params = {
        'name':pokemon
    }
    url = ('https://pokeapi.co/api/v2/move/')
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        quit()
    else:
        response = requests.get(url, params = params).json()
    
    results = response['results']
    moves = results[0]['name']
    for i in range(1,len(results)):
        moves += f', {results[i]["name"]}'
    print(moves)
    return moves

#print(get_moves('charizard'))

@app.route('/', methods = ['GET', 'POST'])
def hello_world(text=None, error=0):
    try:
        pokemon = request.form['text'].lower()
        print(is_pokemon(pokemon))
        if not is_pokemon(pokemon):
            return render_template('index.html', text=None, error=1)
    except Exception as e:
        return render_template('index.html', text=e, error=0)
    text += f'{pokemon} has the following moves:\n{get_moves(pokemon)}'
    
    
    

    return render_template('index.html', text=text, error=error)


