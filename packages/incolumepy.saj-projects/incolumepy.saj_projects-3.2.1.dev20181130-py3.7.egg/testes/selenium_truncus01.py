#!/usr/bin/env python
#  -*- coding: utf-8 -*-
__author__ = "@britodfbr"
__copyright__ = "Copyright 2007, incolume.com.br"
__credits__ = ["Ricardo Brito do Nascimento"]
__license__ = "GPL"
__version__ = "1.0a"
__maintainer__ = "@britodfbr"
__email__ = "contato@incolume.com.br"
__status__ = "Production"


import logging
import pandas as pd
import numpy as np
import logging.handlers
from src.incolumepy.saj_projects.legis import Legis
from src.incolumepy.saj_projects.selenium_multaccess import Scrapy_camara

def exemplo01():
    a = Scrapy_camara()
    a.numero = 74
    a.ano = 1889
    try:
        logging.debug('starting...')
        a.query_form()
        print(a.collection_query)
        a.fill_metadados()
        print(a.collection_metadados)
        # a.fill_content()
        # a.collection2jsonfile()
    except (AttributeError) as e:
        logging.error(e)
        raise
        print(e)
    finally:
        a.firefox.quit()

def exemplo02():
    a = Scrapy_camara(ano=1900)
    #a.numero = 74
    try:
        logging.debug('starting...')
        a.query_form()
        print(a.collection_query)
        a.fill_metadados()
        print(a.collection_metadados)
        # a.fill_content()
        # a.collection2jsonfile()
    except (AttributeError) as e:
        logging.error(e)
        raise
        print(e)
    finally:
        a.firefox.quit()

def exemplo03():
    a = Scrapy_camara()
    a.numero = 113
    a.ano = 1889
    try:
        logging.debug('starting...')
        a.query_form()
        print(a.collection_query)
        print('collection_query', len(a.collection_query))
        # ---- ok até aqui ----
        #a.toFile(tipo='json', collection='query')
        a.fill_metadados()
        print(a.collection_metadados)
        print('collection_metadados', len(a.collection_metadados))
        # a.toFile(tipo='json', collection='metadados')
        # a.fill_content()
        # a.collection2jsonfile()
    except:
       raise
    finally:
        a.firefox.quit()

if __name__ == '__main__':
    #exemplo01()
    #exemplo02()
    exemplo03()

    pass
