from bs4 import BeautifulSoup
import requests

def non_react_scrape(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'lxml')
    
    # form_objects = soup.findAll('form')

    form_objects = []

    for form in soup.find_all('form'):
        form_object = {}

        # Get form action URL
        action_url = form.get('action', '')
        form_object['url'] = action_url

        # Get form inputs
        inputs = []
        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name', '')
            input_value = input_tag.get('value', '')
            inputs.append({'name': input_name, 'value': input_value})

        form_object['body'] = inputs

        # Store the form object
        form_objects.append(form_object)

    # Print all captured form_objects
    # for idx, form in enumerate(form_objects):
    #     print(f"Form {idx + 1}:")
    #     print(f"Action URL: {form['url']}")
    #     print("Inputs:")
    #     for input_data in form['body']:
    #         print(f" - Name: {input_data['name']}, Value: {input_data['value']}")
    #     print()

    return form_objects