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


def get_moves(movelist) -> list:
    moves = [movelist[0]['move']['name'].capitalize()]
    for i in range(1,len(movelist)):
        if movelist[i]['move']:
            if movelist[i]['move']['name']:
                moves.append(f"{movelist[i]['move']['name'].capitalize()}")
    return moves

#print(get_moves('charizard'))

def get_stats(stats) -> list:
    return [
        [stat['stat']['name'].upper(),
         stat['base_stat']] 
        for stat in stats]


def get_info(pokemon) -> list:
    url = (f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        quit()
    else:
        r = requests.get(url).json()
    #print(f'r: \n\n\n{r}')
    types = r['types'][0]['type']['name']
    print(types)
    if len(r['types']) == 2:
        types = f"{types} and {r['types'][1]['type']['name']}"
        print(types)
    games = [r['game_indices'][i]['version']['name'].capitalize() for i in range(len(r['game_indices']))]
    poke_id = r['id']
    moves = get_moves(r['moves'])
    stats = get_stats(r['stats'])
    return [poke_id, types, games, moves, stats]




# pokemon id voor image
@app.route('/', methods = ['GET', 'POST'])
def hello_world(pokemonName='', maintext = '', error=0, moves='', poke_id=-1, types='', games='', stats=None):
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
    types=info[1]
    games = info[2]
    moves = info[3]
    stats = info[4]
    
    

    return render_template('index.html', pokemonName=pokemon.capitalize(), error=error, moves=moves, poke_id=poke_id, types=types, games=games, stats=stats)
