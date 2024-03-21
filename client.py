import requests
from prettytable import PrettyTable

def get_pokemon_info(pokemon_name):
    server_url = "http://localhost:5000/get_pokemon"
    params = {'name': pokemon_name}
    try:
        response = requests.get(server_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to find Pokémon named '{pokemon_name}'. Server responded with status code {response.status_code}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to connect to the server: {e}")
        return None

def display_pokemon_data(pokemon_data):
    if pokemon_data:
        table = PrettyTable()
        table.field_names = ["Attribute", "Value"]
        for key, value in pokemon_data.items():
            table.add_row([key.title(), value])
        print("\nPokémon Details:")
        print(table)
    else:
        print("No data to display.")

if __name__ == "__main__":
    while True:
        pokemon_name = input("\nEnter the name of the Pokémon you're interested in (or type 'rocket' to exit): ").strip()
        if pokemon_name.lower() == 'rocket':
            print("Team Rocket is blasting off again!")
            break

        if pokemon_name:
            pokemon_data = get_pokemon_info(pokemon_name)
            display_pokemon_data(pokemon_data)
        else:
            print("Please enter a valid Pokémon name.")
