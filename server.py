from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
pokemon_objects = []

class Pokemon:
    def __init__(self, id, name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary):
        self.id = id
        self.name = name
        self.type1 = type1
        self.type2 = type2 or 'None'  # Handle missing Type 2 as 'None'
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.generation = generation
        self.legendary = legendary

    def to_dict(self):
        return vars(self)

@app.route('/get_pokemon', methods=['GET'])
def get_pokemon():
    pokemon_name = request.args.get('name', default="", type=str).lower()
    for pokemon in pokemon_objects:
        if pokemon.name.lower() == pokemon_name:
            return jsonify(pokemon.to_dict())
    return jsonify({'error': 'Pokémon not found'}), 404

if __name__ == "__main__":
    try:
        path = r'venv/Docs/Pokemon.csv'
        pokemon_df = pd.read_csv(path)

        # Data cleaning and preparation
        pokemon_df.drop_duplicates(inplace=True)
        pokemon_df.sort_values(by='Name', ascending=True, inplace=True)
        pokemon_df['Type 2'] = pokemon_df['Type 2'].fillna('None')  # Fill NaN for 'Type 2'
        pokemon_df['Legendary'] = pokemon_df['Legendary'].fillna(False)  # Fill NaN with False
        pokemon_df['Legendary'] = pokemon_df['Legendary'].astype(bool)  # Convert to boolean

        # Create Pokemon objects
        for _, row in pokemon_df.iterrows():
            pokemon_objects.append(Pokemon(
                id=row['#'],
                name=row['Name'],
                type1=row['Type 1'],
                type2=row['Type 2'],
                total=row['Total'],
                hp=row['HP'],
                attack=row['Attack'],
                defense=row['Defense'],
                sp_atk=row['Sp. Atk'],
                sp_def=row['Sp. Def'],
                speed=row['Speed'],
                generation=row['Generation'],
                legendary=row['Legendary']
            ))

        app.run(debug=True)
    except Exception as e:
        print(f"Failed to load and process the Pokemon CSV: {e}")
