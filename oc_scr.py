import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

start_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=BANKNIFTY'


def get_chain():
    try:
        pg = requests.get(start_url)
        bsf = BeautifulSoup(pg.content, 'html5lib')
        tables = bsf.findAll('table')
        table = bsf.find("table", attrs={'id':'octable'})
        table.find('thead')('tr')[0].extract()
        lrow = table('tbody')[0]('tr')[-1].extract()
        df = pd.read_html(table.prettify())
        df = df[0]
        df = df.replace('-', 0)
        df.to_excel(f'banknifty_{datetime.now():%Y-%m-%d_%H-%M-%S}.xlsx')
        print('Saved ...')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    get_chain()