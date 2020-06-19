import pandas as pd
import csv
import re

df = pd.read_csv("idf.csv")
idf = df['IDF_Values']

l8 = []
with open('file.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        k = (line[0]).split('\n')
        for i10 in k:
            l8.append(i10)
l8 = l8[1:]

links = []
with open('links.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        k = (line[0]).split('\n')
        for i10 in k:
            links.append(i10)


terms = []
count = []
document = []

indx = 0 

with open('tcd1.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        if len(line) != 0 and indx != 0:
            terms.append(line[0])
            count.append(float(line[1]))
            document.append(int(line[2]))
        indx = indx + 1


k = 0
l = []
for k in range(len(terms)):
    dicti={}
    dicti['term'] = terms[k]
    dicti['count'] = count[k]
    dicti['Doc#'] = document[k]
    l.append(dicti.copy())

print(l)


df = pd.read_csv("lengths.csv")
lengths = df['Lengths']
print(lengths)



q = 'uk'
sub_q = re.split("[\s|,|.|!]",q) 
len_q = 0
qti =[]
for i in sub_q:
    cnt = 0
    for i1 in l8:
        if i==i1:
            len_q = len_q + (idf[cnt]*idf[cnt])
            qti.append(idf[cnt])
        cnt = cnt + 1  
cossim=[]
for i in range(1,len(links)+1):
    cos=0
    for i1 in l:
        if i1['Doc#'] == i:
            cnt = 0
            for i2 in sub_q:
                if i2 == i1['term']:
                    print(i1['term'])
                    cos = cos + i1['count'] * idf[cnt]
                cnt = cnt + 1
    cossim.append(cos)
for i in range(0,len(links)):
    if lengths[i] != 0:
        cossim[i] = cossim[i]/lengths[i]
    else:
        cossim[i] = 0
l = []
for i in range(1,len(links)+1):
    l.append(i)
for i in range(0,len(links)):
    for j in range(0,len(links)-i-1):
        if cossim[j] > cossim[j+1]:
            cossim[j],cossim[j+1] = cossim[j+1],cossim[j]
            l[j],l[j+1] = l[j+1],l[j]
cnt = 0
for i in cossim:
    if i == 0:
        cnt = cnt + 1
for i in range(0,len(links)-cnt):
    print(links[l[i]])

