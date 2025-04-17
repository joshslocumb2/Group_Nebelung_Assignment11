
# File Name: Nebelung_Assignment11
# Student Name: Josh Slocumb, Caitlin Hutchins
# email: slocumbjt@mail.uc.edu, hutchicu@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 4/10/2025
# Course #/Section: IS 4010-001
# Semester/Year:Spring 2025
# Brief Description of the assignment: This assignment interacts with a csv file, cleans it and prints several csv files of the data cleaned
# Citations: Perplexity AI
# Brief Description of what this module does: This module processes and cleans our data 

import requests
from typing import Optional
from urllib.parse import quote

class ZipCodeService:
    """Handles zip code lookups using zipcodebase API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://app.zipcodebase.com/api/v1"
    
    def get_zip_code(self, city: str, state: str) -> Optional[str]:
        """Get a ZIP code for a city and state"""
        try:
            city_encoded = quote(city)
            state_encoded = quote(state)
            
            url = f"{self.base_url}/code/city?apikey={self.api_key}&city={city_encoded}&state_code={state_encoded}&country=us"
            
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Correctly handle API response format
                results = data.get('results', [])
                if results:
                    return str(results[0])  # Return first zip code from list
        except Exception:
            pass
        return None

