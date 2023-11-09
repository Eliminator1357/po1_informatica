from flask import Flask, render_template, request
import pokemon
import requests
import evolution
import time
import logging
from random import randint

pokemons = pokemon.get_pokemon()  # een array van dicts {'name':id}
if pokemons == None:
    quit()  # wil geen app hebben met een niet-werkende api
idnamedict = {pokemon["id"]: pokemon["name"] for pokemon in pokemons}

app = Flask(__name__)
# zet alle logs uit als log.disabled True is
# is makkelijker met debuggen
log = logging.getLogger("werkzeug")
log.disabled = False


def is_pokemon(s: str) -> bool:
    # als s gelijk is aan een pokemon['name'] in pokemons dan is de invoer een pokemon
    global pokemons
    for pokemon in pokemons:
        if pokemon["name"] == s:
            return True
    return False


def get_random_pokemon() -> str:
    # Kiest een random pokemon door een random getal te nemen tussen 1 en het aantal pokemon
    # Dit getal wordt door een dict gevoerd en hieruit krijg je de naam van de pokemon
    global pokemons, idnamedict
    numberOfPokemon = len(pokemons) + 1
    randomID = randint(1, numberOfPokemon)
    randomName = idnamedict[randomID]
    return randomName


def get_moves(movelist) -> list:
    # zet alle moves in movelist in de array moves
    moves = []
    for i in range(0, len(movelist)):
        if movelist[i]["move"]:
            if movelist[i]["move"]["name"]:
                moves.append(f"{movelist[i]['move']['name'].capitalize()}")
    return moves


def get_stats(stats) -> list:
    # array van arrays met elke stat en de waarde ervan
    return [[stat["stat"]["name"].upper(), stat["base_stat"]] for stat in stats]


def get_sprites(sprites, extrasprites) -> list:
    keys = list(sprites.keys())
    spriteURLS = [sprites[key] for key in keys]
    # de laatste 2 elementen in de sprites dict zijn geen urls maar meer sprites
    # deze nemen veel ruimte in dus als er niet op de knop is gedrukt laat ik ze weg
    if not extrasprites:
        spriteURLS.pop(-1)
        spriteURLS.pop(-1)
    else:
        versions, other = spriteURLS[-1], spriteURLS[-2]
        # nu zijn ze niet meer nodig
        spriteURLS.pop(-1)
        spriteURLS.pop(-1)
        # er zijn geneste dicts in sprites, een heet other en de andere heet versions
        # om de sprites er uit te halen zijn er geneste for loops nodig
        otherKeys = list(other.keys())
        for key in otherKeys:
            tempkeys = list(other[key].keys())
            for tempkey in tempkeys:
                if other[key][tempkey]:
                    spriteURLS.append(other[key][tempkey])

        # hier is er nog een derde for loop nodig omdat er hier 3 dicts genest zijn:
        # versions -> generations -> game -> links
        generationkeys = list(versions.keys())
        for generation in generationkeys:
            gamekeys = list(versions[generation].keys())
            for game in gamekeys:
                if versions[generation][game]:
                    spritekeys = list(versions[generation][game].keys())
                    for spritekey in spritekeys:
                        if spritekey == "animated":
                            # geanimeerde sprites zijn te veel gedoe om er nu nog in te doen
                            continue
                        spriteURLS.append(versions[generation][game][spritekey])
    return spriteURLS


def get_info(pokemon, extrasprites) -> list:
    # functie om alle info op te halen met 1 request (gaat veel sneller dan meerdere requests doen)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        # status 200 is ok, dus als status niet 200 is gaat er iets fout
        # [None, status] omdat de functie een array returnt
        return [None, status]

    else:
        # als status 200 is
        r = requests.get(url).json()

    # zet alle variabelen klaar voor de individuele get functies zodat het leesbaarder is
    speciesURL = r["species"]["url"]
    types = r["types"][0]["type"]["name"]
    # (pokemon kunnen max 2 types hebben en om grammaticafouten te voorkomen is dit de beste optie denk ik)
    if len(r["types"]) == 2:
        types = f"{types} and {r['types'][1]['type']['name']}"
    games = [
        r["game_indices"][i]["version"]["name"].capitalize()
        for i in range(len(r["game_indices"]))
    ]
    poke_id = r["id"]

    # haalt alle info op
    moves = get_moves(r["moves"])
    stats = get_stats(r["stats"])
    evolutions = evolution.get_evolutions(speciesURL)
    sprites = get_sprites(r["sprites"], extrasprites)
    info = [poke_id, types, games, moves, stats, evolutions, sprites]
    return info


@app.route("/", methods=["GET", "POST"])
def main(
        pokemonName="",
        maintext="",
        error=0,
        moves="",
        poke_id=-1,
        types="",
        games="",
        stats=None,
        evolutions=None,
        sprites=None,
):
    # om de tijd te beoordelen is time.perf_counter beter dan time.time omdat perf_counter nauwkeuriger is
    start_time = time.perf_counter()
    # als er een error is laat het een error pagina zien
    try:
        pokemon = request.form["text"].lower()
        # bool(int(...)) want req.form(['extra_sprites']) is altijd 0 of 1, maar als een string. bool ziet '0' als True, dus moet ik er eerst een int van maken
        extrasprites = bool(int(request.form["extra_sprites"]))
        # als er random is ingevoerd moet pokemon een random pokemon worden
        if pokemon == "random":
            pokemon = get_random_pokemon()

        # als de ingevoerde tekst geen pokemon is geeft het een error
        if not is_pokemon(pokemon):
            return render_template("index.html", text=None, error=1)
    except Exception as e:
        print(e)
        return render_template("index.html", text=e, error=0)

    info = get_info(pokemon, extrasprites)

    # info[0] is de pokemon id, als er geen id is voor de pokemon is er wat fout gegaan
    if info[0] == None:
        return render_template("error.html", errorcode=info[1])
    poke_id = info[0]
    types = info[1]
    games = info[2]
    moves = info[3]
    stats = info[4]
    if info[5]:
        evolutions = info[5]
    sprites = info[6]

    end_time = time.perf_counter()
    print(f"Pagina laden duurde {end_time - start_time:.2f} sec.")
    return render_template(
        "index.html",
        pokemonName=pokemon.capitalize(),
        error=error,
        moves=moves,
        poke_id=poke_id,
        types=types,
        games=games,
        stats=stats,
        evolutions=evolutions,
        sprites=sprites,
    )
