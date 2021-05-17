import sys
import time

import requests
from bs4 import BeautifulSoup

from Constants import Constants


class VaccinParser:
    __location = ""
    __secondsForSleep = 5

    def __init__(self, location: str):
        self.__location = location

    def __TestConnection(self, client: requests.Session):
        status_code = client.get(Constants.URL).status_code
        if status_code != 200:
            print("Error: Website niet gevonden, status code {}.", status_code, file=sys.stderr)
            time.sleep(self.__secondsForSleep)
            self.__TestConnection(client)

    def __ParseCSRF(self, client: requests.Session) -> str:
        html = BeautifulSoup(client.get(Constants.URL).text, 'html.parser')
        token = html.find(class_="location-selector").find(attrs={"name": "_token"})
        return token['value']

    def __GetSearchResults(self, location: str) -> BeautifulSoup:
        def errorHandler(message):
            print(message, file=sys.stderr)
            time.sleep(self.__secondsForSleep)
            return self.__GetSearchResults(location)

        client = requests.session()
        self.__TestConnection(client)

        csrf = self.__ParseCSRF(client)
        data = {"_token": csrf, "location": location}
        r = client.post(Constants.URL + Constants.FORM, data=data)
        if r.status_code == 419:
            return errorHandler("Error: CSRF-token niet goed doorgegeven.")
        elif r.status_code != 200:
            return errorHandler("Error: onbekende status code: {}".format(r.status_code))
        else:
            return BeautifulSoup(r.text, 'html.parser')

    def GetVaccins(self) -> list:
        soup = self.__GetSearchResults(self.__location)
        praktijken = soup.find(id="locations-container").find_all(class_="card")
        if len(praktijken) == 0:
            return [0, []]

        results = []
        for praktijk in praktijken:
            if 'op-is-op' not in [s.strip() for s in praktijk.attrs['class']]:
                results.append(praktijk.find('h5').text.strip().replace('\n', ' '))

        return [len(praktijken), results]
