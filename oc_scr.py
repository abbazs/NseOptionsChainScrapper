import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

start_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY'

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

def get_chain(date):
    try:
        url = f'{start_url}&date={date}'
        pg = requests.get(url)
        bsf = BeautifulSoup(pg.content, 'html5lib')
        table = bsf.find("table", attrs={'id':'octable'})
        table.find('thead')('tr')[0].extract()
        df = pd.read_html(table.prettify())
        df = df[0]
        df = df.replace('-', 0)
        df.to_excel(f'banknifty_{date}_{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx')
        print('Saved ...')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    exps = get_expirys(start_url)
    for d in exps:
        get_chain(d)