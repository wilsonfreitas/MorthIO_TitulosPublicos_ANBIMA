# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from datetime import datetime as dt
from datetime import timedelta as timedelta
from itertools import dropwhile, ifilter
from StringIO import StringIO

from textparser import PortugueseRulesParser
pp = PortugueseRulesParser()

# Read in a page
date = dt.today() - timedelta(1)
url = 'http://www.anbima.com.br/merc_sec/arqs/ms{date}.txt'.format(date=dt.strftime(date, '%y%m%d'))
text = scraperwiki.scrape(url)

# parse page
text = StringIO(text)
_drop_first_3 = dropwhile(lambda x: x[0] < 3, enumerate(text))
_drop_empy = ifilter(lambda x: x[1].strip() is not '', _drop_first_3)
for c, line in _drop_empy:
    row = line.split('@')
    tit = dict(
        titulo=row[0],
        data_referencia=row[1],
        codigo_selic=row[2],
        data_base=row[3],
        data_vencimento=row[4],
        taxa_max=pp.parse(row[5]),
        taxa_min=pp.parse(row[6]),
        taxa_ind=pp.parse(row[7]),
        pu=pp.parse(row[8]),
        desvio_padrao=pp.parse(row[9])
    )
    scraperwiki.sqlite.save(
        unique_keys=['titulo', 'data_base', 'data_vencimento'],
        data=tit
    )
