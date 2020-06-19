from flask import Flask,render_template,redirect,url_for
from forms import CountryForm
import urllib
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import os


PEOPLE_FOLDER = os.path.join('static', 'country_graph')

app = Flask(__name__) #creating the Flask class object 

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
  
 
@app.route('/', methods=['GET', 'POST']) #decorator drfines the   
def home():  
    form = CountryForm()
    if form.validate_on_submit():
        file1 = open("myfile.txt","w") 
        file1.write(form.country.data)
        file1.close() 
        return redirect(url_for('country_details'))
    return render_template('home.html',title = ' Search for a country ',form = form)

@app.route('/country_details')
def country_details():
    
    
#idf
    indx = 0
    idf = []
    with open('idf.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if len(line) != 0 and indx != 0:
                idf.append(float(line[0]))
            indx = indx + 1

    indx = 0
    l8 = []
    with open('l8.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if len(line) != 0 and indx != 0:
                l8.append(line[0])
            indx = indx + 1

    links = []
    with open('links.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            k = (line[0]).split('\n')
            for i10 in k:
                links.append(i10)


    headlines = []
    with open('headline.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            k = (line[0]).split('\n')
            for i10 in k:
                headlines.append(i10)
            


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

    indx = 0
    lengths = []
    with open('lengths.csv','r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if len(line) != 0 and indx != 0:
                lengths.append(float(line[0]))
            indx = indx + 1

    f = open("myfile.txt", "r")
    q = f.read().lower()


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
    
    needed_links = []
    needed_headlines = []
    cnt = 0
    for i in cossim:
        if i == 0:
            cnt = cnt + 1
    cnt = 0
    for i in cossim:
        if i == 0:
            cnt = cnt + 1
    for i in range(len(links)-1,cnt-1,-1):
        needed_links.append(links[l[i]-1])    
        needed_headlines.append(headlines[l[i]-1])
    
    
    needed1 = []
    for i in needed_links:
        if len(needed1) == 0:
            needed1.append(i)
        else:
            if needed1[len(needed1)-1] != i:
                needed1.append(i)
    needed_links = needed1

    needed2 = []
    for i in needed_headlines:
        if len(needed2) == 0:
            needed2.append(i)
        else:
            if needed2[len(needed2)-1] != i:
                needed2.append(i)
    needed_headlines = needed2


    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], q+'.jpg')
    legend = os.path.join(app.config['UPLOAD_FOLDER'], 'Legend.jpg')
    return render_template('country_details.html',len = len(needed_links),links = needed_links,profilepic_filename  = full_filename,headlines = needed_headlines,legend =legend )


  
if __name__ =='__main__':  
    app.run(debug = True)  