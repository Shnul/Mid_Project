import requests
from prettytable import PrettyTable


def get_pokemon_info(names):
    server_url = "http://localhost:5000/get_pokemon"
    pokemon_data = {}
    for name in names:
        params = {'name': name}
        try:
            response = requests.get(server_url, params=params)
            if response.status_code == 200:
                pokemon_data[name] = response.json()
            else:
                print(
                    f"Error: Unable to find Pokémon named '{name}'. Server responded with status code {response.status_code}.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while trying to connect to the server: {e}")
    return pokemon_data


def display_pokemon_data(pokemon_data):
    if pokemon_data:
        table = PrettyTable()
        field_names = ["Attribute"] + [name.capitalize() for name in pokemon_data.keys()]
        table.field_names = field_names

        # Get a list of all attributes
        attributes = set().union(*[attributes.keys() for attributes in pokemon_data.values()])

        # Add rows to the table for each attribute
        for attribute in attributes:
            row = [attribute.capitalize()]
            for name, attributes in pokemon_data.items():
                attribute_value = attributes.get(attribute, '')
                if isinstance(attribute_value, dict):
                    row.append(attribute_value.get(attribute, ''))
                else:
                    row.append(attribute_value)
            table.add_row(row)

        print("\nPokémon Details:")
        print(table)
    else:
        print("No data to display.")


if __name__ == "__main__":
    while True:
        # Prompt for Pokémon name
        user_input = input("\nEnter your Pokémon names separated by '|' (or type 'exit' to quit): ").strip()
        if user_input.lower() == 'team rocket':
            print("Exiting the program.")
            break

        pokemon_names = [name.strip() for name in user_input.split('|')]
        pokemon_data = get_pokemon_info(pokemon_names)
        display_pokemon_data(pokemon_data)
