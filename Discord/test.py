import json
from enum import Enum
import requests

class Elements(Enum):
    neutral = 1
    grass = 2
    fire = 3
    water = 4
    electric = 5
    ice = 6
    ground = 7
    dark = 8
    dragon = 9



with open ('files.json', 'r') as f:
    data = json.load(f)
    for pal in data:
        dic = {
            "name": pal['name'].lower(),
            "id": str(pal['key']),
            "partner_skill": pal['aura']['name'],
            "elements": [],
            "food": 0,
            "kindling": 0,
            "planting": 0,
            "handwork": 0,
            "lumbering": 0,
            "medicine_production": 0,
            "transporting": 0,
            "watering": 0,
            "generating_electricity": 0,
            "gathering": 0,
            "mining": 0,
            "cooling": 0,
            "farming": 0,
            "farming_loot": None,
        }
        for element in pal['types']:
            dic["elements"].append(Elements[element].value)
        for suit in pal['suitability']:
            if suit['type'] == 'medicine_function toLocaleLowerCase() { [native code] }':
                dic['medicine_production'] = int(suit['level'])
            elif suit['type'] == 'generating_function toLocaleLowerCase() { [native code] }':
                dic['generating_electricity'] = int(suit['level'])
            else:
                dic[suit['type']] = int(suit['level'])
        dic['day_habitat_img'] = f"./img/{dic['name']}_day.png".replace(' ', '_')
        dic['night_habitat_img'] = f"./img/{dic['name']}_night.png".replace(' ', '_')
        dic['pal_img'] = f"./img/{dic['name']}.png".replace(' ', '_')
        x = requests.post('https://palworld-api.asylium.app/api/v1/pals', json=dic)
        print(x.json())
