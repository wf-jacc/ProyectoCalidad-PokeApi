import requests
import json
from database import connect, create_pokemon_table, save_pokemon_to_team, get_team_pokemon, remove_pokemon_from_team

def get_pokemon_data(pokemon_id):
    if pokemon_id.isdigit():
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    else:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id.lower()}"
    response = requests.get(url)
    data = response.json()

    if "id" in data:
        pokemon_number = data["id"]
        pokemon_name = data["name"]
        moves = [move["move"]["name"] for move in data["moves"]]
        types = [type["type"]["name"] for type in data["types"]]
        weaknesses = []

        for type_name in types:
            type_url = f"https://pokeapi.co/api/v2/type/{type_name}"
            type_response = requests.get(type_url)
            type_data = type_response.json()
            if 'damage_relations' in type_data:  # Fix: Use 'damage_relations' instead of 'damage_relation'
                for damage_relation in type_data["damage_relations"]["double_damage_from"]:
                    weaknesses.append(damage_relation["name"])

        return {
            "number": pokemon_number,
            "name": pokemon_name,
            "types": types, 
            "moves": moves,
            "weaknesses": weaknesses
        }
    return None

def main():
    print('''
 ██▓███   ▒█████   ██ ▄█▀ ▓█████ ███▄ ▄███▓ ▒█████   ███▄    █ 
▓██░  ██ ▒██▒  ██▒ ██▄█▒  ▓█   ▀▓██▒▀█▀ ██▒▒██▒  ██▒ ██ ▀█   █ 
▓██░ ██▓▒▒██░  ██▒▓███▄░  ▒███  ▓██    ▓██░▒██░  ██▒▓██  ▀█ ██▒
▒██▄█▓▒ ▒▒██   ██░▓██ █▄  ▒▓█  ▄▒██    ▒██ ▒██   ██░▓██▒  ▐▌██▒
▒██▒ ░  ░░ ████▓▒░▒██▒ █▄▒░▒████▒██▒   ░██▒░ ████▓▒░▒██░   ▓██░
▒▓▒░ ░  ░░ ▒░▒░▒░ ▒ ▒▒ ▓▒░░░ ▒░ ░ ▒░   ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
░▒ ░       ░ ▒ ▒░ ░ ░▒ ▒░░ ░ ░  ░  ░      ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
░░       ░ ░ ░ ▒  ░ ░░ ░     ░  ░      ░   ░ ░ ░ ▒     ░   ░ ░ 
░ ░  ░  ░   ░   ░         ░       ░ ░           ░ ''')
    print("Bienvenido al programa de Pokémon")
    db_connection = connect("localhost", "root", "", "pokedb")
    create_pokemon_table(db_connection)

    while True:
        print("\n¿Qué acción deseas realizar?")
        print("1. Obtener información de un Pokémon por nombre o número en la Pokédex")
        print("2. Mostrar Pokémon de un equipo")
        print("3. Quitar un Pokémon del equipo")
        print("4. Salir")
        opcion = input("Ingresa el número de la opción: ")

        if opcion == "1":
            pokemon_id = input("Ingresa el nombre o número del Pokémon: ")
            pokemon_data = get_pokemon_data(pokemon_id)
            if pokemon_data:
                print("\nInformación del Pokémon:")
                print(f"Número: {pokemon_data['number']}")
                print(f"Nombre: {pokemon_data['name']}")
                print("Tipos: ")
                for type in pokemon_data["types"]:
                    print(f"- {type}")
                print("Movimientos:")
                for move in pokemon_data["moves"]:
                    print(f"- {move}")
                print("Debilidades:")
                for weakness in pokemon_data["weaknesses"]:
                    print(f"- {weakness}")

                guardar = input("¿Deseas guardar este Pokémon en el equipo? (s/n): ")
                if guardar.lower() == "s":
                    team_name = input("Ingresa el nombre del equipo: ")
                    save_pokemon_to_team(db_connection, team_name, pokemon_data)
                    print(f"El Pokémon {pokemon_data['name']} ha sido guardado en el equipo {team_name}")
            else:
                print("No se encontró ningún Pokémon con ese nombre o número.")

        elif opcion == "2":
            team_name = input("Ingresa el nombre del equipo: ")
            team_pokemon = get_team_pokemon(db_connection, team_name)
            if team_pokemon:
                print(f"\nPokémon del equipo {team_name}:")
                for pokemon in team_pokemon:
                    print(f"Número: {pokemon['pokemon_number']}")
                    print(f"Nombre: {pokemon['pokemon_name']}")
                    print("--------------------")
            else:
                print(f"No se encontraron Pokémon en el equipo {team_name}")

        elif opcion == "3":
            team_name = input("Ingresa el nombre del equipo: ")
            pokemon_id = input("Ingresa el nombre o número del Pokémon a quitar: ")
            remove_pokemon_from_team(db_connection, team_name, pokemon_id)
            print(f"El Pokémon ha sido removido del equipo {team_name}")

        elif opcion == "4":
            break

        else:
            print("Opción inválida. Por favor, ingresa una opción válida.")

    db_connection.close()

if __name__ == "__main__":
    main()
