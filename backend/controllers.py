#----------------------------------------------------------------------------------------------------#
# This file contains the controller classes for the CountryService. The controller classes are
# responsible for handling incoming requests, interacting with the service layer, and returning
# responses to the client. The CountryController class contains methods for getting all countries,
# getting country details by name, and refreshing the data from the external API. The controller
# classes are designed to be used as dependencies in the main application (app.py) to provide the
# API endpoints for the application. The controllers are responsible for processing the requests
# and returning the appropriate responses to the client. The controllers are an essential part of
# the application architecture, as they define the behavior of the API endpoints and how they interact
# with the service layer to provide data to the client.
# ----------------------------------------------------------------------------------------------------#
from flask import jsonify, Blueprint
from services import CountryService

country_bp = Blueprint('country_bp', __name__)

class CountryController:
    def __init__(self, country_service: CountryService):
        self.country_service = country_service

    def get_all_countries(self):
        countries = self.country_service.get_all_countries()
        return jsonify([country.to_dict() for country in countries])

    def get_country_details(self, name):
        country = self.country_service.get_country_details(name)
        if country:
            return jsonify(country.to_dict())
        else:
            return jsonify({"message": "Country not found"}), 404

    def refresh_data(self):
        if self.country_service.refresh_data():
            return jsonify({"message": "Data refreshed successfully"}), 200
        else:
            return jsonify({"message": "Failed to refresh data"}), 500