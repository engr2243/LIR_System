# -*- coding: utf-8 -*-
import re
class room:
    """
    Identify and extract court rooms from the input text
    param:
        spacy_model-> object: spacy model for spanish text
    """
    def __init__(self, spacy_model):
        self.spacy_model = spacy_model
    
    def get(self, text):
        """
        Extract court rooms mentioined in text using spacy model by loc entity
        params:
            text-> str: input sentence text in plain
        returns:
            rooms-> list: rooms identified in text
        """
        text = '\n'.join(text.split("\n")[0:40])
        x = self.spacy_model(text)
        rooms = [ee.text for ee in x.ents if ee.label_=='LOC']
        rooms = [x for x in rooms if x.lower().strip().startswith('sala ')]
        if rooms:
            rooms = rooms
        else:
            rooms = []
        rooms = list(set([re.sub("\n", '', x.strip().upper()) for x in rooms]))
        return rooms

