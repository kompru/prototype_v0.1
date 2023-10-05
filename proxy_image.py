import base64
import json
import requests
from requests.exceptions import HTTPError

def fetch_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will check for HTTP errors and raise an exception if any are found
        return base64.b64encode(response.content).decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def lambda_handler(event, context):
    try:
        image_url = event['queryStringParameters'].get('url')
        
        if not image_url:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "URL parameter is missing"}),
                "isBase64Encoded": False
            }

        print("Fetching image")

        image_base64 = fetch_image(image_url)

        if image_base64 is None:
            raise Exception("Failed to fetch image")

        print("Image fetched and encoded successfully.")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "https://www.kompru.com",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({"image": image_base64}),
            "isBase64Encoded": False
        }
    except HTTPError as e:
        print(f"HTTP Error: {e}")
        return {
            "statusCode": e.response.status_code,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)}),
            "isBase64Encoded": False
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "An error occurred"}),
            "isBase64Encoded": False
        }
