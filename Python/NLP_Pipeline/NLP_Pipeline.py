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

    def nlp_get_subject(self, text_input):
        global subject
        # first get all named entities from the text input
        entities = self.named_entity_recognition_pipeline(text_input)
        # get all location entities
        location_entities = [entity for entity in entities if entity['entity_group'] == 'LOC']
        subject = location_entities[0]['word'] if len(
            location_entities) != 0 else subject  # replace subject is there is a new location entity
        return subject, entities