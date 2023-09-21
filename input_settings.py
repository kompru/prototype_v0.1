import pandas as pd

class InputSettings:

    # Save products-out-stock in .xlsx?
    ONLY_AVAILABLE_PRODUCTS = False

    # Save match-search-term? in .xlsx?
    ONLY_MATCH_SEARCH_TERM_PRODUCTS = False

    # Save product-input-price = incompativel in .xlsx?
    ONLY_COMPATIBLE_PRICES_PRODUCTS = False
    
    DIRECTORY_PATH = "/Users/athos/Library/CloudStorage/GoogleDrive-athos@kompru.com/My Drive/06 Code/prototype_Luis/prototype_v0.1/"
 
    # Excel Header columns
    EXCEL_HEADER = ['k collected-at',         'k term',                   'k unit-input', 
                    'store-id',               'store-type',               'product-id',
                    'master-product-id',      'product-price',            'product-real-price',
                    'product-unit',           'k product-size',           'k unit-input-size',
                    'k product-input-unit',   'k product-input-price',    'k match-unit-input?',
                    'product-name',           'k term-in-product-name?',  'product-out-stock',
                    'step-quantity-in-grams']

    INPUT_SITE = True
    WORKBOOK_PATH = './Workbook.xlsx'

    df_name = pd.read_excel(WORKBOOK_PATH, sheet_name='name')
    df_address = pd.read_excel(WORKBOOK_PATH, sheet_name='address')
    df_query = pd.read_excel(WORKBOOK_PATH, sheet_name='query')
    df_spreadsheet_id = pd.read_excel(WORKBOOK_PATH, sheet_name='spreadsheet_id')

    for i in df_name.index:
        name = df_name.iloc[i]['Name']
        address = df_address.iloc[i]['Address']
        term = df_query.iloc[i]['Query']  
        query_dict = {(term, "kg"): ()}  
        spreadsheet_id = df_spreadsheet_id.iloc[i]['Spreadsheet_ID']

    SITE = [
        {
            "__NAME__": name,
            "__ADDRESS__": address,
            "__QUERY__": query_dict, 
            "__SPREADSHEET_ID__": spreadsheet_id
        }    
    ] 

    PAGE_TWO = [
        {
            "__ADDRESS__": address,
            "__TERM__":term,
            "__SPREADSHEET_ID__":spreadsheet_id,
            "__PRODUCT_NAME__":'omo sabao em po lavagem perfeita 800gr',
        }
    ]
            
        
        