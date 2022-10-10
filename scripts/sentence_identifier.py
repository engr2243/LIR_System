# -*- coding: utf-8 -*-

import re
class sentenceID:
    """Extract sentence id by pattern matching"""
    def __init__(self):
        self.pattern = "[A-Z]+[0-9]+\S[\d]{4}|[A-Z]+\s[0-9]+\S[\d]{4}|[A-Z]+[0-9]+\S[\d]+\S[\d]|[A-Z]+\S[\d]{4}"
    
    def get(self, text):
        """
        Function to extract sentence id by regex pattern matching.
        params:
            - text->str: input string
        returns
            - sent_id->str: returns sentence id as string
        """
        text = '\n'.join(text.split('\n')[0:40])
        text = re.sub(" - |- | -", '-', text)
        sent_id = re.findall(self.pattern, text)
        if sent_id:
            sent_id = sent_id[0]
            if len(sent_id)<18:
                pass
            else:
                sent_id=''
        else:
            sent_id = ''
        return sent_id