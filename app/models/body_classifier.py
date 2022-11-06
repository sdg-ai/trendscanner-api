# -*- coding: utf-8 -*-
import requests
import os
import dotenv
dotenv.load_dotenv()

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class BodyNonbodyClassifier:
    """A class to define functions to train/test/predict and evaluate the noise classifier.
    """

    def __init__(self):
        #TODO: This should be initialized in a general __init__
        body_classifier_host = os.environ.get('BODY_CLASSIFIER_HOST')
        body_classifier_port = os.environ.get('BODY_CLASSIFIER_PORT')
        if(body_classifier_port):
            self.body_service = body_classifier_host + ':' + body_classifier_port
        else:
            self.body_service = body_classifier_host

    def predict(self, text):
        """
        A function which predicts whether the text is noise.
        :inputs:
            text: text to predict.
        :return:
            is_body: whether the text is body or non-body (noise).
        """
        data = {"text":text}
        logger.info("HERE")
        logger.info(data)

        #return "NOISE"
        response = requests.post(self.body_service + "/clean", json=data, timeout=30) 

        
        if(response.status_code == 200):
            return response.json()

        else:
            #TODO: Add proper error handling
            return "Error" 