# Copyright 2026 Allan Brand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://apache.org
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import mgrs
import argparse
import requests
from dotenv import load_dotenv

# Load variables from the local .env file
load_dotenv()

def get_config():
    api_key = os.environ.get("GEOCODIO_API_KEY")
    base_url = os.environ.get("GEOCODIO_BASE_URL", "https://api.geocod.io/v2")
    
    if not api_key:
        raise ValueError("Error: GEOCODIO_API_KEY is not set in the environment or .env file.")
        
    return api_key, base_url

def address_to_mgrs_geocodio(address_string):
    key, base_url = get_config()
    
    response = requests.get(f"{base_url}/geocode", params={"q": address_string, "api_key": key})
    response.raise_for_status()
    data = response.json()
    
    results = data.get("results")
    if not results or len(results) == 0:
        raise ValueError(f"Could not resolve location for address: {address_string}")
        
    # FIX: Select the first dictionary match inside the list element
    best_match = results[0]
    location = best_match["location"]
    lat, lon = location["lat"], location["lng"]
    formatted_address = best_match["formatted_address"]
    
    m = mgrs.MGRS()
    mgrs_coord = m.toMGRS(lat, lon, MGRSPrecision=5)
    if isinstance(mgrs_coord, bytes):
        mgrs_coord = mgrs_coord.decode('utf-8')
        
    return {
        "address": formatted_address,
        "latitude": lat,
        "longitude": lon,
        "mgrs": mgrs_coord
    }

def mgrs_to_address_geocodio(mgrs_string):
    m = mgrs.MGRS()
    try:
        lat, lon = m.toLatLon(mgrs_string)
    except Exception as e:
        raise ValueError(f"Invalid MGRS coordinate string format: {e}")
        
    key, base_url = get_config()
    
    response = requests.get(f"{base_url}/reverse", params={"q": f"{lat},{lon}", "api_key": key})
    response.raise_for_status()
    data = response.json()
    
    results = data.get("results")
    if not results or len(results) == 0:
        return {"latitude": lat, "longitude": lon, "address": "No address found."}
        
    # FIX: Select the first dictionary match inside the list element
    best_match = results[0]
    return {
        "latitude": lat,
        "longitude": lon,
        "address": best_match["formatted_address"]
    }

def main():
    parser = argparse.ArgumentParser(
        description="Convert locations using dynamic HTTP requests to Geocodio API via .env config."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--to-mgrs", metavar="ADDRESS", help="Convert an address to MGRS.")
    group.add_argument("--to-address", metavar="MGRS_COORD", help="Convert MGRS to an address.")
    args = parser.parse_args()

    try:
        if args.to_mgrs:
            result = address_to_mgrs_geocodio(args.to_mgrs)
            print(f"MGRS (1-Meter): {result['mgrs']}")
            print(f"Full Address:   {result['address']}")
        elif args.to_address:
            sanitized_mgrs = args.to_address.replace(" ", "")
            result = mgrs_to_address_geocodio(sanitized_mgrs)
            print(f"Full Address:   {result['address']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
