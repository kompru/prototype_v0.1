from collections import Counter, defaultdict 
import unicodedata
import json

class ProductFormatter:

    def sortProductsbyScore():
        pass
    
    def getTermPricesAndStores(product_name:str, _product_prices:list, _product_stores:list, _datetime_search:list, _products_formatted_names:list )->dict:
        formatted_names_by_term = defaultdict(list)
        for formatted_name, price, store, datetime in zip(_products_formatted_names, _product_prices, _product_stores, _datetime_search):
            if  product_name == formatted_name:
                product_dict = {}
                product_dict['product-name'] = formatted_name
                product_dict['price'] = price
                product_dict['store'] = store
                product_dict['collected-in'] = datetime
                formatted_names_by_term[product_name].append(product_dict)

        return formatted_names_by_term

    def getProductsLowestPrice(_product_prices:list, _products_formatted_names:list)->dict:
        formatted_names_by_price = defaultdict(list)
        for formatted_name, price in zip(_products_formatted_names, _product_prices):
            if  len(formatted_names_by_price[formatted_name]) == 0:
                product_dict = {}
                product_dict['product-name'] = formatted_name
                product_dict['start-price'] = price
                product_dict['stores'] = 1
                formatted_names_by_price[formatted_name].append(product_dict)
            else:
                product_dict = formatted_names_by_price[formatted_name][0]
                product_dict['stores'] += 1
                actual_price = product_dict['start-price']
                if price < actual_price:
                    product_dict['start-price'] = price

        return formatted_names_by_price

    def setProductsFormattedNames(product_names:list, quantities:list,units:list)->list:
        # Format product names first, considering quantity and unit
        products_formatted_names = []
        for name, qty, unit in zip(product_names, quantities, units):
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
            formatted_name = name.lower().strip()

            if qty is not None and float(qty) != 0.0:
                formatted_name = f"{formatted_name} {qty}{unit}"
            
            products_formatted_names.append(formatted_name)
        return products_formatted_names

    def getProductsInfo(products_list:list)->tuple:
        product_names = []
        store_addresses = []
        product_quantities = []
        product_units = []
        product_prices = []
        product_datetime = []
        product_scores = []
        for products_dict in products_list:
            for header,value in products_dict.items():
                if header == 'product-name':
                    product_names.append(value)
                elif header == 'store-address':
                    store_addresses.append(value)
                elif header == 'product-quantity':
                    product_quantities.append(value)
                elif header == 'product-unit':
                    product_units.append(value)
                elif header == 'product-price':
                    product_prices.append(value)
                elif header == 'k collected-at':
                    product_datetime.append(value)
                elif header == 'product-score':
                    product_scores.append(value)

        return product_names, store_addresses, product_quantities, product_units, product_prices, product_datetime, product_scores
    
class JsonFile:
    def createJsonFile(products_list:list, file_path:str):
        _products_list = []
        for product in products_list:
            _products_list.append(product)
        with open(f'{file_path}.json', 'w') as fp:
            json.dump(_products_list, fp, indent=1)
            fp.close()

    def format_address(input_address):
        # Split the string into words
        words = input_address.split()

        # Capitalize the first letter of each word and join them
        capitalized_words = [word.capitalize() for word in words]

        # Join the capitalized words into a single string
        formatted_address = ''.join(capitalized_words)

        # Remove spaces, commas, dots, and hyphens
        formatted_address = formatted_address.replace(' ', '').replace(',', '').replace('.', '').replace('-', '')

        return formatted_address