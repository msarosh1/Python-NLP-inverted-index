import random
import string
import sys
import math
import os
import requests
import re
import fnv
import hashlib
from pprint import pprint
from collections import Counter
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from bs4.element import Comment
from pprint import pprint

def mybm25func(D, tfd, tfq, df, lend, avglend):
    k1 = 1.2
    k2 = 500
    b = 0.75
    K = k1 * ((1-b) + (b*(lend/avglend)))
    temp = ((D + 0.5)/(df+0.5)) * (((1+k1)*tfd)/(K+tfd)) * (((1+k2)*tfq)/(k2 + tfq))
    answer = math.log(temp, 10)
    return answer




required_punc = string.punctuation + "—\""
required_punc = required_punc.replace('\'', '')
sl_file = 'C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\stoplist.txt'
term_index_file = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\term_index.txt", "r", errors='ignore')
term_id_file = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\TERMID.txt", "r", errors='ignore')
query_file = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 2\\topics.xml")
docid = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\DOCID.txt", "r", errors='ignore')
BM25ranking = open("C:\\Users\\Muham\\Desktop\\Semester 5\\Info Ret\\Assignment 1\\BM25.txt", "a", errors='ignore')

doc_ids = {}
temp = []
doc_id_raw = docid.readlines()
for x in doc_id_raw:
    temp = x.split("\t")
    doc_ids.update({temp[0]: temp[1]})

term_content = term_id_file.readlines()
term_content1 = {}
for x in term_content:
    a = x.split()
    if len(a) == 2:
        term_content1.update({a[1]: a[0]})
templist = ()
td_pairs = {}
tempdocid = 1
tif_dat = [x.split() for x in term_index_file.readlines()]
doc_freqs = {}
for i in range(len(tif_dat)):
    doc_freqs.update({tif_dat[i][0]: tif_dat[i][2]})

currtermid = 1
for i in range(len(tif_dat)):
    del(tif_dat[i][1:3])
    td_pairs.update({int(tif_dat[i][0]): {}})
    for j in range(len(tif_dat[i])):
        tif_dat[i][j] = tif_dat[i][j].split(',')
        if j == 0:
            currtermid = int(tif_dat[i][j][0])
        elif j == 1:
            tempdocid = int(tif_dat[i][j][0])
            td_pairs[currtermid].setdefault(int(tempdocid), []).append(int(tif_dat[i][j][1]))
        else:
            td_pairs[currtermid].setdefault(int(tif_dat[i][j][0]) + int(tempdocid), []).append(int(tif_dat[i][j][1]))


stoplist = open(sl_file).read()
stoplist = stoplist.splitlines()
qids = []
new_soup = BeautifulSoup(query_file, 'html.parser')
for element in new_soup.find_all("topic"):
    qids.append(element['number'])
queries = [x.get_text() for x in new_soup.find_all('query')]
queries = [x for x in queries if x not in stoplist]
queries = [x.translate(str.maketrans('','',required_punc)) for x in queries]
ps = PorterStemmer()
queries = [x.lower().split() for x in queries]

for i in range(len(queries)):
    for j in range(len(queries[i])):
        queries[i][j] = ps.stem(queries[i][j])
print(queries)

file_content = term_index_file.readlines()
file_content = [x.strip().split()[0:3] for x in file_content]

tot_words = 0
for i in td_pairs.keys():
    for j in td_pairs[i].keys():
        tot_words += len(td_pairs[i][j])

D = len(doc_ids)
avg_dlen = tot_words/D
term_freq = 0
doc_freq = 0
lend = 0
tfq = 0
avglend = 0
currtermid = 0
bm25sum = 0
doc_length = 0
currbm25score = 0
osakafinal = {}

for i in range(len(queries)):
    doc_length = 0
    for k in doc_ids.keys():
        doc_length = 0
        currbm25score = 0
        for j in range(len(queries[i])):
            if queries[i][j] in term_content1:
                currtermid = int(term_content1[queries[i][j]])
                tfq = queries[i].count(queries[i][j])
                if currtermid in td_pairs:
                    if int(k) in td_pairs[currtermid]:
                        doc_freq = doc_freqs[k]
                        term_freq = len(td_pairs[currtermid][int(k)])
                        for l in td_pairs.keys():
                            if int(k) in td_pairs[int(l)]:
                                doc_length += len(td_pairs[int(l)][int(k)])
                        currbm25score += mybm25func(D, term_freq, tfq, int(doc_freq), doc_length, avg_dlen)
        osakafinal.update({qids[i]: [doc_ids[k], round(currbm25score, 3)]})

sorted(osakafinal.items(), key=lambda e: e[1][1])

for k, v in osakafinal.items():
    BM25ranking.write(str(k) + " " + str(v[0]) + " " + str(v[1]) + " run1\n")
print("it's done")