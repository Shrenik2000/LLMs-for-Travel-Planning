#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pandas import DataFrame
from typing import Optional, Union
import re
import requests
from requests.exceptions import SSLError
import time
import numpy as np


# In[ ]:


class Flights:
    def __init__(self, path="database/flights/clean_Flights_2022.csv"):
        self.path = path
        self.data = None

        try:
            self.data = pd.read_csv(self.path).dropna()[['Flight Number', 'Price', 'DepTime', 'ArrTime', 'ActualElapsedTime', 'FlightDate', 'OriginCityName', 'DestCityName', 'Distance']]
            print("Flights API loaded.")
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            self.data = pd.DataFrame()

    def load_db(self):
        try:
            self.data = pd.read_csv(self.path).dropna().rename(columns={'Unnamed: 0': 'Flight Number'})
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")

    def run(self, origin: str, destination: str, departure_date: str) -> Union[DataFrame, str]:
        """Search for flights by origin, destination, and departure date."""
        results = self.data[(self.data["OriginCityName"] == origin) &
                            (self.data["DestCityName"] == destination) &
                            (self.data["FlightDate"] == departure_date)]
        if results.empty:
            return f"There is no flight from {origin} to {destination} on {departure_date}."
        return results

    def run_for_annotation(self, origin: str, destination: str, departure_date: str) -> str:
        """Search for flights by origin, destination, and departure date considering potential annotations."""
        results = self.data[(self.data["OriginCityName"] == self.extract_before_parenthesis(origin)) &
                            (self.data["DestCityName"] == self.extract_before_parenthesis(destination)) &
                            (self.data["FlightDate"] == departure_date)]
        return results.to_string(index=False)

    @staticmethod
    def extract_before_parenthesis(s):
        match = re.search(r'^(.*?)\([^)]*\)', s)
        return match.group(1) if match else s

    def get_city_set(self):
        city_set = set()
        for index, row in self.data.iterrows():
            city_set.add(row['OriginCityName'])
            city_set.add(row['DestCityName'])
        return city_set

#Example of how to use the consolidated script
# if __name__ == "__main__":
#     # Replace with the path to your flights CSV file
#     flights = Flights(path="database/flights/clean_Flights_2022.csv")
    
#     # Load the database
#     flights.load_db()
    
#     # Search for flights
#     origin = "Oakland"
#     destination = "Tucson"
#     departure_date = "2022-03-15"
#     result = flights.run(origin, destination, departure_date)
#     print(result)

#     Search for flights considering potential annotations
#     result_with_annotation = flights.run_for_annotation("New York (NY)", "Los Angeles (LA)", departure_date)
#     print(result_with_annotation)

#     Get set of cities
#     city_set = flights.get_city_set()
#     print(city_set)


# In[ ]:


class Restaurants:
    def __init__(self, path="database/restaurants/clean_restaurant_2022.csv"):
        self.path = path
        try:
            self.data = pd.read_csv(self.path).dropna()[['Name', 'Average Cost', 'Cuisines', 'Aggregate Rating', 'City']]
            print("Restaurants loaded.")
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            self.data = pd.DataFrame()

    def load_db(self):
        try:
            self.data = pd.read_csv(self.path).dropna()
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")

    def run(self, city: str) -> Union[DataFrame, str]:
        """Search for restaurants by city."""
        results = self.data[self.data["City"] == city]
        if results.empty:
            return "There are no restaurants in this city."
        return results

    def run_for_annotation(self, city: str) -> DataFrame:
        """Search for restaurants by city, considering potential annotations."""
        city_cleaned = self.extract_before_parenthesis(city)
        results = self.data[self.data["City"] == city_cleaned]
        return results

    @staticmethod
    def extract_before_parenthesis(s):
        match = re.search(r'^(.*?)\([^)]*\)', s)
        return match.group(1) if match else s

# Example of how to use the consolidated script
# if __name__ == "__main__":
#     # Replace with the path to your restaurants CSV file
#     restaurants = Restaurants(path="database/restaurants/clean_restaurant_2022.csv")
    
#     # Load the database
#     restaurants.load_db()
    
