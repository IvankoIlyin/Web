import json

import requests
from bs4 import BeautifulSoup


def make_scrappey(url):
    url_scrappey = "https://article-extraction.newscatcherapi.xyz/scrappey"

    headers = {
        "accept": "application/json",
        "x-api-token": "nSnF5bTbD0QDI1GpM347JfXCCYs6fofkUrbRnkk6kN7xEaMXCl",
        "Content-Type": "application/json",
    }

    url_to_call = {"link": url}
    response = requests.post(url_scrappey, headers=headers, data=json.dumps(url_to_call))
    if response.status_code == 200:
        return BeautifulSoup(response.json()["html"], "html.parser")
    else:
        return print(f"Failed to make API call: {response.status_code}, {response.text}")


def make_scrapingbee(url):
    url_scrapingbee = "https://article-extraction.newscatcherapi.xyz/scrapingbee"

    headers = {
        "accept": "application/json",
        "x-api-token": "nSnF5bTbD0QDI1GpM347JfXCCYs6fofkUrbRnkk6kN7xEaMXCl",
        "Content-Type": "application/json",
    }

    url_to_call = {"link": url}
    response = requests.post(url_scrapingbee, headers=headers, data=json.dumps(url_to_call))
    if response.status_code == 200:
        return BeautifulSoup(response.json()["html"], "html.parser")
    else:
        return print(f"Failed to make API call: {response.status_code}, {response.text}")