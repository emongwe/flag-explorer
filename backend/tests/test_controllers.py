#----------------------------------------------------------------------------------------------------#
# This is the test file for the controllers module. It tests the controllers in the module using
# pytest fixtures and asserts the expected behavior of the controllers. The tests are designed to
# verify that the controllers return the correct responses for different scenarios, such as getting
# all countries, getting country details by name, and refreshing the data from the external API.
# The tests ensure that the controllers interact correctly with the service layer and handle the
# responses appropriately. The test cases cover different scenarios to validate the behavior of the
# controllers in the application.
#----------------------------------------------------------------------------------------------------#

import pytest
from src.country_api.controllers.controller import CountryController
from flask import Flask, Blueprint
import json

def test_get_all_countries_controller(country_controller):
    response = country_controller.get_all_countries()
    assert response.status_code == 200  # No need for app context
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["name"] == "Test Country 1"

def test_get_country_details_controller(country_controller):
    response = country_controller.get_country_details("Test Country 1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Test Country 1"
    assert data["population"] == 1000

    response_not_found = country_controller.get_country_details("Nonexistent")
    assert response_not_found.status_code == 404
    data_not_found = json.loads(response_not_found.data)
    assert data_not_found["message"] == "Country not found"

def test_refresh_data_controller(country_controller):
    response = country_controller.refresh_data()
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Data refreshed successfully"