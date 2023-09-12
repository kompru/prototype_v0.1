import pandas as pd
from ast import literal_eval  # <-- Added this import

class InputSettings:
# Load the Excel Workbook
    workbook_path = './Workbook.xlsx'

    # Read sheets into dataframes
    df_name = pd.read_excel(workbook_path, sheet_name='name')
    df_address = pd.read_excel(workbook_path, sheet_name='address')
    df_query = pd.read_excel(workbook_path, sheet_name='query')
    df_spreadsheet_id = pd.read_excel(workbook_path, sheet_name='spreadsheet_id')

    print(df_address)
    print(df_query)

    # Create CLIENTS dynamically
    CLIENTS = []
    for i in df_name.index:
        # Convert the string-formatted 'Query' to an actual dictionary
        cell_content = df_query.iloc[i]['Query']  # <-- New line
        query_dict = {(cell_content, "kg"): ()}   # <-- Changed this line
        print(query_dict)
        client_dict = {
            "__NAME__": df_name.iloc[i]['Name'],
            "__ADDRESS__": df_address.iloc[i]['Address'],
            "__QUERY__": query_dict,  # <-- Changed this line
            "__SPREADSHEET_ID__": df_spreadsheet_id.iloc[i]['Spreadsheet_ID']
        }
        CLIENTS.append(client_dict)


    # Just remember to user / instead of \
    DICTIONARY_FILE_PATH = '/Users/athos/Library/CloudStorage/GoogleDrive-athos@kompru.com/My Drive/06 Code/Github/rappi-scrapper_v2/rappi-scrapper/dictionary.xlsx'

    # THE UNIT IS SECONDS 60 * 2 = 120 seconds = 2 minutes
    # 1 HOUR = 60 * 60
    # 2 HOURS = 60 * 60 * 2
    AUTO_SCRIPT_SCHEDULER_TIME = 1

    # Save products-out-stock in .xlsx?
    # True  -> Save oducts-out-stock = False in .xlsx file
    # False -> Save pnly proroducts-out-stock = True or False in .xlsx file
    ONLY_AVAILABLE_PRODUCTS = False

    # Save match-search-term? in .xlsx?
    # True  -> Save only match-search-term? = True in .xlsx file
    # False -> Save match-search-term? = True or False in .xlsx file
    ONLY_MATCH_SEARCH_TERM_PRODUCTS = False

    # Save product-input-price = incompativel in .xlsx?
    # True  -> Save only product-input-price != incompativel in .xlsx file
    # False -> Save all product-input-price in .xlsx file
    ONLY_COMPATIBLE_PRICES_PRODUCTS = False
    
    DIRECTORY_PATH = "/Users/athos/Library/CloudStorage/GoogleDrive-athos@kompru.com/My Drive/06 Code/Barra-de-busca-para-itens-MVP/rappi-scrapper/"

    
    # Excel Header columns
    EXCEL_HEADER = ['k collected-at',         'k term',                   'k unit-input', 
                    'store-id',               'store-type',               'product-id',
                    'master-product-id',      'product-price',            'product-real-price',
                    'product-unit',           'k product-size',           'k unit-input-size',
                    'k product-input-unit',   'k product-input-price',    'k match-unit-input?',
                    'product-name',           'k term-in-product-name?',  'product-out-stock',
                    'step-quantity-in-grams']