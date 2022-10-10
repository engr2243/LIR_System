#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import spacy
nlp = spacy.load("es_core_news_lg")

class get_name:
    """
    Match and extract names from the text using NER and Logic based
    approach.
    param:
        spacy_model-> object: spacy model for spanish text
    """
    def __init__(self, spacy_model):
        self.spacy_model = spacy_model
        # Pattern used in matchin Judges Names
        self.pattern1a = 'magistrada|magistrados|magistradas|conjuez|Consejero'
        self.pattern1b = 'ponentes|ponenta'
        self.pattern2 = 'magistrada|magistrados|magistradas|ponentes|ponente'
    
    def name_boundry(self, text, reshape_boundry = False):
        """
        Identify a list of lines return as list, which contains the text lines 
        with judges names
        Prams:
            - text->str: input text
            - reshape_boundry(optional): bolean(True/False): Used in case the first
              lines does not match the patterns for judge names which allow to reshape
              text boudry to search names containing lines at last page
        returns: a list of sentences containing person names
        """
        txt_tmp = text.strip().lower()
        txt_tmp = re.sub(self.pattern1a, 'magistrado', txt_tmp)
        txt_tmp = re.sub(self.pattern1b, 'ponente', txt_tmp)
        cond = ('magistrado ponente' in txt_tmp) or ('magistradoponente' in txt_tmp)
        lines = [line.strip() for line in text.split('\n') if line.strip()!='']
        if cond:
            index = [txt_tmp.split('\n').index(x) for x in txt_tmp.split('\n')
                     if (('magistrado ponente' in x) or ('magistradoponente' in x))]
            index = index[0]
            if (index-2)>2:
                name_boundry =  lines[index-2:index+3]
            else:
                name_boundry =  lines[index-1:index+2]
        else:
            name_boundry = lines[0:10]
        
        if reshape_boundry:
            name_boundry = lines[-5:]
        name_boundry = [x.strip() for x in name_boundry]
        return name_boundry
    
    def by_spacy(self, name_boundry):
        """
        Extract names using spacy NER model trained on Spanish Text. Load the
        pretrained model from spacy and used to identify Person names in the 
        text
        Params:
            - name_boundry->list:  List containing sentence identified to be
            having person names
        returns: A list of names if detected on None values.
        """
        sent_ = self.spacy_model(' '.join(name_boundry).lower())
        names = [ee.text for ee in sent_.ents if ee.label_=="PER"]
        if names:
            names_ = []
            for name in names:
                try:
                    name = [x for x in name_boundry if re.sub(self.pattern2,'', name).strip() in x.lower()]
                    name = name[0]
                    name = re.sub(self.pattern2.upper()+"|:", '', name.upper())
                    if 1<len(name.split(' '))<7:
                        names_.append(name)
                    else:
                        continue
                except IndexError:
                    continue
            if names_:
                names_ = names_
            else:
                names_=None
        else:
            sent_ = self.spacy_model(' '.join(name_boundry).lower())
            names = [ee.text for ee in sent_.ents if ee.label_=="PER"]
            if names:
                names_ = []
                for name in names:
                    try:
                        name = [x for x in name_boundry if re.sub(self.pattern2, '', name.lower()).strip() in x.lower()]
                        name = name[0]
                        name = re.sub(self.pattern2.upper()+"|:", '', name.upper())
                        if 1<len(name.split(' '))<7:
                            names_.append(name)
                        else:
                            continue
                    except IndexError:
                        continue
                if names_:
                    pass
                else:
                    names_=None
            else:
                names_ = None
        return names_
    
    def by_logic(self, name_boundry):
        """
        Extract names from text using logical approach. Usually the names occurs
        above, infront of or below lines which contains the name matching patterns
        i.e "magistrado ponente" or other relevent words
        params:
            nameboundry->List: A list of lines containing the pattern for names
            or names itslef
        returns:
            - Name if matched
            - None if not matched
            
        """
        if len(name_boundry)==5:
            new_boundry = name_boundry[1:-1]
        else:
            new_boundry = name_boundry
            
        if len(new_boundry)==3:
            mid_index = 1
            mid_elem = new_boundry[mid_index]
            mid_elem = re.sub(self.pattern1a, 'magistrado', mid_elem.lower())
            mid_elem = re.sub(self.pattern1b, 'ponente', mid_elem.lower())
            mid_elem = mid_elem.replace(':', '')
            name = re.findall(r"(?<=ponente).*", mid_elem.strip())
            if name:
                name = re.sub(self.pattern2.upper()+"|:", '', name[0].upper())
                if 1<len(name.split(' '))<7:
                    name = [name.upper()]
                else:
                    name=None
            else:
                exp_name = {x:y for x,y in enumerate(new_boundry) if bool(re.search(r'\d', y))==False}
                if 2 in exp_name.keys():
                    name = re.sub(self.pattern2.upper()+"|:", '', exp_name[2].upper())
                    if 1<len(name.split(' '))<7:
                        name = [name]
                    else:
                        name = None
                elif 0 in exp_name.keys():
                    name = re.sub(self.pattern2.upper()+"|:", '', exp_name[0].upper())
                    if 1<len(name.split(' '))<7:
                        name = [name]
                    else:
                        name = None
                else:
                    name = None
        else:
            name = None
        return name
    
    def extract(self, text):
        """
        Compile the above functions to extract names
        params:
            text->str
        returns:
            names->list
        """
        nb = self.name_boundry(text)
        names = self.by_spacy(nb)
        if names==None:
            names = self.by_logic(nb)
            if names:
                names =  names
            else:
                nb = self.name_boundry(text, reshape_boundry=True)
                names = self.by_spacy(nb)
                if names:
                    names = names
                else:
                    names = ['NA']
        else:
            names = names
        return list(set(names))
