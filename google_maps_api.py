import os
import json
import time
import requests
from datetime import datetime

# Initialize global variable to keep track of the last string
last_string = ""

def handler(event, context):
    global last_string
    
    # Lambda environment variables for API key
    GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']

    # Extract address string from event (you may need to adjust this based on your API Gateway setup)
    current_string = event['queryStringParameters']['address']
    
    # Wait for 0.5 seconds
    time.sleep(0.5)

    # If the current string is different from the last one
    if current_string != last_string:
        # Update the last string
        last_string = current_string
        
        # Make Google Maps API request, restricted to Brazil
        url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={current_string}&key={GOOGLE_MAPS_API_KEY}&components=country:BR"
        
        # Print current action
        print(f"[{datetime.now()}] Making Google Maps API request.")
        
        try:
            # Execute GET request
            response = requests.get(url)
            
            # Parse response to JSON
            suggestions = response.json()
            
            # Return list of formatted addresses
            return {
                "statusCode": 200,
                "body": json.dumps({"suggestions": suggestions})
            }
        except Exception as e:
            # Print error information
            print(f"Error: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
    else:
        # Return without making an API call
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "https://d82cwlwrba78u.cloudfront.net",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
            "body": json.dumps({"suggestions": []})
        }
