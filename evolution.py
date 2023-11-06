import requests


def get_id_name(species: dict) -> dict:
    # species is een dict waarin de url  staat en de naam van de pokemon staat
    # de naam lees je af uit de dict en de id haal je uit de url
    # voorbeeld:
    # species = {'name':'pikachu', 'ur;':'https://pokeapi.co/api/v2/pokemon-species/25/'}
    return {"id": species["url"].split("/")[-2], "name": species["name"].capitalize()}


def get_evolutions(speciesURL: str) -> list:
    # doet request naar api om de url van de evolutieketen te krijgen
    r = requests.get(speciesURL)
    status = r.status_code
    if status != 200:
        return [None, status]
    else:
        r = requests.get(speciesURL).json()

    # met de url kan je de keten bekijken en de pokemon er uit krijgen
    chainURL = r["evolution_chain"]["url"]
    # doet een request naar de chainurl om de keten ook daadwerkelijk te krijgen
    r = requests.get(chainURL)
    status = r.status_code
    if status != 200:
        return [None, status]
    else:
        r = requests.get(chainURL).json()

    # als er een evolutie is in de keten is possible een list met de evoluties
    if r["chain"]["evolves_to"]:
        possible = r["chain"]["evolves_to"]
    else:
        # anders niet
        possible = []
    # de eerste pokemon zit niet in evolves_to dus die moet er apart uit worden gehaald
    first_poke = get_id_name(r["chain"]["species"])

    evos = [first_poke]
    # er zijn pokemon (zoals eevee) die in meerdere pokemon kunnen evolueren
    # je moet dus elke pokemon in possible afgaan om ze allemaal te vangen (hehe)
    for poke in possible:
        evos.append(get_id_name(poke["species"]))
        # als de pokemon nog een keer evolueert
        if poke["evolves_to"]:
            for evolve in poke["evolves_to"]:
                evos.append(get_id_name(evolve["species"]))
                # vaker hoeft niet, want er is geen pokemon die meer dan twee keer evolueert
                # (a -> b -> c zijn twee evoluties)
    return evos
