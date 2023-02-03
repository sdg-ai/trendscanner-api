# -*- coding: utf-8 -*-
import dotenv, os
import requests
dotenv.load_dotenv()

class TrendsInnovationClassifier:
    """ CHANGE THIS: A class to define functions to train/test/predict and evalute the classifier.
    """

    def __init__(self):

        #TODO: This should be initialized in a general __init__
        trends_innovations_host = os.environ.get('TRENDS_INNOVATIONS_HOST')
        trends_innovations_port = os.environ.get('TRENDS_INNOVATIONS_PORT')
        if(trends_innovations_port.isnumeric()):
            self.trends_service = trends_innovations_host + ':' + trends_innovations_port
        else:
            self.trends_service = trends_innovations_host

    def scan_predict(self, text):
        """ Function to scan over three sentence blocks and make predictions
        :arg text (str) - input text string
        @:return array([{"text": <text-snippet>,
                        "indices": [(<start>, <end>)],
                         "prediction": <tag str>}]"""
        
        data = {"text":text}
        response = requests.post(self.trends_service + "/predictions", json=data, timeout=30)

        if(response.status_code == 200):
            return response.json()

        else:
            #TODO: Add proper error handling
            return "Error"
