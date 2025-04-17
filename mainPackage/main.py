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

# main.py
 
import os
import time
from datacleanerPackage.data_handler import DataHandler
from datacleanerPackage.data_cleaner import DataCleaner
from apiPackage.zip_service import ZipCodeService

def main():
    API_KEY = "e978c950-162b-11f0-97f0-e96660f7696c"
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Data')
    
    input_path = os.path.join(DATA_DIR, 'fuel_data.csv')
    clean_path = os.path.join(DATA_DIR, 'cleanedData.csv')
    anomaly_path = os.path.join(DATA_DIR, 'dataAnomalies.csv')
    corrupted_path = os.path.join(DATA_DIR, 'corruptedData.csv')  # New output path
    
    try:
        start_time = time.time()
        
        handler = DataHandler(input_path)
        cleaner = DataCleaner(ZipCodeService(API_KEY))
        
        print("Processing data...")
        raw_data = handler.read_csv()
        clean_data, anomalies, corrupted = cleaner.process_data(raw_data)  # Updated to receive corrupted data
        
        handler.write_csv(clean_data, clean_path)
        handler.write_csv(anomalies, anomaly_path)
        handler.write_csv(corrupted, corrupted_path)  # Write corrupted data
        
        print("\nCleaning Complete!")
        print(f"Original rows: {len(raw_data):,}")
        print(f"Cleaned rows: {len(clean_data):,}")
        print(f"Anomalies found: {len(anomalies):,}")
        print(f"Corrupted addresses: {len(corrupted):,}")  # New output stat
        print(f"Duplicates removed: {cleaner.duplicates_removed:,}")
        print(f"ZIP codes added: {cleaner._zip_lookups}")
        print(f"Time taken: {time.time()-start_time:.2f}s")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
