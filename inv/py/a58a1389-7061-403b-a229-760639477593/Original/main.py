import requests
from bs4 import BeautifulSoup

def scrape_weapons(url):
    weapons = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', class_='Wikitable')
    rows = table.find_all('tr')

    current_type = ""
    for row in rows:
        type_cell = row.find('th', class_='navboxhead')
        if type_cell:
            current_type = type_cell.text.strip()
            continue

        trigger_cell = row.find('td', class_='navboxgroup')
        trigger = trigger_cell.text.strip() if trigger_cell else ""

        weapon_data = row.find_all('span', class_='tooltip-full')
        for data in weapon_data:
            anchors = data.find_all('a')
            if len(anchors) == 2:
                name = anchors[1]['href'].rsplit('/', 1)[-1]
                link = anchors[1]['href']
                weapon = {
                    "type": current_type,
                    "trigger": trigger,
                    "name": name,
                    "url": link
                }
                weapons.append(weapon)

    return weapons

url = 'https://warframe.fandom.com/wiki/Weapons#By_Type_'
weapons = scrape_weapons(url)
print(weapons)
