from input_settings import InputSettings
from utils.xlsx_utils import XlsxUtils

class AditionalQueriesAlgorithm:
    @staticmethod
    # param
    #   query is a tuple (arr, arr)
    def get_aditional_queries(query, keywords, file_sheet_synonym_words):
        search_key = query[0]
        unit = query[1]
        new_list = list()

        columns = XlsxUtils.get_columns_by_key(file_sheet_synonym_words, search_key)
        if columns is not None:
            for col in columns:
                new_list.append({(col, unit):keywords})

        return new_list