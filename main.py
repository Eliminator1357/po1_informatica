from flask import Flask, render_template, request
import pokemon
import requests
pokemons = pokemon.get_pokemon()
app = Flask(__name__)


def is_pokemon(s: str) -> bool:
    global pokemons
    for pokemon in pokemons:
        if pokemon['name'] == s:
            return True
    return False

def get_image(pokemon: str) -> str:

    spriteURL = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png'
    return spriteURL


def get_moves(pokemon) -> list:
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
    # zorg ervoor dat arrey returnt
    results = response['results']
    moves = [results[0]['name'].capitalize()]
    for i in range(1,len(results)):
        if results[i]:
            if results[i]['name']:
                moves.append(f'{results[i]["name"].capitalize()}')
    return moves


#print(get_moves('charizard'))


def get_info(pokemon) -> list:
    url = (f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        quit()
    else:
        response = requests.get(url).json()
    #print(f'Response: \n\n\n{response}')
    poke_id = response['id']
    return [poke_id]




# pokemon id voor image
@app.route('/', methods = ['GET', 'POST'])
def hello_world(pokemonName='', maintext = '', error=0, moves='', poke_id=-1):
    # check if pokemon exists, give error page if not
    try:
        pokemon = request.form['text'].lower()
        print(is_pokemon(pokemon))
        if not is_pokemon(pokemon):
            return render_template('index.html', text=None, error=1)
    except Exception as e:
        return render_template('index.html', text=e, error=0)
    info = get_info(pokemon)
    poke_id = info[0]
    moves = get_moves(pokemon)
    
    
    

    return render_template('index.html', pokemonName=pokemon.capitalize(), error=error, moves=moves, poke_id=poke_id)


if __name__ == "__main__" and 1==1:
    #print(get_moves('charizard'))
    #print(get_image('6'))
    print(get_info('charizard'))