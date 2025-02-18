import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Configure standard logger
logger = logging.getLogger('country-api')
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = logging.FileHandler('country-api.log')
file_handler.setLevel(logging.DEBUG)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Model (simplified representation)
def get_country_data(name, data):
    for country in data:
        if country['name']['common'] == name:
            return {
                'name': country['name']['common'],
                'population': country.get('population', 'N/A'),
                'capital': country['capital'][0] 
                    if country.get('capital') 
                    else 'N/A',
                'flags': country.get('flags', [])
            }
    return None

# Load country data (from JSON file)
try:
    with open('countries.json', 'r') as f:
        country_data = json.load(f)
except FileNotFoundError:
    print("Error: countries.json not found. Please create this file.")
    exit()
except json.JSONDecodeError:
    print("Error: Invalid JSON format in countries.json.")
    exit()

# Controller
@app.route('/countries', methods=['GET'])
def get_countries():
    logger.info('Received request for /countries')
    name = request.args.get('name')
    if name:
        country = get_country_data(name, country_data)
        if country:
            return jsonify(country)
        else:
            return jsonify({"message": "Country not found"}), 404
    else:
        countries = [{'name': country['name']['common']} for country in country_data]
        return jsonify(countries)

if __name__ == '__main__':
    app.run(debug=True)