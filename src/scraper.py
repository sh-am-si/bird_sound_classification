from bs4 import BeautifulSoup 
import urllib
import requests
import html5lib
import json
import traceback

from datetime import datetime

from typing import Dict, List

import time
import numpy as np

import os

from pymongo import MongoClient

import logging
import logging.config
import yaml

import src.utils

with open('./conf/config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('scraperLogger')


def read_table(table, page:int) -> List[Dict]:
    dicts = []

    for ri, _row in enumerate(table):
        if _row:
            try:
                name_item = _row.find(attrs={'class' : "common-name"})
                name = name_item.find_next()
                t = _row.find_all(attrs={"class": "jp-type-single"})
                d = {
                    'name': name.text,
                    'sci_name': name.attrs['href'].replace('/species/',  ''),
                    'id': t[0].attrs['id'],
                    'filepath':  t[0].attrs['data-xc-filepath'], 
                    'data-id':  t[0].attrs['data-xc-id'],
                    'page': page,
                    'row': ri,
                    'audio': None
                }

                for i, td in enumerate(_row.findAll("td")):
                    if i==2:
                        try:
                            d['length'] = td.text.strip()
                        except:
                            d['length'] = None
                            logger.debug(f"reading page {page}, row {ri} 'length' wasn't read")
                    if i==3:
                        try:
                            d['contributor'] = td.find_next().text
                        except:
                            d['contributor'] = None
                            logger.debug(f"reading page {page}, row {ri} 'contributor' wasn't read")
                    if i==4:
                        try:
                            d['date'] = td.text
                        except:
                            d['date'] = None 
                            logger.debug(f"reading page {page}, row {ri} 'date' wasn't read")
                    if i==5:
                        try:
                            d['time'] = td.text
                        except:
                            d['time'] = None  
                            logger.debug(f"reading page {page}, row {ri} 'time' wasn't read")                              
                    if i==6:
                        try:
                            d['country'] = td.text
                        except:
                            d['country'] = None 
                            logger.debug(f"reading page {page}, row {ri} 'country' wasn't read")
                    if i==7:
                        try:
                            d['location'] = td.find_next().text
                        except:
                            d['location'] = None
                            logger.debug(f"reading page {page}, row {ri} 'location' wasn't read")
                    if i==8:
                        try:
                            d['elev'] = td.text
                        except:
                            d['elev'] = None 
                            logger.debug(f"reading page {page}, row {ri} 'elev' wasn't read")
                    if i==9:
                        try:
                            d['type'] = td.text
                        except:
                            d['type'] = None
                            logger.debug(f"reading page {page}, row {ri} 'type' wasn't read")
                            
                    if i==10:
                        try:
                            text = td.find_next().text.split('\n')
                            d['note'] = text[0]
                            for t in text:
                                if 'bird-seen:' in t:
                                    d['bird_seen'] = t.split(':')[1]
                                if 'playback-used:' in t:
                                    d['playback_used'] = t.split(':')[1]
                        except:
                            d['note'] = None 
                            logger.debug(f"reading page {page}, row {ri} 'note' wasn't read")
                    if i==11:
                        try:
                            d['class'] = td.find(attrs={'class':'selected'}).find_next().text
                        except:
                            d['class'] = None
                            logger.debug(f"reading page {page}, row {ri} 'class':'selected' wasn't read") 

                dicts.append(d)
    
            except Exception as e:
                logger.error(f"reading page {page}, row {ri} error {traceback.format_exc()} {e}")
    
    return dicts


class Xeno:

    def __init__(self) -> None:
        try:
            self.db = src.utils.get_mongo_access()
            logger.info('Xeno scraper initialization')
        except Exception as e:
            logger.error(f'db was not loaded {e}')

        self.pages = 22668# TODO get this value


    def get_url(self, page:int) -> str:
        assert 1 <= page <= self.pages 
        return f"https://xeno-canto.org/explore?dir=0&order=cnt&pg={page}"


    def get_table(self, page: int) -> Dict:
          
        req = requests.get(self.get_url(page))
        soup = BeautifulSoup(req.content, 'html5lib')

        table = soup.findAll(lambda tag: tag.name=='tbody')
        logger.info(f'Table was loaded {datetime.now().strftime("%H:%M:%S")}')
        if table and len(table)>1:
            return table[1]
        else:
            logger.error(f'Failed to read page {page} at {datetime.now().strftime("%H:%M:%S")}')


    def store_data(self, page: int):

        table = self.get_table(page=page)
        # print(table)
        dicts = read_table(table=table, page=page)
        # print(dicts)
        for d in dicts:
            self.db.insert_one(d)

    def get_last_page(self) -> int:

        page = 1
        cursor = self.db.find({})
        for document in cursor:
            page = max(page, document.get('page', 0))

        return page


    def start(self, time_sleep:int=2):
        first_page = self.get_last_page()
        for page in range(first_page, self.pages + 1):
            self.store_data(page=page)
            time.sleep(time_sleep)



if __name__ == '__main__':

    xeno = Xeno()
    xeno.store_data(page=1)



