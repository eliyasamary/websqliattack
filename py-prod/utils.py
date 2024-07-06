import re
import requests
from bs4 import BeautifulSoup

def find_regex_in_soup(soup, pattern):
    html_content = str(soup)
    matches = re.findall(pattern, html_content)
    return matches


def check_if_react(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'lxml')

    is_react = False

    bundle_res = find_regex_in_soup(soup, "js/bundle.js")
    menifest_res = find_regex_in_soup(soup, "manifest.json")

    print(len(bundle_res))
    print(len(menifest_res))

    if len(bundle_res) > 0:
        is_react = True
    if len(menifest_res) > 0:
        is_react = True

    return is_react