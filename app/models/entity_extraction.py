#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import dotenv
dotenv.load_dotenv()

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class EntityExtractor:

    def __init__(self):
                #TODO: This should be initialized in a general __init__
        article_entities_host = os.environ.get('ARTICLE_ENTITIES_HOST')
        article_entities_port = os.environ.get('ARTICLE_ENTITIES_PORT')
        if(article_entities_port):
            self.entities_service = article_entities_host + ':' + article_entities_port
        else:
            self.entities_service = article_entities_host

    def get_annotations(self,text):
        data = {"text":text}
        response = requests.post(self.entities_service + "/entities", json=data, timeout=30) 

        if(response.status_code == 200):
            return response.json()

        else:
            #TODO: Add proper error handling
            return "Error"  

