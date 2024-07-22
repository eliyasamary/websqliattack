from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from gloabls import payloads

def react_scraping(input_url):    
    chromedriver_path = "C:\\Program Files\\ChromeDriver\\chromedriver.exe"

    service = Service(executable_path=chromedriver_path)

    # For windows driver:
    driver = webdriver.Chrome(service=service)

    # For linux driver:
    # driver = webdriver.Chrome()

    driver.get(input_url)
    time.sleep(2)  # Wait for the page to load
    
    forms = driver.find_elements(By.TAG_NAME, "form")

    form_objects = []

    for form in forms:
        form_data = []
        input_fields = form.find_elements(By.TAG_NAME, "input")
        
        for input_field in input_fields:
            field_name = input_field.get_attribute("name")
            existing_value = input_field.get_attribute("value")
            if not existing_value:  # Only fill if the input is empty
                if field_name in payloads:
                    input_field.send_keys(payloads[field_name])
                    form_data.append({"name": field_name, "value": payloads[field_name]})
                else:
                    input_field.send_keys(payloads["basic"])
                    form_data.append({"name": field_name, "value": payloads["basic"]})
            else:
                form_data.append({"name": field_name, "value": existing_value})
        
        # Submit the form
        try:
            submit_button = form.find_element(By.TAG_NAME, "button")
            submit_button.click()
        except:
            print("No submit button found in form")
        
        time.sleep(5)  # Wait for the form submission to process

        # Capture requests
        for request in driver.requests:
            if request.response:
                if request.method == 'POST' and request.response.status_code == 401:
                    body = json.loads(request.body)
                    body_list = [{"name": key, "value": value} for key, value in body.items()]
                    for item in body_list:
                        if item["value"] == payloads["basic"]:
                            item["value"] = ''
                    temp_obj = {
                        "url": request.url,
                        "body": body_list
                    }
                    form_objects.append(temp_obj)
                    break  # Break after capturing the form submission request

    driver.quit()
    
    return form_objects

