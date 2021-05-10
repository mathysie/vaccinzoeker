import locale
import random
import time
from datetime import datetime

from Notifier import Notifier
from VaccinParser import VaccinParser

CANCELLED = 'Cancelled'

locale.setlocale(locale.LC_ALL, '')


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

    parser = VaccinParser(location)

    while True:
        vaccins = parser.GetVaccins()
        if len(vaccins[1]) > 0:
            Notifier.Notify(vaccins[1])
        else:
            print("{}\t{} praktijken: geen vaccin!".format(datetime.now().strftime("%d %b %Y %H:%M:%S"), vaccins[0]))

        time.sleep(random.gauss(30, 3))


main()
