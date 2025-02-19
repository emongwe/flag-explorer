#-------------------------------------------------------------------------------------------------------#
# The data_access.py file contains the data access layer of the application.
# It interacts with external APIs and data sources to fetch and store data. 
# The RestCountriesAPI class is responsible for fetching data from the external RestCountries API, 
# while the JsonFileDataSource class handles reading and writing data to a local JSON file. 
# The JsonFileDataSource class also has methods for retrieving all countries, getting country details
# by name, and refreshing the data from the external API. The RestCountriesAPI class uses the requests
# library to make HTTP requests to the external API and handle responses. 
# The JsonFileDataSource class uses the json library to read and write data to a JSON file. 
# The classes are designed to be used as dependencies in the main application (app.py) to provide data 
# to the services and controllers. The data_access.py file is a crucial part of the application 
# architecture, as it ensures data is fetched and stored correctly for the rest of the application to use.
#-------------------------------------------------------------------------------------------------------#
import requests
import json
import os
from .entities import Country

class RestCountriesAPI: 
    BASE_URL = os.getenv("RESTCOUNTRIES_API_URL", "https://restcountries.com/v3.1")

    def fetch_all_countries(self):
        try:
            response = requests.get(f"{self.BASE_URL}/all")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from external API: {e}")
            return None 

class JsonFileDataSource:
    def __init__(self, filename="countries_data.json", api_client=RestCountriesAPI()):
        self.filename = filename
        self.api_client = api_client

    def _load_data(self):
        if not os.path.exists(self.filename):
            if not self.refresh_data():
                return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data from file: {e}")
            return []

    def _save_data(self, data):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data to file: {e}")
            return False
        return True

    def get_all_countries(self):
        return self._load_data()

    def get_country_by_name(self, name):
        data = self._load_data()
        for country in data:
             if country["name"].lower() == name.lower():
                return country
        return None

    def refresh_data(self):
        raw_data = self.api_client.fetch_all_countries()
        if raw_data is None:
            return False

        transformed_data = []
        for country_data in raw_data:
            transformed_country = {
                "name": country_data.get("name", {}).get("common", "N/A"),
                "flag": country_data.get("flags", {}).get("svg", ""),
                "population": country_data.get("population", 0),
                "capital": country_data.get("capital", ["N/A"])[0] if country_data.get("capital") else "N/A",
            }
            transformed_data.append(transformed_country)

        return self._save_data(transformed_data)