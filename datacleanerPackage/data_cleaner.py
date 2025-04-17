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


from typing import List, Dict, Tuple
from apiPackage.zip_service import ZipCodeService
import re

class DataCleaner:
    """Handles core data cleaning logic"""
    
    def __init__(self, zip_service: ZipCodeService):
        self.zip_service = zip_service
        self._zip_lookups = 0
        self.duplicates_removed = 0
        self.corrupted_addresses = 0  # New counter added
        
    def process_data(self, data: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Main processing method (now returns 3 lists)"""
        seen = set()
        cleaned = []
        anomalies = []
        corrupted = []  # New list for corrupted addresses
        
        for row in data:
            if self._is_pepsi(row):
                anomalies.append(row)
                continue
                
            row = self._format_price(row)
            row = self._fix_zipcodes(row)
            
            # New corruption check
            if self._is_corrupted_address(row):
                corrupted.append(row)
                self.corrupted_addresses += 1
                continue
                
            # Existing deduplication logic
            row_hash = hash(frozenset(row.items()))
            if row_hash not in seen:
                seen.add(row_hash)
                cleaned.append(row)
            else:
                self.duplicates_removed += 1
        
        return cleaned, anomalies, corrupted  # Now returns 3 outputs

    def _is_corrupted_address(self, row: Dict) -> bool:
        """Detect corrupted addresses where ZIP code appears first"""
        addr_key = next((k for k in row if 'address' in k.lower()), None)
        if not addr_key or not row[addr_key]:
            return False
            
        # Check if address starts with ZIP code pattern
        return bool(re.match(r'^\s*\d{5}(-\d{4})?\s', row[addr_key]))

    # Keep existing methods unchanged below
    def _is_pepsi(self, row: Dict) -> bool:
        """Detect Pepsi purchases"""
        return any('pepsi' in str(v).lower() for v in row.values())

    def _format_price(self, row: Dict) -> Dict:
        """Ensure exactly 2 decimal places"""
        for key in [k for k in row if 'gross price' in k.lower()]:
            try:
                value = row[key].strip()
                if value:
                    row[key] = f"{float(value):.2f}"
            except (ValueError, TypeError):
                row[key] = "0.00"  # Default invalid prices to 0.00
        return row

    def _fix_zipcodes(self, row: Dict) -> Dict:
        """Add missing zip codes (max 5)"""
        if self._zip_lookups >= 5:
            return row
            
        addr_key = next((k for k in row if 'address' in k.lower()), None)
        if not addr_key:
            return row
            
        address = row[addr_key]
        if not re.search(r'\b\d{5}(-\d{4})?\b', address):
            try:
                parts = [p.strip() for p in address.split(',')]
                if len(parts) >= 3:
                    city = parts[-2]
                    state = parts[-1].split()[-1]
                    
                    if zip_code := self.zip_service.get_zip_code(city, state):
                        row[addr_key] = f"{address}, {zip_code}"
                        self._zip_lookups += 1
            except Exception:
                pass
        return row
