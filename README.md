# Vaccinzoeker
Een geautomatiseerde zoeker van overgebleven COVID-vaccins op [prullenbakvaccin.nl](https://prullenbakvaccin.nl).

## Werking
Eerst wordt naar een locatie gevraagd. Daar kan een postcode of plaatsnaam ingevuld worden. Daarna wordt gevraagd om de ingevulde locatie te bevestigen. Prullenbakvaccin.nl accepteert vrijwel elke invoer als een plaatsnaam, vandaar dat de geldigheid van de invoer niet automatisch gecontroleerd kan worden.

De ingevoerde plaatsnaam wordt frequent (± iedere 30 seconden) op prullenbakvaccin.nl ingevuld. Als er vaccins bij huisartsen in de buurt over blijken te zijn, dan wordt een melding naar Windows gestuurd.

## Vereisten
Getest op Windows 10.

## Installatie
Installeer eerst [PyInstaller](https://www.pyinstaller.org/). Daarna moet het script `CreateExecutable.ps1` met Powershell gedraaid worden. Het is getest met Powershell 7.1 en Python 3.8.

Er verschijnt dan een map 'dist' met daarin de executable en het benodigde plaatje.

## Kudo's
Het programma is tot stand gekomen met behulp van de volgende externe pakketten:
- [Python](https://www.python.org/)
- [Python Requests](https://docs.python-requests.org)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Juicy Fish](https://icon-icons.com/nl/pictogram/injectie-vaccin-vaccinatie-naald-genezen-coronavirus/141460)
- [Prullenbakvaccin.nl](https://prullenbakvaccin.nl)
