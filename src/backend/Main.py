from Garden import Garden
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
garden = Garden()


def get_all_plants():
    plants = garden.get_all_plants()

    # Convert the tuples into a list of dictionaries for easier JSON conversion
    plants_list = []
    for plant in plants:
        plant_dict = {
            'PK': plant[0],
            'name': plant[1],
            'water_freq': plant[2],
            'fertilizer_freq': plant[3],
            'temp_min': plant[4],
            'temp_max': plant[5],
            'humidity_min': plant[6],
            'humidity_max': plant[7]
        }
        plants_list.append(plant_dict)

    return plants_list


def get_plant(plant_id):
    plant = garden.get_plant(plant_id)

    plant_dict = {
        'PK': plant[0],
        'name': plant[1],
        'water_freq': plant[2],
        'fertilizer_freq': plant[3],
        'temp_min': plant[4],
        'temp_max': plant[5],
        'humidity_min': plant[6],
        'humidity_max': plant[7]
    }

    return plant_dict


def insert_plant(plant_dict):
    garden.insert_plant(
        name=plant_dict.get('name'),
        water_freq=plant_dict.get('water_freq'),
        fertilizer_freq=plant_dict.get('fertilizer_freq'),
        temp_min=plant_dict.get('temp_min'),
        temp_max=plant_dict.get('temp_max'),
        humidity_min=plant_dict.get('humidity_min'),
        humidity_max=plant_dict.get('humidity_max')
    )

    return plant_dict


@app.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    func_name = data.get('funcName')
    params = data.get('params')
    response = jsonify({'error': 'Unknown function name'})

    if func_name == 'get-all-plants':
        response = jsonify(get_all_plants())
    elif func_name == 'get-plant':
        response = jsonify(get_plant(params.get('id')))
    elif func_name == 'insert-plant':
        response = jsonify(insert_plant(params))

    return response


app.run(host='0.0.0.0', port=5000)
