from bs4 import BeautifulSoup
import requests

def non_react_scrape(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'lxml')
    

    form_objects = []

    for form in soup.find_all('form'):
        form_object = {}

        action_url = form.get('action', '')
        form_object['url'] = action_url

        inputs = []
        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name', '')
            input_value = input_tag.get('value', '')
            inputs.append({'name': input_name, 'value': input_value})

        form_object['body'] = inputs

        form_objects.append(form_object)

    return form_objects