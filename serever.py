import json

from flask import Flask, request
import pandas as pd
import csv

app = Flask(__name__)
pokemon_objects = []

class Pokemon:
    def __init__(self, id, name, type1, type2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary, image_path=None):
        self.id = id
        self.name = name
        self.type1 = type1
        self.type2 = type2 if type2 else 'None'
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.generation = generation
        self.legendary = legendary
    def __repr__(self):
        return f"Pokemon({self.name}, Type: {self.type1}/{self.type2})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type1': self.type1,
            'type2': self.type2,
            'total': self.total,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'sp_atk': self.sp_atk,
            'sp_def': self.sp_def,
            'speed': self.speed,
            'generation': self.generation,
            'legendary': self.legendary
        }

@app.route('/get_pokemon', methods=['GET'])
def get_pokemon():
    # search = request.data
    args = request.args
    pokemon_name = args['name']
    for item in pokemon_objects:
        if item.name.lower() == pokemon_name:
            return json.dumps(item.to_dict())

    return('false')


if __name__ == "__main__":
    path = r'C:\Users\USER\PycharmProjects\Mid_Project\Mid_Project\Mid_Project\Docs\Pokemon.csv'
    pokemon_df = pd.read_csv(path)

    pokemon_df = pokemon_df.drop_duplicates()
    pokemon_df = pokemon_df.sort_values(by='#', ascending=True)
    pokemon_df = pokemon_df.reset_index(drop=True)


    # Iterate over each row in the DataFrame and create a Pokemon object
    for index, row in pokemon_df.iterrows():
        pokemon = Pokemon(
            id=row['#'],
            name=row['Name'],
            type1=row['Type 1'],
            type2=row['Type 2'] if pd.notnull(row['Type 2']) else 'None',  # Handling potential NaN values
            total=row['Total'],
            hp=row['HP'],
            attack=row['Attack'],
            defense=row['Defense'],
            sp_atk=row['Sp. Atk'],
            sp_def=row['Sp. Def'],
            speed=row['Speed'],
            generation=row['Generation'],
            legendary=row['Legendary']
        )
        pokemon_objects.append(pokemon)
    app.run()