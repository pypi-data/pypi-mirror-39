import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.prezzibenzina.it/distributori/{}"

class PrezziBenzinaPy():

    def get_by_id(self, id):
        gas_list = []
        r = requests.get(BASE_URL.format(id))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('div', {"class": "st_reports_row"})
        for row in table[1:]:
            gas = {
                'date': row.find('div', {"class": "st_reports_data"}).text,
                'fuel': row.find('div', {"class": "st_reports_fuel"}).text,
                'service': row.find('div', {"class": "st_reports_service"}).text,
                'price': row.find('div', {"class": "st_reports_price"}).text
            }
            gas_list.append(gas)
        return gas_list

    def get_station_name(self, id):
        r = requests.get(BASE_URL.format(id))
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.find('div', {"class": "st_name"}).text
