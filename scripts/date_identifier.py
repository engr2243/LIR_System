# -*- coding: utf-8 -*-
from text_to_num import text2num
from datetime import date as dt
import re
import nltk

stopword_es = nltk.corpus.stopwords.words('spanish')

class date:
    """
    Class to identify and parse lines containing dates and extract and convert
    dates into presentable format
    """
    def __init__(self):
        self.terms = ['bogotá','d.t.','d . c .', 'd.c.', 'd.c .', 'd .c.' ,
                      'd .c .', 'd. c.', 'd. c .', 'santafé de bogotá']
        self.months_dic =  {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5,
               'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9,
               'octubre': 10, 'noviembre': 11, 'diciembre': 12, 'embre':12}
        self.year = dt.today().year

        
    def text2numbers(self, str_):
        """
        convert text to numbers
        params:
            str_-> str: String containing numbers written in words
        retruns-> int:
            converted word numbers to numerical format
        """
        try:
            num = text2num(str_, "es")
        except ValueError:
            num=None
        return num

    def text2date_format(self, eff_dates):
        """
        Function to take effective date(raw sentence format), process and convert
        into a proper datetime format(YYYY-MM-DD)
        params:
            eff_dates-> str:
                Raw format of effective date written in the form of words+numbers
        return:
            date_out-> str: Returns date in a refined format (YYYY-MM-DD)
        """
        months_dic = self.months_dic
        try:
            if eff_dates:
                num = eff_dates[0]
                month_str = re.findall(pattern = "|".join(months_dic.keys()), string=num)[0]
                month_num = months_dic[month_str]
                date_yr = re.findall(r"(?<!\d)(\d{1,2}|\d{4})(?!\d)", num)
                date_yr = [x for x in date_yr if x.isnumeric()]
                if len(date_yr)>=2:
                    day = date_yr[0]
                    year_ = date_yr[1]
                    if  len(year_)==2  and int(year_)>int(str(year)[-2:]):
                        year_ = '19' + year_
                    elif len(year_)==2  and int(year_)<=int(str(year)[-2:]):
                        year_ = '20' + year_
                    elif len(year_)==4:
                        year_ = year_
                    else:
                        year_ =''
                    date_out = '{yyyy}-{mm}-{dd}'.format(yyyy = year_, mm=month_num, dd=day)
                elif len(date_yr)==1:
                    day = date_yr[0]
                    str_ = num.split(month_str)[-1].strip()
                    str_ = re.sub(r'[^\w\s]', '', str_)
                    str_ = ' '.join([x for x in str_.split() if x not in stopword_es])
                    str_ = unidecode.unidecode(str_)
                    year_ = self.text2numbers(str_)
                    if year_==None:
                        str_ = ' '.join(list(dict.fromkeys(str_.split())))
                        year_ = self.text2numbers(str_)
                        if year_==None:
                            str_ = str_.split(day)[1]
                            str_ = ' '.join(list(dict.fromkeys(str_.split())))
                            year_ = self.text2numbers(str_)
                        else:
                            year_ = ''
                    else:
                        year_ = year_
                    date_out = '{yyyy}-{mm}-{dd}'.format(yyyy = year_, mm=month_num, dd=day)
                else:
                    date_out = ''
                
            else:
                date_out = ''
        except (NameError, IndexError):
            date_out = ''
        return date_out
        
    def get(self, text):
        """
        Function to identify the sentence for effective dates, use the above functions
        to process and convert it into proper formats
        params:
            text-> str: input text
        returns:
            date_out-> Output date
        """
        terms = self.terms
        text = text.lower().split('\n')[0:20]
        eff_dates = []
        for line in text:
            line = line
            cond = any(line.strip().startswith(x) or x in line.strip() for x in terms)
            if cond:
                index = text.index(line)
                target_text = text[index].strip()
                eff_dates.append(target_text) 
                break
            else:
                continue
        date_out = self.text2date_format(eff_dates)
        if len(date_out.split('-'))==3:
            pass
        else:
            date_out = ''
        return date_out


