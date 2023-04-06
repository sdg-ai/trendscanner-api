# -*- coding: utf-8 -*-

import os
import json
import csv
from .trends_innovation_classifier import TrendsInnovationClassifier
from .sentiment_classifier import SentimentInterface
from .body_classifier import BodyNonbodyClassifier
from .entity_extraction import EntityExtractor
import nltk


_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)

with open(get_data('country_codes.json'), 'rt', encoding='utf-8', errors='ignore') as f:
    country_code_map = json.load(f)

class EnrichmentCoordinator:
    def __init__(self, locs_disambiguation=False):
        # self.d2c = Doc2Climate()
        self.d2t = TrendsInnovationClassifier()
        self.d2s = SentimentInterface()
        self.entity_recognition = EntityExtractor()
        self.cleaner = BodyNonbodyClassifier()
        self.locs_flag = locs_disambiguation
        self.locs = None

        nltk.download('punkt')

        if self.locs_flag:
            from graphlocation.location import Locations
            self.locs = Locations()

            
    def span_tokenize(self, text):
        text_objects = []
        sents = nltk.sent_tokenize(text)
        offset = 0
        for sent in sents:
            offset = text.find(sent, offset)
            text_obj = {'string_indices': [offset,offset + len(sent)], 'text': sent}
            text_objects.append(text_obj)
            offset += len(sent)
        return text_objects
    
    
    def clean_text(self, text):
        sentences = self.span_tokenize(text)
        cleaned_sentences = []
        for sentence in sentences:
            prediction = self.cleaner.predict(sentence)
            if prediction == 'BODY':
                cleaned_sentences.append(sentence)
        return ' '.join(cleaned_sentences)


    def process(self, article_text, debug=False):
        article_text = self.clean_text(article_text)
        trend_results = self.d2t.scan_predict(article_text)
        sentiment = self.d2s.text_to_sentiment(article_text)[0]
        # entities = self.entity_recognition.get_annotations(article_text)
        entities = []
        entities_dedupe_set = set()
        for item in trend_results:
            item['extract_sentiment'] = self.d2s.text_to_sentiment(item['text'])[0]
            entity_list = []
            for entity in self.entity_recognition.get_annotations(item['text']):
                if self.locs_flag:
                    if entity[1] == 'GPE' or\
                            (entity[2]['entityType'] and 'Place' in entity[2]['entityType']):
                        loc_class = self.locs.get_location(entity[0])
                        if loc_class.country:
                            entity[2]['country'] = country_code_map[loc_class.country.lower()][0]

                if entity[0] not in entity_list:
                    entity_list.append(entity[0])
                    if entity[0] not in entities_dedupe_set:
                        entities.append(entity)
                        entities_dedupe_set.add(entity[0])

            item['extract_entities'] = entity_list
            if not debug:
                del item['text']
            # print(item)

        results = {'trend_extractions': trend_results,
                   'article_sentiment': sentiment,
                   'article_entities': entities,
                   # TODO: replace with real model
                   'climate_relevance_score':0.95}

        print(len(trend_results))
        return results

