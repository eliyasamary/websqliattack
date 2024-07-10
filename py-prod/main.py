from utils import check_if_react
from non_react_scraping import non_react_scrape
from react_scraping import react_scraping
from non_blind_generator import non_blind
import logger
import time
from datetime import datetime

# Get current timestamp
current_timestamp = datetime.now().timestamp()

# Convert timestamp to a human-readable format
human_readable_time = datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')

file_readable_time = datetime.fromtimestamp(current_timestamp).strftime('%d-%m-%Y_%H-%M-%S')

filename = f"file-{file_readable_time}.txt"

logger.open_log_file(filename)

# input_url = 'https://online.shenkar.ac.il/'
input_url = 'http://localhost:3000/'

logger.log_start_stamp(human_readable_time, input_url)

is_react = check_if_react(input_url)

forms = []

if is_react == False:
    print("Not React Option")

    forms = non_react_scrape(input_url)
    
elif is_react == True:
    print("React Option")

    forms = react_scraping(input_url)

else :
    print("Error")

print(forms)

for form in forms:
    non_blind(form)
    
logger.log_end_stamp()
    
logger.close_log_file()
