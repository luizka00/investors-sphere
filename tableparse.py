# Library for opening url and creating 
# requests
import urllib.request
import pandas as pd
# pretty-print python data structures
from pprint import pprint
# for parsing all the tables present 
# on the website
from html_table_parser.parser import HTMLTableParser
import matplotlib.pyplot as plt

def get_content(url):

    #making request to the website
    request = urllib.request.Request(url=url)
    f = urllib.request.urlopen(request)

    #reading contents of the website
    return f.read()

si_content= get_content('https://strefainwestorow.pl/rekomendacje/lista-rekomendacji/wszystkie').decode('utf-8') #defining html content from this link

tabela = HTMLTableParser()

tabela.feed(si_content)

print("\n\nRekomendacje\n") 
print(pd.DataFrame(tabela.tables[0])) #converting table to dataframe 

rec= pd.DataFrame(tabela.tables[0])

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Prevent line breaks in columns

print(rec)