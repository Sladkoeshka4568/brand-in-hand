import json


with open('filters/female_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_female = json.load(file)

with open('filters/male_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_male = json.load(file)
data_shoes = data_male + data_female

def search_data(manufacturer=None, size=None, price_min=None, price_max=None):
    result = []
    for f in data_shoes:
        if f['manufacturer'] == manufacturer:
            if int(f['price']) >= price_min and int(f['price']) <= price_max:
                for s in f['size']:
                    if size == int(s):
                        result.append(f)
                    else:
                        continue
    return result

def unic_name():
    result = []
    for d in data_shoes:
        result.append(d['manufacturer'])
    result = set(result)
    result = list(result)
    return result

def unic_model(brand, data):
    result = []
    for i in data:
        result.append(i['name'].split(f'{brand.upper()} ')[-1].strip())

    result = set(result)
    result = list(result)
    return result

def searth_model(brand, name_model, data):
    result = []
    for i in data:
        if i['name'].split(f'{brand.upper()} ')[-1].strip() == name_model:
            result.append(i)
    return result
