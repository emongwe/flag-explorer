#-------------------------------------------------------------------------------------------------------#
# This file contains unit tests and integration tests for the app.py file.  The tests are designed to
# ensure that the application functions correctly and that the API endpoints return the expected data.
# The tests cover the main functionality of the application, including getting all countries, getting
# country details by name, and handling error cases. The tests are an essential part of the application
# development process, as they help ensure that the application works as expected and that new changes
# do not introduce bugs or regressions.
#-------------------------------------------------------------------------------------------------------#  
import pytest
from ..app import app, get_country_data

# Test data (for testing)
test_data = [
    {'name': {'common': 'United States'}, 'population': 331002651, 'capital': ['Washington, D.C.'], 'flags': ['https://flagcdn.com/w320/us.png']},
    {'name': {'common': 'France'}, 'capital': ['Paris']},
    {'name': {'common': 'Germany'}, 'population': 83240525},
    {'name': {'common': 'Invalid Country'}},
]

def test_get_country_data():
    # Test case 1: Valid country
    country = get_country_data('United States', test_data)
    assert country == {'name': 'United States', 'population': 331002651, 'capital': 'Washington, D.C.', 'flags': ['https://flagcdn.com/w320/us.png']}

    # Test case 2: Missing population
    country = get_country_data('France', test_data)
    assert country == {'name': 'France', 'population': 'N/A', 'capital': 'Paris', 'flags': []}

    # Test case 3: Missing capital
    country = get_country_data('Germany', test_data)
    assert country == {'name': 'Germany', 'population': 83240525, 'capital': 'N/A', 'flags': []}

    # Test case 4: Invalid country
    country = get_country_data('Invalid Country', test_data)
    assert country == {'capital': 'N/A', 'name': 'Invalid Country', 'population': 'N/A' , 'flags': []}
    
# Integration Tests
@pytest.fixture
def client():
    with app.test_client() as client:
        return client

def test_get_countries_endpoint(client):
    # Test case 1: Get list of countries
    response = client.get('/countries')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Test case 2: Get specific country details and flags
    response = client.get('/countries?name=United States')
    assert response.status_code == 200
    country = response.get_json()
    assert country['name'] == 'United States'
    assert country['population'] == 329484123
    assert country['capital'] == 'Washington, D.C.'
    assert len(country['flags']) > 0

    # Test case 3: Country not found
    response = client.get('/countries?name=NonExistentCountry')
    assert response.status_code == 404
    error_message = response.get_json()
    assert error_message['message'] == 'Country not found'