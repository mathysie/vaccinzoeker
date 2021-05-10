import locale
import random
import sys
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

from Constants import Constants

secondsForSleep = 5
CANCELLED = 'Cancelled'

locale.setlocale(locale.LC_ALL, '')


def TestConnection(client: requests.Session):
    status_code = client.get(Constants.URL).status_code
    if status_code != 200:
        print("Error: Website niet gevonden, status code {}.", status_code, file=sys.stderr)
        time.sleep(secondsForSleep)
        TestConnection(client)


def ParseCSRF(client: requests.Session) -> str:
    html = BeautifulSoup(client.get(Constants.URL).text, 'html.parser')
    token = html.find(class_="location-selector").find(attrs={"name": "_token"})
    return token['value']


def GetSearchResults(location: str) -> BeautifulSoup:
    def errorHandler(message):
        print(message, file=sys.stderr)
        time.sleep(secondsForSleep)
        GetSearchResults(location)

    client = requests.session()
    TestConnection(client)

    csrf = ParseCSRF(client)
    data = {"_token": csrf, "location": location}
    r = client.post(Constants.URL + Constants.FORM, data=data)
    if r.status_code == 419:
        errorHandler("Error: CSRF-token niet goed doorgegeven.")
    elif r.status_code != 200:
        errorHandler("Error: onbekende status code: {}".format(r.status_code))
    else:
        return BeautifulSoup(r.text, 'html.parser')


def GetVaccins(soup: BeautifulSoup) -> list:
    praktijken = soup.find(id="locations-container").find_all(class_="card")
    if len(praktijken) == 0:
        return [0, []]

    results = []
    for praktijk in praktijken:
        if 'op-is-op' in praktijk.attrs['class']:
            results.append(praktijk.find('h5').text.strip().replace('\n', ' '))

    return [len(praktijken), results]


def NotifyUser(vaccins: list):
    text = ""
    for vaccin in vaccins:
        text += vaccin + '\n'

    n = ToastNotifier()
    n.show_toast(
        title="{} vaccins gevonden!\n".format(len(vaccins)),
        msg=text,
        icon_path='../img/Spuit.ico',
        duration=20,
        threaded=True
    )


def GetLocation() -> str:
    asking = True
    while asking:
        location = input("Welk gebied wil je zoeken?\n")
        confirm = input("Klopt locatie '{}'?\n[J]=Ja, [N]=Nee, [C]=Cancel\n".format(location))
        if confirm.lower() == 'j':
            asking = False
        elif confirm.lower() == 'c':
            asking = False
            location = CANCELLED

    return location


def main():
    location = GetLocation()
    if (location.lower() == CANCELLED):
        return

    while True:
        soup = GetSearchResults(location)
        vaccins = GetVaccins(soup)
        if len(vaccins[1]) > 0:
            NotifyUser(vaccins[1])
        else:
            print("{}\t{} praktijken: geen vaccin!".format(datetime.now().strftime("%d %b %Y %H:%M:%S"), vaccins[0]))

        time.sleep(random.gauss(30, 3))


main()
