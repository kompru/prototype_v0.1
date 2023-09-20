def format_address(input_str):
    # Split the string into words
    words = input_address.split()

    # Capitalize the first letter of each word and join them
    capitalized_words = [word.capitalize() for word in words]

    # Join the capitalized words into a single string
    formatted_address = ''.join(capitalized_words)

    # Remove spaces, commas, dots, and hyphens
    formatted_address = formatted_address.replace(' ', '').replace(',', '').replace('.', '').replace('-', '')

    return formatted_address

# Example usage:
input_address = "Rua Doadora Eliane Stancioli, 35 - Buritis, Belo Horizonte - MG, 30575-790"
result = format_address(input_address)
print(result)