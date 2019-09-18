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

print(sys.argv[1])
print(sys.argv[2])

required_punc = string.punctuation + "—\""
required_punc = required_punc.replace('\'', '')

if sys.argv[1] == "--term":
    flag = 1
else:
    print("Are you sure you don't want to tokenize the data? Type Y for yes, N for No")
    txt_ent = input()
    if txt_ent.lower() == "y":
        flag = 2
    else:
        flag = 1
txt = sys.argv[2]
txt = txt.lower()
if flag == 1:
    ps = PorterStemmer()
    txt = ps.stem(txt)
print(txt)
term_index = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\term_index.txt", "r", errors='ignore')
term_id_file = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\TERMID.txt", "r", errors='ignore')
term_content = term_id_file.readlines()
term_content1 = {}
for x in term_content:
    a = x.split()
    if len(a) == 2:
        term_content1.update({a[1]: a[0]})
print(term_content1)

if txt in term_content1:
    term_id = term_content1[txt]
    file_content = term_index.readlines()
    file_content = [x.strip().split()[0:3] for x in file_content]
    foundflag = 0
    for x in file_content:
        if x[0] == term_id:
            print("Listing for Term: " + sys.argv[2])
            print("TERMID: " + str(term_id))
            print("Number of documents containing term: " + str(x[2]))
            print("Term frequency in corpus: " + str(x[1]))
            foundflag = 1
            break
    if foundflag == 0:
        print("Term not found")
else:
    print("Term not found")