#     # Search for restaurants in a specific city
#     city = "Tucson"
#     result = restaurants.run(city)
#     print(result)

    # Search for restaurants considering potential annotations
    #result_with_annotation = restaurants.run_for_annotation("New York (NY)")
    #print(result_with_annotation)


# In[ ]:


class Attractions:
    def __init__(self, path="database/attractions/attractions.csv"):
        self.path = path
        try:
            self.data = pd.read_csv(self.path).dropna()[['Name', 'Latitude', 'Longitude', 'Address', 'Phone', 'Website', 'City']]
            print("Attractions loaded.")
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            self.data = pd.DataFrame()

    def load_db(self):
        try:
            self.data = pd.read_csv(self.path).dropna()[['Name', 'Latitude', 'Longitude', 'Address', 'Phone', 'Website', 'City']]
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")

    def run(self, city: str) -> Union[DataFrame, str]:
        """Search for attractions by city."""
        results = self.data[self.data["City"] == city]
        results = results.reset_index(drop=True)
        if results.empty:
            return "There are no attractions in this city."
        return results

    def run_for_annotation(self, city: str) -> DataFrame:
        """Search for attractions by city, considering potential annotations."""
        city_cleaned = self.extract_before_parenthesis(city)
        results = self.data[self.data["City"] == city_cleaned]
        results = results.reset_index(drop=True)
        return results

    @staticmethod
    def extract_before_parenthesis(s):
        match = re.search(r'^(.*?)\([^)]*\)', s)
        return match.group(1) if match else s

# Example of how to use the consolidated script
# if __name__ == "__main__":
#     # Replace with the path to your attractions CSV file
#     attractions = Attractions(path="database/attractions/attractions.csv")
    
#     # Load the database
#     attractions.load_db()
    
#     # Search for attractions in a specific city
#     city = "Tucson"
#     result = attractions.run(city)
#     print(result)

    # Search for attractions considering potential annotations
    # result_with_annotation = attractions.run_for_annotation("San Francisco (CA)")
    # print(result_with_annotation)


# In[ ]:


class Accommodations:
    def __init__(self, path="database/accommodations/clean_accommodations_2022.csv"):
        self.path = path
        try:
            self.data = pd.read_csv(self.path).dropna()[['NAME', 'price', 'room type', 'house_rules', 'minimum nights', 'maximum occupancy', 'review rate number', 'city']]
            print("Accommodations loaded.")
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            self.data = pd.DataFrame()

    def load_db(self):
        try:
            self.data = pd.read_csv(self.path).dropna()
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")

    def run(self, city: str) -> Union[DataFrame, str]:
        """Search for accommodations by city."""
        results = self.data[self.data["city"] == city]
        if results.empty:
            return "There are no accommodations in this city."
        return results

    def run_for_annotation(self, city: str) -> DataFrame:
        """Search for accommodations by city, considering potential annotations."""
        city_cleaned = self.extract_before_parenthesis(city)
        results = self.data[self.data["city"] == city_cleaned]
        return results

    @staticmethod
    def extract_before_parenthesis(s):
        match = re.search(r'^(.*?)\([^)]*\)', s)
        return match.group(1) if match else s

# Example of how to use the consolidated script
# if __name__ == "__main__":
#     # Replace with the path to your accommodations CSV file
#     accommodations = Accommodations(path="database/accommodations/clean_accommodations_2022.csv")
    
#     # Load the database
#     accommodations.load_db()
    
#     # Search for accommodations in a specific city
#     city = "Tucson"
#     result = accommodations.run(city)
#     print(result)

#     Search for accommodations considering potential annotations
#     result_with_annotation = accommodations.run_for_annotation("New York (NY)")
#     print(result_with_annotation)


# In[ ]:


class Cities:
    def __init__(self, path="database/background/citySet_with_states.txt") -> None:
        self.path = path
        self.load_data()
        print("Cities loaded.")

    def load_data(self):
        try:
            with open(self.path, "r") as file:
                city_state_mapping = file.read().strip().split("\n")
            self.data = {}
            for unit in city_state_mapping:
                city, state = unit.split("\t")
                if state not in self.data:
                    self.data[state] = [city]
                else:
                    self.data[state].append(city)
        except Exception as e:
            print(f"An error occurred while loading the data: {e}")
            self.data = {}

    def run(self, state) -> dict:
        if state not in self.data:
            raise ValueError("Invalid State")
        else:
            return self.data[state]

