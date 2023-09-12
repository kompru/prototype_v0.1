from fuzzywuzzy import fuzz
import pandas as pd
import re
import unidecode

# Portuguese stop words common in groceries and supermarket products
grocery_stop_words = set([
    "de", "do", "da", "em", "com", "para", "ml", "kg", "g", "l", "un", "pct", "und",
    "litro", "grama", "metro", "marca", "tipo" ])

# List of compound words that could be written differently
compound_words = [
    'extra virgem', 'extra-virgem'
    ]

# Negative keywords that lower the score if they are in the secondary but not in primary
# Unicode and lowercasing the keywords
negative_keywords = [unidecode.unidecode(keyword.lower()) for keyword in [
    'artificial', 'imitacao', 'generica', 'falso', 'repl', 'generico', 'sabor','aroma','suino','suina','sem','petisco','petiscos','caes','burguer', 'burger','hamburger', 'hamburguer',
    'light','zero','lactose', 'acucar','kit','caldo','knorr','salgadinho','cubos','desnatado','semidesnatado','lacfree','vegetal','em po','pao', 'diet', 'not', 'instantaneo','vegano','vegana','extrato',
    'composto','ceral','suplemento','cor','coloracao','chocolate','interfolhado','tempero','veg','racao'
]]

grocery_synonyms = {
    'interfolhas': 'interfolhado',
    'interfolha': 'interfolhado',  
    'interfolhadas': 'interfolhado',
    'longa vida': 'integral',
    'tolete': 'inteiro',
    'light': 'leve',
    'zero': '0',
    'diet': 'dieta',
    'desnatado': 'sem gordura',
    'fatiado': 'laminado',
    'fatiado': 'fatias',
    'picado': 'moído',
    'congelado': 'gelado',
    'orgânico': 'natural',
    'cru': 'in natura',
    'cozido': 'preparado',
    'natural': 'puro',
    'fluido':'líquido',
    'sólido': 'duro',
    'macio': 'suave',
    'forte': 'intenso',
    'doce': 'açucarado',
    'salgado': 'temperado',
    'pequeno': 'mini',
    'grande': 'maxi',
    'extra': 'adicional',
    'premium': 'especial',
    'fresco': 'novo',
    'seco': 'desidratado',
    'caseiro': 'artesanal',
    'tradicional': 'clássico',
    'instantâneo': 'rápido',
    'pronto': 'rápido',
    'vegetal': 'planta',
    'puro': 'sem mistura',
    'misturado': 'composto',
    'temperado': 'condimentado',
    'especiaria': 'condimento',
    'picante': 'apimentado',
    'azedo': 'cítrico',
    'bovina': 'bov',
    'sabão líquido':'detergente liquido',
    'lava louca':'detergente liquido',
    'lava loucas':'detergente liquido',
    'desinfetante': 'antisséptico',
    'limpador': 'higienizador',
    'alvejante': 'clareador',
    'amaciante': 'suavizante',
    'multiuso': 'polivalente',
    'esponja': 'fibra',
    'álcool': 'etanol',
    'removedor': 'desincrustante',
    'desodorante': 'neutralizador de odor',
    'vassoura': 'escova',
    'toalha': 'pano',
    'rodo': 'raspa-chão',
    'mop': 'esfregão',
    'lustra-móveis': 'polidor',
    'tira-manchas': 'desengordurante',
    'pano': 'flanela',
    'cera': 'polimento',
    'sabão': 'detergente',
    'saponáceo': 'limpador abrasivo'
}

grocery_synonyms = {unidecode.unidecode(k.lower()): unidecode.unidecode(v.lower()) for k, v in grocery_synonyms.items()}

# Remove Portuguese special characters
def normalize_special_chars(text):
    return unidecode.unidecode(text)

# Remove space and hyphen for known compound words
def handle_compound_words(text, compound_words_list):
    for word in compound_words_list:
        text = text.replace(word, word.replace(' ', '').replace('-', ''))
    return text

# Modify preprocess function to include an optional parameter for removing number terms
def preprocess(text, stop_words, negative_keywords, compound_words, grocery_synonyms):
    text = normalize_special_chars(text)
    text = handle_compound_words(text, compound_words)

    # Replace synonyms before tokenization
    for synonym, replacement in grocery_synonyms.items():
        text = re.sub(r'\b' + re.escape(synonym) + r'\b', replacement, text, flags=re.IGNORECASE)

    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    words = text.split()

    # Remove terms containing numbers
    words = [word for word in words if not any(char.isdigit() for char in word)]

    preserved_words = set()
    for keyword_set in [negative_keywords, compound_words, list(grocery_synonyms.keys()), list(grocery_synonyms.values())]:
        for keyword in keyword_set:
            preserved_words.update(keyword.split())

    # Remove stop words and further unidecode
    words = [unidecode.unidecode(word) for word in words if word.lower() not in stop_words or word.lower() in preserved_words]
    
    return ' '.join(words)

# Additional Scoring for missing keywords
# Additional Scoring for missing and negative keywords
# Additional Scoring for missing and negative keywords
def additional_scoring(primary, secondary, negative_keywords):
    primary_words = set(primary.split())
    secondary_words = set(secondary.split())
    missing_count = len(primary_words - secondary_words)
    
    negative_count = 0
    for neg_kw in negative_keywords:
        if ' ' in neg_kw:  # Compound keyword
            if neg_kw in secondary and neg_kw not in primary:
                negative_count += 1
        else:  # Single keyword
            if neg_kw in secondary_words and neg_kw not in primary_words:
                negative_count += 1

    return -5 * missing_count - 20 * negative_count

# Main function modified for batch processing
def main():
    # Read data from CSV
    df = pd.read_csv("2023-09-03 fuzzy_test - big.csv")

    # Initialize an empty list to store results
    results = []

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        print(f"Processing row {index + 1}")
        
        primary_product = preprocess(row['primary'], grocery_stop_words, negative_keywords, compound_words, grocery_synonyms)

        # Assuming secondary products are comma-separated in the CSV
        secondary_products_input = row['secondary'].split(',')
        secondary_products = [preprocess(product.strip(), grocery_stop_words, negative_keywords, compound_words, grocery_synonyms) for product in secondary_products_input]

        # Scoring logic here
        scores = []
        for original, tokenized in zip(secondary_products_input, secondary_products):
            score = fuzz.token_set_ratio(primary_product, tokenized)
            score += additional_scoring(primary_product, tokenized, negative_keywords)
            scores.append((original.strip(), tokenized, score))

        sorted_scores = sorted(scores, key=lambda x: x[2], reverse=True)
        
        # Append results (CHANGED)
        results.append({
            "primary": primary_product,
            "original secondary": original.strip(),
            "tokenized secondary": tokenized,
             "score": score
            })

    # Convert results to a DataFrame and save as CSV (CHANGED)
    result_df = pd.DataFrame(results)
    result_df.to_csv("sorted_scores_big.csv", index=False)
    print("Finished processing. Results saved to sorted_scores.csv.")

if __name__ == "__main__":
    main()