# -*- coding: utf-8 -*-
import re
class section:
    """
    Identify and extract rooms section from sentences/judgements files
    """
    def __init__(self):
        self.terms = ['sección']
    
    def get(self, text):
        """Process and extract rooms sections from sentences/judgements files
        params:
            text-> str: input text
        returns:
            section->list: list of room sections identified
        """
        terms = self.terms
        text = text.split('\n')[0:30]
        sections = []
        for line in text:
            line = line.strip()
            cond = any(line.lower().startswith(x) for x in terms)
            if cond:
                sections.append(line)
            else:
                continue
        if sections:
            section = sections
        else:
            section = []
        section = list(set([re.sub("\n", '', x.strip().upper()) for x in section]))
        return section

