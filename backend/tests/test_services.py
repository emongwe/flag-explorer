#--------------------------------------------------------------------------------------------------------#
# This file contains the tests for the services module of the application. The tests are designed to
# ensure that the service layer functions correctly and provides the expected behavior when interacting
# with the data access layer. The tests cover the methods for getting all countries, getting country
# details by name, and refreshing the data from the external API. The tests are an essential part of
# the application architecture, as they verify that the service layer functions correctly and provides
# the expected behavior to the controllers and client. The tests are designed to be run using the pytest
# testing framework and can be executed by running the pytest command in the terminal.
# --------------------------------------------------------------------------------------------------------#

import pytest
from src.country_api.services.service import CountryService
from src.country_api.services.entity import Country

def test_get_all_countries(country_service, test_countries):
    countries = country_service.get_all_countries()
    assert len(countries) == 2
    assert all(isinstance(country, Country) for country in countries)
    assert countries[0].name == test_countries[0]["name"]
    assert countries[0].cca2 == test_countries[0]["cca2"]
    assert countries[0].flag == test_countries[0]["flag"]
    assert countries[0].capital == test_countries[0]["capital"]
    assert countries[0].population == test_countries[0]["population"]

def test_get_country_details(country_service, test_countries):
    country = country_service.get_country_details("Test Country 1")
    assert isinstance(country, Country), f"Expected Country instance but got {type(country)}"
    assert country.name == "Test Country 1"
    assert country.cca2 == "SG"
    assert country.flag == "🚩"
    assert country.capital == "Test Capital 1"
    assert country.population == 1000

     # Test not found case
    not_found_country = country_service.get_country_details("Nonexistent Country")
    assert not_found_country is None

def test_refresh_data(country_service, mock_data_source):
    assert country_service.refresh_data() is True
    mock_data_source.refresh_data.assert_called_once()