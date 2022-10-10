# -*- coding: utf-8 -*-
import re
class filingID:
    """Identify, extract and format filing id from the input text"""
    def __init__(self):
        self.terms = ['rad', 'expediente', 'ref', 'casación']
    
    def get(self, text):
        """
        identify and  filing id in the input text through patterns matching and
        returned as output.
        params:
            - text-> str: input text
        returns:
            num->str: Filing number as string.
        """
        terms = self.terms
        text = text.split('\n')[0:30]
        filing_no = []
        for line in text:
            line = line.strip()
            cond = any(line.lower().startswith(x) for x in terms)
            if cond:
                filing_no.append(line)
            else:
                continue
        if filing_no:
            # num = 'Radicación n." 11001-22-10-000-2019-00519-01'
            num = filing_no[0]
            num = re.findall("[\d+](.*)", num)
            if num:
                num = num[0]
            else:
                num = ''
        else:
            num = ''
        return num
