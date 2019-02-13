import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from string import Template

start_url = Template('https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=$SYMBOL')

def get_expirys(url):
    try:
        pg = requests.get(url)
        bsf = BeautifulSoup(pg.content, 'html5lib')
        exps = bsf.find('select', attrs={'name':'date'}).findAll('option')
        expirys = []
        for e in exps[1:]:
            expirys.append(e.contents[0].strip())
        return expirys
    except Exception as e:
        print(e)

def get_chain(url, date, symbol):
    try:
        url = f'{url}&date={date}'
        pg = requests.get(url)
        bsf = BeautifulSoup(pg.content, 'html5lib')
        table = bsf.find("table", attrs={'id':'octable'})
        table.find('thead')('tr')[0].extract()
        df = pd.read_html(table.prettify())
        df = df[0]
        df = df.replace('-', 0)
        name = f'{symbol}_{date}_{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx'
        df.to_excel(name)
        print(f'Saved {name} ...')
    except Exception as e:
        print(e)

def get_options_chain(symbol):
    url = start_url.substitute(SYMBOL=symbol)
    exps = get_expirys(url)
    for d in exps:
        get_chain(url, d, symbol)

def get_nifty():
    get_options_chain('NIFTY')

def get_bank_nifty():
    get_options_chain('BANKNIFTY')

if __name__ == '__main__':
    get_bank_nifty()
    get_nifty()