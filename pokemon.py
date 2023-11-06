import json
import requests

response = {}


def get_pokemon():
    # haalt alle pokemon op
    # limit:100_000 want de api geeft standaard 20 op als je geen limiet zet, om alle pokemon te krijgen moet de limiet erg groot zijn
    global response
    params = {"offset": 0, "limit": 100_000}
    url = "https://pokeapi.co/api/v2/pokemon"
    r = requests.get(url)
    status = r.status_code
    if status != 200:
        print(f"error {status}")
        return None
    else:
        response = requests.get(url, params=params).json()
        return format_names()


def format_names():
    global response
    results = response["results"]
    names, ids = [], []
    for result in results:
        # voor elk resultaat (dus elke pokemon) haalt het de id uit de url
        # de urls zijn opgebouwd uit een link naar de api en aan het einde de id van de pokemon
        # uit de url kan je dus de id van de pokemon halen door de laatste chars te pakken
        # voorbeeld url: https://pokeapi.co/api/v2/pokemon/967/
        poke_id = int(str(result["url"])[34:-1])
        ids.append(poke_id)
        names.append(result["name"])
    array = [{"name": names[i], "id": ids[i]} for i in range(len(names))]
    return array
