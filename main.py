import requests
from bs4 import BeautifulSoup as bs
import csv


class RequestError(Exception):
    pass


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise RequestError


def get_rates(html):
    soup = bs(html, "lxml")
    data = soup.find("table", class_="data")
    rates = data.find_all("tr")
    return [[value.text for value in currency.find_all("td")] for currency in rates[1:]]


def save_in_csv(filename, matrix):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in matrix:
            writer.writerow(row)


save_in_csv("Валюты.csv", get_rates(get_html("https://cbr.ru/currency_base/daily/")))
