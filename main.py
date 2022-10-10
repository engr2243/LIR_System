# -*- coding: utf-8 -*- 

#Libraries/packages
import sys
import os
import nltk
nltk.download('stopwords')

WORKDIR = os.getcwd()
sys.path.append(WORKDIR+'/scripts')

import spacy
from tqdm import tqdm
import glob
import json

from text_extractor import Extract
from judge_name import get_name
from sentence_identifier import sentenceID
from filing_identifier import filingID
from date_identifier import date
from room_identifier import room
from section_identifier import section

nlp = spacy.load("es_core_news_lg")

def main():
    """
    Main function:
        To load all files from the input directory
        Process each file and write the results to the
        same direcotry containing the files.
        
    """
    dir_ = input('Path to files:')
    files = glob.glob(dir_+ "\*.*")
    for file in tqdm(files):
        file_name, ext = os.path.splitext(file)
        if ext in ['.docx', '.doc', '.pdf']:
            with open(file_name+'.json', 'w', newline='') as f:
                text = Extract().get(file)
                names = get_name(spacy_model=nlp).extract(text)
                sentID = sentenceID().get(text)
                filling_id = filingID().get(text)
                eff_date = date().get(text)
                rooms = room(spacy_model=nlp).get(text)
                room_section = section().get(text)
                out = {'ponentes': names, 'identificador': sentID,
                                  'radicado': filling_id, 'fechaVigencia': eff_date,
                                  'salas':rooms, 'secciones': room_section}
                json.dump(out, f, indent=1)
                f.close()
        else:
            continue
    return

if __name__ == "__main__":
    print('start extraction')
    main()