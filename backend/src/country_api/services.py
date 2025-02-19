#--------------------------------------------------------------------------------------------------------#
# Description: This file contains the service layer of the application. It is responsible for
# interacting with the data access layer and providing the business logic for the application.
# The CountryService class contains methods for getting all countries, getting country details by name,
# and refreshing the data from the external API. The service layer is designed to be used as a dependency
# in the main application (app.py) to provide the business logic for the application. The service layer
# is responsible for processing the data from the data access layer and providing it to the controllers.
# The service layer is an essential part of the application architecture, as it defines the behavior of
# the application and how it interacts with the data access layer to provide data to the controllers.
# The service layer is responsible for handling the business logic of the application and ensuring that
# the data is processed correctly before being returned to the client.
# --------------------------------------------------------------------------------------------------------#
import requests
import json
import os
from .entities import Country

class CountryService:
    def __init__(self, data_source):
        self.data_source = data_source

    def get_all_countries(self):
        countries = self.data_source.get_all_countries()
        return [Country(c["name"], c["flag"]) for c in countries]

    def get_country_details(self, name):
        country_data = self.data_source.get_country_by_name(name)
        if country_data:
            return Country(**country_data)
        return None

    def refresh_data(self):
        return self.data_source.refresh_data()