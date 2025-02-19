#----------------------------------------------------------------------------------------------------#
# This file is the entry point for the application. It creates the Flask app and registers the
# routes using the Flask Blueprint. The app is configured to use the CountryController to handle
# requests related to country data. The create_app function initializes the application and returns
# the app instance. The main execution block runs the app in debug mode.
# The app.py file is the main entry point for the application and is responsible for creating the
# Flask app, registering routes, and running the application. The app.py file is an essential part
# of the application architecture, as it defines the structure and behavior of the application and
# how it interacts with the data access and service layers to provide data to the client.
#----------------------------------------------------------------------------------------------------#
from flask import Flask
from .models.data_access import JsonFileDataSource, RestCountriesAPI
from .services.service import CountryService
from .controllers.controller import CountryController, country_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Dependency Injection
    api_client = RestCountriesAPI()
    data_source = JsonFileDataSource(api_client=api_client)
    country_service = CountryService(data_source)
    country_controller = CountryController(country_service)
    
    # Register Routes (using Flask Blueprint)
    @country_bp.route('/countries', methods=['GET'])
    def get_all_countries_route():
        return country_controller.get_all_countries()

    @country_bp.route('/countries/<string:name>', methods=['GET'])
    def get_country_details_route(name):
        return country_controller.get_country_details(name)

    @country_bp.route('/refresh', methods=['POST'])
    def refresh_data_route():
        return country_controller.refresh_data()

    app.register_blueprint(country_bp)
    return app

# Main Execution 
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)