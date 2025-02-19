#-----------------------------------------------------------------------------------------------#
# Description: This file contains the class definition for the Country entity. The Country class
# represents a country object with attributes such as name, flag, population, and capital. The
# class provides a method to convert the object to a dictionary for API responses. The Country
# entity is used throughout the application to represent country data and provide a consistent
# interface for interacting with country information. The entity class is an essential part of
# the application architecture, as it defines the structure and behavior of the country objects
# used in the application.
#-----------------------------------------------------------------------------------------------#
class Country:
    def __init__(self, name, flag, population=None, capital=None):
        self.name = name
        self.flag = flag
        self.population = population
        self.capital = capital

    def to_dict(self):
        """Converts the Country object to a dictionary (for API responses)."""
        return {
            "name": self.name,
            "flag": self.flag,
            "population": self.population,
            "capital": self.capital,
        }