# Example of how to use the Cities class
# if __name__ == "__main__":
#     # Replace with the path to your city-state file
#     cities = Cities(path="database/background/citySet_with_states.txt")
    
#     # Fetch cities for a specific state
#     state = "Arizona"
#     try:
#         cities_list = cities.run(state)
#         print(f"Cities in {state}: {cities_list}")
#     except ValueError as e:
#         print(e)


# In[3]:


class Notebook:
    def __init__(self) -> None:
        self.data = []

    def write(self, input_data: DataFrame, short_description: str):
        self.data.append({"Short Description": short_description, "Content": input_data})
        return f"The information has been recorded in Notebook, and its index is {len(self.data)-1}."
    
    def update(self, input_data: DataFrame, index: int, short_description: str):
        if index < 0 or index >= len(self.data):
            return "Index out of range."
        self.data[index]["Content"] = input_data
        self.data[index]["Short Description"] = short_description
        return "The information has been updated in Notebook."
    
    def list(self):
        results = []
        for idx, unit in enumerate(self.data):
            results.append({"index": idx, "Short Description": unit['Short Description']})
        return results

    def list_all(self):
        results = []
        for idx, unit in enumerate(self.data):
            if isinstance(unit['Content'], DataFrame):
                results.append({
                    "index": idx,
                    "Short Description": unit['Short Description'],
                    "Content": unit['Content'].to_string(index=False)
                })
            else:
                results.append({
                    "index": idx,
                    "Short Description": unit['Short Description'],
                    "Content": unit['Content']
                })
        return results
    
    def read(self, index):
        if index < 0 or index >= len(self.data):
            return "Index out of range."
        return self.data[index]
    
    def reset(self):
        self.data = []
        
    
    def extract_all_as_string(self):
        all_data_str = ""
        for idx, unit in enumerate(self.data):
            description = unit['Short Description']
            if isinstance(unit['Content'], DataFrame):
                content_str = unit['Content'].to_string(index=False)
            else:
                content_str = str(unit['Content'])
            all_data_str += f"Index {idx} - Description: {description}\nContent:\n{content_str}\n\n"
        return all_data_str


# In[12]:


# Create a sample DataFrame
# data = {
#     'Column1': [1, 2, 3],
#     'Column2': ['A', 'B', 'C']
# }
# df = pd.DataFrame(data)

# # Initialize the notebook
# notebook = Notebook()

# # Add the DataFrame to the notebook
# notebook.write(df, "This is a sample entry")

# # List summaries of entries
# print(notebook.list(), '\n')
# # List detailed content of all entries
# print(notebook.list_all(), '\n')

# # Update the entry at index 0
# df_new = pd.DataFrame({
#     'Column1': [4, 5, 6],
#     'Column2': ['D', 'E', 'F']
# })
# notebook.update(df_new, 0, "Updated description")

# # Read the entry at index 0
# print(notebook.read(0))

# # Reset the notebook (clear all entries)
# notebook.reset()


# In[ ]:


def extract_before_parenthesis(text: str) -> str:
    """Extracts the part of the text before any parentheses."""
    if "(" in text:
        return text.split("(")[0].strip()
    return text.strip()

