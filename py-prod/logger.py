# logger.py
import requests

file = None

def open_log_file(file_path):
    global file
    file = open(file_path, "a")  # Use "a" to append to the file

def close_log_file():
    global file
    if file:
        file.close()

def log_response(response_text):
    global file
    if file:
        file.write(f"Response text: {response_text}\n")
        print(f"Response text: {response_text}")

def make_request(url):
    response = requests.get(url)
    log_response(response.text)