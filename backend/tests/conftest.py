#------------------------------------------------------------------------------------------------------#
# This file contains the fixtures that will be used in the tests. Fixtures are reusable objects that
# can be shared across multiple test functions. In this file, we define fixtures for the Flask app,
# test client, test countries data, mock data source, country service, country controller, and mock
# external API. These fixtures will be used in the test functions to set up the test environment and
# provide the necessary dependencies for testing the application components. The fixtures are defined
# using the pytest framework and are used to create the necessary objects for testing the application.
#------------------------------------------------------------------------------------------------------#

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import pytest
from country_api.app import create_app
from country_api.models.data_access import JsonFileDataSource, RestCountriesAPI
from country_api.services.service import CountryService
from country_api.controllers.controller import CountryController

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_countries():
    return [
        {"name": "Test Country 1", "flag": "🚩", "population": 1000, "capital": "Test Capital 1"},
        {"name": "Test Country 2", "flag": "🏳️", "population": 2000, "capital": "Test Capital 2"}
    ]
@pytest.fixture
def mock_data_source(test_countries, mocker):
    mock_source = mocker.MagicMock(spec=JsonFileDataSource)
    mock_source.get_all_countries.return_value = test_countries
    mock_source.get_country_by_name.side_effect = lambda name: next((c for c in test_countries if c["name"] == name), None)
    mock_source.refresh_data.return_value = True
    return mock_source

@pytest.fixture
def country_service(mock_data_source):
    return CountryService(mock_data_source)

@pytest.fixture
def country_controller(country_service):
    return CountryController(country_service)

@pytest.fixture
def mock_external_api(mocker):
    mock_api = mocker.MagicMock(spec=RestCountriesAPI)
    return mock_api