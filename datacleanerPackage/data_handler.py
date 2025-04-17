
# File Name: Nebelung_Assignment11
# Student Name: Josh Slocumb, Caitlin Hutchins
# email: slocumbjt@mail.uc.edu, hutchicu@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 4/10/2025
# Course #/Section: IS 4010-001
# Semester/Year:Spring 2025
# Brief Description of the assignment: This assignment interacts with a csv file, cleans it and prints several csv files of the data cleaned
# Citations: Perplexity AI
# Brief Description of what this module does: This module interacts with the data cleaner package to print the results of the cleaned files
# File Name: Nebelung_Assignment11
# Student Name: Josh Slocumb, Caitlin Hutchins
# email: slocumbjt@mail.uc.edu, hutchicu@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date: 4/10/2025
# Course #/Section: IS 4010-001
# Semester/Year:Spring 2025
# Brief Description of the assignment: This assignment interacts with a csv file, cleans it and prints several csv files of the data cleaned
# Citations: Perplexity AI
# Brief Description of what this module does: THis module reads the csv file so it can be processed from dictionaries

import csv
import os
from typing import List, Dict

class DataHandler:
    """Handles CSV input/output operations"""
    
    def __init__(self, input_path: str):
        self.input_path = input_path
        
    def read_csv(self) -> List[Dict[str, str]]:
        """Read CSV file into list of dictionaries"""
        with open(self.input_path, 'r') as f:
            return list(csv.DictReader(f))
    
    @staticmethod
    def write_csv(data: List[Dict], output_path: str) -> None:
        """Write data to CSV file"""
        if not data:
            print(f"Warning: No data to write to {output_path}")
            return
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fieldnames = data[0].keys()
    
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

