import random
import string
import sys
import os
import requests
import re
import fnv
import hashlib
from pprint import pprint
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from bs4.element import Comment
from pprint import pprint


# This function checks for the required tags in the html string
# def req_tags(element):
#     if element.parent.name in ['query']:
#         return True
#     if isinstance(element, Comment):
#         return False
#     return False
#
# # This function uses the previous function to extract only the required text from the html string
# def my_html_parser(html_string):
#     new_soup = BeautifulSoup(html_string, 'html.parser')
#     texts = new_soup.findAll("query")
#     for x in texts:
#
#     return u"".join(texts)


required_punc = string.punctuation + "—\""
required_punc = required_punc.replace('\'', '')
sl_file = 'C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\stoplist.txt'
term_index = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\term_index.txt", "r", errors='ignore')
term_id_file = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\TERMID.txt", "r", errors='ignore')
query_file = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 2\\topics.xml")
term_content = term_id_file.readlines()
term_content1 = {}
for x in term_content:
    a = x.split()
    if len(a) == 2:
        term_content1.update({a[1]: a[0]})
print(term_content1)

stoplist = open(sl_file).read()
stoplist = stoplist.splitlines()

new_soup = BeautifulSoup(query_file, 'html.parser')
queries = [x.get_text() for x in new_soup.find_all('query')]
print(queries)
queries = [x for x in queries if x not in stoplist]
queries = [x.translate(str.maketrans('','',required_punc)) for x in queries]
ps = PorterStemmer()
print(queries)
queries = [x.lower().split() for x in queries]
print(queries)
for i in range(len(queries)):
    for j in range(len(queries[i])):
        queries[i][j] = ps.stem(queries[i][j])
print(queries)