import json

directory_path = "./data"
file_name = 'input'
json_file_name = f'{directory_path}/{file_name}'

try:
    with open(f'{json_file_name}.json', 'r') as json_file:
        json_data = json.load(json_file)
        json_file.close()
except FileNotFoundError as err:
    print(f'Error: {err}')

# print(json_data)

for key,value in json_data.items():
    if key == 'address':
        address = value

print(address)