# Function to calculate the check digit for an EAN code
def calculate_check_digit(ean_str):
    total_sum = 0
    for i, digit in enumerate(ean_str[:-1]):
        if i % 2 == 0:
            total_sum += int(digit)
        else:
            total_sum += int(digit) * 3
    mod = total_sum % 10
    return 0 if mod == 0 else 10 - mod

# Function to validate an EAN code
def validate_ean(ean_str):
    if not ean_str.isdigit() or len(ean_str) != 13:
        return False
    return calculate_check_digit(ean_str) == int(ean_str[-1])

# New function to fabricate a sequence based on an invalid one
def fabricate_ean(invalid_ean):
    return "789" + invalid_ean[3:]


# Main code
if __name__ == "__main__":
    ean_code = input("Enter the EAN code for validation: ")
    if validate_ean(ean_code):
        print("Valid EAN code.")
    else:
        print("Invalid EAN code.")
