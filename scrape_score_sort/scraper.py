import os
import pytz
import json
import requests
from datetime import datetime
from geopy.geocoders import GoogleV3
from utils.product_formatter_utils import ProductFormatter, JsonFile
from utils.rappi_utils import StringUtils
from requests.exceptions import HTTPError, RequestException

# Constants
SAO_PAULO_TIMEZONE = pytz.timezone("America/Sao_Paulo")
URL_PASSPORT = "https://services.rappi.com.br/api/rocket/v2/guest/passport"
URL_GUEST = "https://services.rappi.com.br/api/rocket/v2/guest"
URL_STORE_ROUTER = 'https://services.rappi.com.br/api/web-gateway/web/stores-router/id/{}'
URL_UNIFIED_SEARCH = 'https://services.rappi.com.br/api/pns-global-search-api/v1/unified-search?is_prime=false&unlimited_shipping=false'

# Exception Classes
class RequestFailedException(Exception):
    pass

class AuthenticationException(Exception):
    pass

def get_current_formatted_time():
    current_datetime = datetime.now(SAO_PAULO_TIMEZONE)
    formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
    return formatted_time

def http_request(url, method='get', headers=None, json_data=None):
    try:
        if method == 'get':
            response = requests.get(url, headers=headers)
        elif method == 'post':
            response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        return response.json()
    except HTTPError as err:
        raise RequestFailedException(f'Request failed: {err}')
    except RequestException as err:
        raise RequestFailedException(f'An error occurred: {err}')

def get_bearer_token():
    request_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'deviceid': '34a6a2f7-2291-43c7-8bc3-98b2dd5b7e67'
    }
    json_data = http_request(URL_PASSPORT, headers=request_headers)
    token = json_data['token']
    request_headers['X-Guest-API-Key'] = token
    json_data = http_request(URL_GUEST, method='post', headers=request_headers)
    access_token = json_data['access_token']
    bearer_token = f'Bearer {access_token}'
    return bearer_token

def get_store_address_and_name(bearer_token, store_id):
    request_headers = {
        'authorization': bearer_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    json_data = http_request(URL_STORE_ROUTER.format(store_id), headers=request_headers)
    store_address = json_data['address']
    store_name = json_data['name']
    return store_address, store_name

def stores_list(lat, lng, query, bearer_token):
    request_headers = {
        'authorization': bearer_token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    payload = {
        'lat': lat,
        'lng': lng,
        'query': query,
        'options': {}
    }
    json_data = http_request(URL_UNIFIED_SEARCH, method='post', headers=request_headers, json_data=payload)
    stores = json_data['stores']
    stores_list = []
    for store in stores:
        store_dict = {}
        search_term = query
        store_id = store['store_id']
        store_address, store_name = get_store_address_and_name(bearer_token, store_id)
        products_list = StringUtils.get_store_products(store, store_id, store_address, store_name, search_term)
        store_dict[store_name] = products_list
        stores_list.append(store_dict)
    return stores_list

def convert_address_into_coordinates(address):
    api_key = os.environ.get('GOOGLE_API_KEY')
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(address)
    lat = location.latitude
    lng = location.longitude
    return lat, lng

def set_search_home_data(_products_list:list, _term:str)->dict:
    _products_dict = {}
    _products_dict['search_term'] = _term
    _products_dict['search_home_results_count'] = len(_products_list)
    _products_dict['search_home_results'] = _products_list
    return _products_dict

def update_product_scores_and_can_add(all_products):
    high_score_present = any(product['product-score'] >= 90 for product in all_products)

    for product in all_products:
        product_score = product['product-score']
        in_stock = product['in_stock']
        
        if in_stock == False:
            product['can_add'] = False
        elif high_score_present and product_score < 70:
            product['can_add'] = False
        elif not high_score_present and product_score < 70:
            product['can_add'] = True
        else:
            product['can_add'] = True

def lambda_handler(event, context):
    term = event['search_term']
    lat = event['lat']
    lng = event['lng']

    # Get the bearer_token
    bearer_token = get_bearer_token()

    products_list = []
    stores = stores_list(lat, lng, term, bearer_token )
    for store in stores:
        for store_items in store.values():
            for items in store_items:
                products_list.append(items)

    update_product_scores_and_can_add(products_list)  # 👈 Add this line here

    filtered_products_list = [product for product in products_list if product.get('can_add')]

    #add datetime 
    current_datetime = datetime.now(SAO_PAULO_TIMEZONE)
    formatted_datetime = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")

    datetime_products_list = []
    for product in filtered_products_list:
        items = list(product.items())
        items.insert(0, ('k collected-at', formatted_datetime))
        product = dict(items)
        datetime_products_list.append(product)

    current_datetime = datetime.now(SAO_PAULO_TIMEZONE)
    formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
    print(f'SCRAPPER: {formatted_time}')
    print(f'TOTAL PRODUCTS SCRAPED: {len(datetime_products_list)}')

    (product_names, store_addresses, 
    product_quantities, product_units, 
    product_prices, product_datetime, 
    product_scores, store_names, product_images) = ProductFormatter.get_products_info(datetime_products_list)

    products_formatted_names = ProductFormatter.set_products_formatted_names(product_names,product_quantities,product_units)
    products_formatted_images = ProductFormatter.set_products_formatted_images(product_images)
    stores_formatted_names = ProductFormatter.set_stores_formatted_names(store_names)
    search_home_results = ProductFormatter.sort_products_from_home_page(products_formatted_names, product_scores, 
                                                                        product_prices, store_addresses, 
                                                                        products_formatted_images)

    addresses_formatted_names = ProductFormatter.set_addresses_formatted_names(store_addresses)

    for product_dict in search_home_results:
        product_name_formatted = product_dict['product_name_formatted']
        search_details_results = ProductFormatter.sort_products_from_details_page(product_name_formatted, product_prices, 
                                                                                addresses_formatted_names, product_datetime, 
                                                                                products_formatted_names, stores_formatted_names, 
                                                                                products_formatted_images)

        product_dict['product_image_url'] = search_details_results[0]['product_image']
        for details_dict in search_details_results:
            details_dict.pop('product_image')

        product_dict['search_details_results'] = search_details_results

    data_dict = set_search_home_data(search_home_results, term)

    return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": data_dict  # Pass the dictionary directly
        }

if __name__ == "__main__":
    lambda_handler(None, None)

    # # test environment
    # json_file_path = "C:/Users/luis/Desktop/Kompru/repos/prototype_v0.1/input.json"
    # if os.path.exists(json_file_path):
    #     with open(json_file_path, 'r') as json_file:
    #         json_data = json.load(json_file)  # Load the JSON data into a Python dictionary
    #         data_dict = lambda_handler(json_data, None)

    #         with open('output.json', 'w') as json_file:
    #             json.dump(data_dict, json_file, indent=4)

    
        

