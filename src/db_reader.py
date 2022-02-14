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
import pandas as pd

import os


import logging
import logging.config
import yaml

import src.utils

with open('./conf/config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('scraperLogger')

class Reader:

    def __init__(self) -> None:
        try:
            self.db = src.utils.get_mongo_access()
            logger.info('Xeno scraper initialization')
        except Exception as e:
            logger.error(f'db was not loaded {e}')

        self.data = []
        self.read()
        logger.info('bird db reading has finished')


    def read(self):

        cursor = self.db.find({})
        for document in cursor:
            self.data.append(document)

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(data=self.data)
        logger.info(f'df shape is {df.shape}')
        logger.info(f'df columns is {df.columns}')
        return df

    def save_json(self)-> None:
        pass

    

if __name__ == '__main__':

    pass