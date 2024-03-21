import requests
from IPython.display import display, HTML, Image
import pandas as pd


def get_pokemon_info(pokemon_name):
    server_url = "http://localhost:5000/get_pokemon"
    params = {'name': pokemon_name}
    response = requests.get(server_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


# Prompt for Pokémon name
pokemon_name = input("Enter the name of the Pokémon you're interested in: ")
pokemon_data = get_pokemon_info(pokemon_name)

if pokemon_data and 'image_url' in pokemon_data and pokemon_data['image_url']:
    # Display the image
    display(Image(url=pokemon_data['image_url']))

    # Display the data in a table (excluding the image URL for clarity)
    df = pd.DataFrame([pokemon_data])
    df.drop(columns=['image_url'], inplace=True)
    display(HTML(df.to_html(index=False)))
else:
    print(f"No valid information or image URL found for {pokemon_name}.")