class GoogleDistanceMatrix:
    def __init__(self) -> None:
        self.data = pd.read_csv('database/googleDistanceMatrix/distance.csv')
        print("GoogleDistanceMatrix loaded.")

    def run(self, origin, destination, mode='driving'):
        origin = extract_before_parenthesis(origin)
        destination = extract_before_parenthesis(destination)
        info = {"origin": origin, "destination": destination, "cost": None, "duration": None, "distance": None}
        response = self.data[(self.data['origin'] == origin) & (self.data['destination'] == destination)]
        if len(response) > 0:
            if response['duration'].values[0] is None or response['distance'].values[0] is None or response['duration'].values[0] is np.nan or response['distance'].values[0] is np.nan:
                return "No valid information."
            info["duration"] = response['duration'].values[0]
            info["distance"] = response['distance'].values[0]
            if 'driving' in mode:
                info["cost"] = int(eval(info["distance"].replace("km", "").replace(",", "")) * 0.05)
            elif mode == "taxi":
                info["cost"] = int(eval(info["distance"].replace("km", "").replace(",", "")))
            if 'day' in info["duration"]:
                return "No valid information."
            return f"{mode}, from {origin} to {destination}, duration: {info['duration']}, distance: {info['distance']}, cost: {info['cost']}"
        return f"{mode}, from {origin} to {destination}, no valid information."
    
    def run_for_evaluation(self, origin, destination, mode='driving'):
        origin = extract_before_parenthesis(origin)
        destination = extract_before_parenthesis(destination)
        info = {"origin": origin, "destination": destination, "cost": None, "duration": None, "distance": None}
        response = self.data[(self.data['origin'] == origin) & (self.data['destination'] == destination)]
        if len(response) > 0:
            if response['duration'].values[0] is None or response['distance'].values[0] is None or response['duration'].values[0] is np.nan or response['distance'].values[0] is np.nan:
                return info
            info["duration"] = response['duration'].values[0]
            info["distance"] = response['distance'].values[0]
            if 'driving' in mode:
                info["cost"] = int(eval(info["distance"].replace("km", "").replace(",", "")) * 0.05)
            elif mode == "taxi":
                info["cost"] = int(eval(info["distance"].replace("km", "").replace(",", "")))
            return info
        return info

    
    
class Evaluation:
    def __init__(self, plan_str, budget):
        self.plan_str = plan_str
        self.budget = budget
    
    def commonse(self):
        # Initialize variables
        check_dash = 1
        check_restaurant_repeat = 1
        restaurants = []

        # Split the plan by days
        days = self.plan_str.split('Day ')
        
        # Check for '-' in incorrect places
        for i, day in enumerate(days):
            if '-' in day:
                if i < len(days) - 1:  # Not the last day
                    if 'Accommodation' not in day or 'Accommodation: -' not in day:
                        check_dash = 0
                elif 'Accommodation: -' in day:
                    check_dash = 1
                else:
                    check_dash = 0
        
        # Collect all restaurants
        for day in days:
            if 'Breakfast:' in day:
                start = day.index('Breakfast:') + len('Breakfast: ')
                end = day.find(';', start)
                if end == -1:
                    end = day.find('\n', start)
                if end == -1:
                    end = len(day)
                restaurant = day[start:end].strip()
                if restaurant != '-':
                    restaurants.append(restaurant)

            if 'Lunch:' in day:
                start = day.index('Lunch:') + len('Lunch: ')
                end = day.find(';', start)
                if end == -1:
                    end = day.find('\n', start)
                if end == -1:
                    end = len(day)
                restaurant = day[start:end].strip()
                if restaurant != '-':
                    restaurants.append(restaurant)

            if 'Dinner:' in day:
                start = day.index('Dinner:') + len('Dinner: ')
                end = day.find(';', start)
                if end == -1:
                    end = day.find('\n', start)
                if end == -1:
                    end = len(day)
                restaurant = day[start:end].strip()
                if restaurant != '-':
                    restaurants.append(restaurant)

        # Check for repeated restaurants
        if len(restaurants) != len(set(restaurants)):
            check_restaurant_repeat = 0

        # Calculate final value
        final_value = (check_dash + check_restaurant_repeat + 5) / 8
        return final_value

    def hard(self):
        # Regular expression to match costs with or without the dollar sign
        cost_matches = re.findall(r'Cost:\s*\$?(\d+\.?\d*)', self.plan_str)
        
        # Convert matches to float and sum them up
        total_cost = sum(float(cost) for cost in cost_matches)
        print("\nBudget: ", total_cost,"\n")
        
        # Check if the total cost is within the budget limit
        if total_cost <= 1.1 * self.budget:
            budget_check = 1
        else:
            budget_check = 0
        
        # Calculate final value
        final_value = (budget_check + 4) / 5
        return final_value

    def evaluate(self):
        return {
            'Commonse Sense constraints pass rate': self.commonse(),
            'Hard Constraint pass rate': self.hard()
        }

# In[ ]:




