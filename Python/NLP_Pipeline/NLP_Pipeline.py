import transformers
from transformers import pipeline
import numpy as np
import pandas as pd
import pickle
import torch

class NLP_Pipeline:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.named_entity_recognition_pipeline = pipeline("ner", aggregation_strategy="simple",
                                                     model="Jean-Baptiste/roberta-large-ner-english", device=device)
        self.zero_shot_classifier_pipeline = pipeline("zero-shot-classification",
                                                      model="facebook/bart-large-mnli", device=device)
        self.previous_subject = ""

    def nlp_get_subject(self, text_input):
        # first get all named entities from the text input
        entities = self.named_entity_recognition_pipeline(text_input)
        # get all location entities
        location_entities = [entity for entity in entities if entity['entity_group'] == 'LOC']
        subject = location_entities[0]['word'].strip() if len(
            location_entities) != 0 else None  # replace subject is there is a new location entity


        return subject, entities

    def nlp_get_major_category(self, text_input):
        # major categories, text info, videos, images, tweets,
        #major_categories = ["videos", "images", "tweets", "info"]
        major_categories = ["videos", "images", "info"]
        classes = self.zero_shot_classifier_pipeline(text_input, candidate_labels=major_categories)
        major_category = classes['labels'][0]
        major_category_score = classes['scores'][0]
        major_category = major_category.strip()
        return major_category, major_category_score
    def nlp_get_info_category_strat_multi_point_category(self, text_input):
        history_categories = ["history"]
        tourist_categories = ["tourist", "eat"]
        general_info_categories = ["general"]
        info_categories = history_categories + tourist_categories + general_info_categories
        classes = self.zero_shot_classifier_pipeline(text_input, candidate_labels=info_categories)
        major_category = classes['labels'][0]
        major_category_score = classes['scores'][0]
        average_distance = sum([major_category_score - i for i in classes['scores'][1:]]) / (len(classes['scores']))
        if major_category in history_categories:
            major_category = "history"
        if major_category in tourist_categories:
            major_category = "tourist"
        if major_category in general_info_categories:
            major_category = "general"
        return major_category, major_category_score

    def pipeline(self, text_input):
        # first get all named entities from the text input
        subject, entities = self.nlp_get_subject(text_input)
        if subject == None:
            subject = self.previous_subject
        self.previous_subject = subject
        text_input = text_input.replace(subject.lower(), subject.capitalize())
        # next, we need to figure out what the user is asking for
        major_category, major_category_score = self.nlp_get_major_category(text_input)

        # next, if we have a request for info, we need to break down what info they are asking for,
        if major_category == "info":
            major_category, major_category_score = self.nlp_get_info_category_strat_multi_point_category(text_input)

        return subject, major_category


    def __call__(self, text_input):
        return self.pipeline(text_input)