from bs4 import BeautifulSoup 
import urllib
import requests
import html5lib
import json
import traceback

from typing import Dict

import time
import numpy as np

import os

from pymongo import MongoClient

import logging
import logging.config
import yaml

with open('./conf/config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger('scraperLogger')

logger.info('This is an info message')
logger.debug('This is a debug message')
logger.error('This is an error message')


class Xeno:

    def __init__(self) -> None:
        logger.info('This is an info message')
        pass

    def read(self, page: int) -> Dict: