import json
import requests
from bs4 import BeautifulSoup
import datetime
import random
import time

def get_citation(name):
    prefix = "https://scholar.google.com/scholar?q=allintitle:"
    name = name.replace('^', '')
    name = name.replace('$', '')
    scholar_link = prefix + name

    page = requests.get(scholar_link).text
    soup = BeautifulSoup(page, "html.parser")

    if "robot" in page:
        raise ConnectionRefusedError

    cite = soup.find_all("a", href=lambda value: value and value.startswith("/scholar?cites="))
    s = cite[0].text if len(cite) >= 1 else "0"
    s = int(''.join(c for c in s if c.isdigit()))

    return s

today = datetime.date.today()
n_upd = random.randint(20, 30)
print('n_upd =', n_upd)

with open('.github/citation/citation.json', 'r') as f:
    table = json.load(f)

sorted_table = sorted(table.items(), key=lambda item: item[1]['last update'])

if len(sorted_table) < n_upd:
    n_upd = len(sorted_table)

for i in range(n_upd):
    name = sorted_table[i][0]
    item = sorted_table[i][1]
    try:
        cite = get_citation(name)
        item['citation'] = cite
        item['last update'] = today.strftime("%Y-%m-%d")
        print('"' + name + '" updated,', 'citation =', cite)
        if i < n_upd - 1:
            time.sleep(random.randint(10, 80))
    except ConnectionRefusedError:
        print('updating "' + name + '" failed')
        break

table = dict(sorted_table)
table = dict(sorted(table.items(), key=lambda item: item[1]['last update']))

with open('.github/citation/citation.json', 'w') as f:
    json.dump(table, f)
