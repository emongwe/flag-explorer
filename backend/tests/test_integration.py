#-------------------------------------------------------------------------------------------#
# Integration tests for the API.  These tests require the external API to be up and running.
# The tests will fetch data from the external API and test the API endpoints for getting all
# countries, getting country details, and refreshing the data.
#-------------------------------------------------------------------------------------------#
import pytest
import json
import os
from app import create_app
from data_access import JsonFileDataSource

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True

    # Use a temporary file for testing.  Important!
    test_db_file = "test_countries_integration.json"
    app.config['DATABASE'] = test_db_file

    with app.test_client() as client:
        yield client

    # Cleanup:  Remove the test database file after tests.
    if os.path.exists(test_db_file):
        os.remove(test_db_file)

def test_get_all_countries_integration(test_client):
    # Test with no existing data
    response = test_client.get('/countries')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_country_details_integration(test_client):
     # Test with an existing country (assuming "Germany" exists in the external API)
    response = test_client.get('/countries/Germany')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Germany"
    assert "population" in data
    assert "capital" in data

    # Test with a non-existent country
    response = test_client.get('/countries/NonExistentCountry')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["message"] == "Country not found"

def test_refresh_data_integration(test_client):
    response = test_client.post('/refresh')
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Data refreshed successfully"

    data_source = JsonFileDataSource()
    data = data_source._load_data()
    assert len(data) > 0