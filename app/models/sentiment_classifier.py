# -*- coding: utf-8 -*-
import dotenv, os
import requests
dotenv.load_dotenv()

class SentimentInterface:
	# sentiment interface class to use SentimentClassifier
    def __init__(self):
                #TODO: This should be initialized in a general __init__
        article_sentiment_host = os.environ.get('ARTICLE_SENTIMENT_HOST')
        article_sentiment_port = os.environ.get('ARTICLE_SENTIMENT_PORT')
        if(article_sentiment_port.isnumeric()):
            self.sentiment_service = article_sentiment_host + ':' + article_sentiment_port
        else:
            self.sentiment_service = article_sentiment_host

    def text_to_sentiment(self, text_lst):        
        data = {"text":text_lst}
        response = requests.post(self.sentiment_service + "/sentiment", json=data, timeout=30) 

        if(response.status_code == 200):
            return response.json()

        else:
            #TODO: Add proper error handling
            return "Error" 
