#-----------------------------------------------------------------------------------------#
# Test cases for the data_access module.
# These tests will cover the JsonFileDataSource and RestCountriesAPI classes.
#-----------------------------------------------------------------------------------------#
import pytest
import os
import json
from data_access import JsonFileDataSource, RestCountriesAPI
from unittest.mock import patch, mock_open

@pytest.fixture
def temp_data_file(tmpdir):
    file = tmpdir.join("test_countries.json")
    yield str(file)
    if os.path.exists(str(file)):
        os.remove(str(file))

def test_json_file_data_source_load_save(temp_data_file, test_countries):
    data_source = JsonFileDataSource(filename=temp_data_file)
    assert data_source._save_data(test_countries) == True
    loaded_data = data_source._load_data()
    assert loaded_data == test_countries

def test_get_all_countries(temp_data_file, test_countries):
     data_source = JsonFileDataSource(filename=temp_data_file)
     data_source._save_data(test_countries)
     all_countries = data_source.get_all_countries()
     assert all_countries == test_countries

def test_get_country_by_name_found(temp_data_file, test_countries):
    data_source = JsonFileDataSource(filename=temp_data_file)
    data_source._save_data(test_countries)
    country = data_source.get_country_by_name("Test Country 1")
    assert country == test_countries[0]

def test_get_country_by_name_not_found(temp_data_file, test_countries):
    data_source = JsonFileDataSource(filename=temp_data_file)
    data_source._save_data(test_countries)
    country = data_source.get_country_by_name("Nonexistent Country")
    assert country is None

def test_json_data_source_load_no_file(temp_data_file, mock_external_api):
    # Test when the file doesn't exist initially.
    mock_external_api.fetch_all_countries.return_value = []
    data_source = JsonFileDataSource(filename=temp_data_file, api_client=mock_external_api)
    data = data_source._load_data()
    assert data == []
    mock_external_api.fetch_all_countries.assert_called_once()


@patch('data_access.requests.get')
def test_rest_countries_api_fetch_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [{"name": {"common": "Test Country"}}]

    api = RestCountriesAPI()
    data = api.fetch_all_countries()
    assert data == [{"name": {"common": "Test Country"}}]
    mock_get.assert_called_once_with("https://restcountries.com/v3.1/all")


@patch('data_access.requests.get')
def test_rest_countries_api_fetch_failure(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException("Test Error")

    api = RestCountriesAPI()
    data = api.fetch_all_countries()
    assert data is None
    mock_get.assert_called_once_with("https://restcountries.com/v3.1/all")


def test_refresh_data_success(temp_data_file, mock_external_api, test_countries):
    # Mock the external API to return test data.
    mock_external_api.fetch_all_countries.return_value = [
        {"name": {"common": "Test Country 1"}, "flags": {"svg": "🚩"}, "population": 1000, "capital": ["Test Capital 1"]},
        {"name": {"common": "Test Country 2"}, "flags": {"svg": "🏳️"}, "population": 2000, "capital": ["Test Capital 2"]},
    ]
    data_source = JsonFileDataSource(filename=temp_data_file, api_client=mock_external_api)
    assert data_source.refresh_data() == True 

    # Load data from the file and verify it's been transformed and saved.
    with open(temp_data_file, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == test_countries


def test_refresh_data_failure(temp_data_file, mock_external_api):
    # Mock the external API to return test data.
    mock_external_api.fetch_all_countries.return_value = None
    data_source = JsonFileDataSource(filename=temp_data_file, api_client=mock_external_api)
    assert data_source.refresh_data() == False