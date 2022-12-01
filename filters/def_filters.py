import json


with open('filters/female_demi_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_female_demi = json.load(file)

with open('filters/female_summer_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_female_summer = json.load(file)

with open('filters/female_winter_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_female_winter = json.load(file)

with open('filters/male_demi_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_male_demi = json.load(file)

with open('filters/male_summer_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_male_summer = json.load(file)

with open('filters/male_winter_sneakers_data.json', 'r', encoding='utf-8') as file:
    data_male_winter = json.load(file)



data_shoes = data_male_winter + data_male_summer + data_male_demi + data_female_winter + data_female_summer + data_female_demi

def search_data(sex= None, season=None, manufacturer=None, size=None):
    result = []
    for f in data_shoes:
        if f['sex'] == sex.lower():
            if f['season'] == season:
                if f['manufacturer'] == manufacturer:
                    for s in f['size']:
                        if size == int(s):
                            result.append(f)
                        else:
                            continue
    return result

def search_data_button(sex= None, season=None):
    result = []
    for f in data_shoes:
        if f['sex'] == sex.lower():
            if f['season'] == season:
                result.append(f)
            else:
                continue
    return result
def unic_name(data):
    result = []
    for d in data:
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


