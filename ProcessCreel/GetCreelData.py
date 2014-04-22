import requests
import os
import re
import fileinput
from datetime import date

DATA_DIR = r"C:\Dev\Data\CreelData\temp"
BASE_URL = r"http://wdfw.wa.gov/fishing/creel/puget/"









def getUrls(baseUrl):

    urls = list()
    r = requests.get(baseURL)
    t= r.text
    t = t.encode("utf8")
    t = t.replace('\n','')
    regexTable = "\<table(.+?)\</table"
    tables = re.findall(regexTable,t)
    regexRows = "\<tr(.+?)\</tr"
    rows = re.findall(regexRows,tables[6])
    for i in range(1,len(rows)-1):
        regexCol = "\<td(.+?)\</td"
        cols = re.findall(regexCol,rows[i])
        for col in cols:
            regexAnchor = "\<a(.+?)\</a"
            anchors = re.findall(regexAnchor,col)
            for anchor in anchors:
                regexHREF = "href=\"(.+?)\""
                href = re.findall(regexHREF,anchor)
                if(len(href)>0):
                    urls.append(href[0])
    return urls

def parseOtherFish(data):
    parsedList = list()
    for i in range(0,10):
        parsedList.append(data[i])

    halibut = '0,'
    if ('halibut' in data[10].lower()):
        halibut = data[11]

    elif ('halibut' in data[12].lower()):
        halibut = data[13]
    halibut = halibut.replace(',', '')
    halibut = halibut.replace('  ', ' ')
    parsedList.append(halibut + ',')


    lingcod = '0,'
    if ('lingcod' in data[10].lower()):
        lingcod = data[11]
    elif ('lingcod' in data[12].lower()):
        lingcod = data[13]
    lingcod = lingcod.replace(',', '')
    lingcod = lingcod.replace('  ', ' ')
    parsedList.append(lingcod + ',')

    # if (data[10] != ''):
    #     fishType = str(data[10]).lower()
    #     if ('halibut' in fishType):
    #         parsedList.append(data[11] + ',')
    #     elif ('lingcod' in fishType):
    #         parsedList.append('0,')
    #         parsedList.append(data[11] + ',')
    #     else:
    #         parsedList.append('0,')
    #         parsedList.append('0,')
    #
    # if (data[12] != ''):
    #     fishType = str(data[12]).lower()
    #     if ('halibut' in fishType):
    #         parsedList.append(data[13] + ',')
    #     elif ('lingcod' in fishType):
    #         parsedList.append('0,')
    #         parsedList.append(data[13] + ',')
    #     else:
    #         parsedList.append('0,')
    #         parsedList.append('0,')

    return parsedList




def parseRow(row):

    regex = ur"'\>(.+?)\<"
    regexCol = "\<td(.+?)\</td"
    cols = re.findall(regexCol,row)
    output = list()
    for col in cols:
        col = col.encode("utf8")


        regexValue = "\>(.*)"
        vals= re.findall(regexValue,col)
        for val in vals:
            if ('&nbsp;' in val):
                val = ''
            val = val.replace(',', '')
            val = val.replace('  ', ' ')
        output.append(val + ',')
    p = parseOtherFish(output)
    s= ''
    if((len(output)>0) and (len(output[0])>1)):
        #s = ''.join(output)
        s = ''.join(p)
        s = s[:-1]
        s=s+'\n'
    return s



def getCreelData(url):
    r = requests.get(url)
    t= r.text
    t = t.replace('\n','')
    regexTable = "\<table(.+?)\</table"
    tables = re.findall(regexTable,t)
    regexRows = "\<tr(.+?)\</tr"
    rows = list()
    if(len(tables)>0):
        rows = re.findall(regexRows,tables[0])
    cvs = list()
    for i in range(6,len(rows)-1):
        r = parseRow(rows[i])
        if(len(r)>0):
            cvs.append(r)
    return cvs

baseURLS = list()
for i in range(2005,2013):
    baseURLS.append(BASE_URL + str(i) +'/')

outFile = os.path.join(DATA_DIR, "CreelData05-12.csv")
out = open(outFile,'w')
out.write('Date,Ramp,Boats,Anglers,Chinook,Coho,Chum,Pink,Sockeye,RockFish,Halibut,Lingcod\n')
for baseURL in baseURLS:
    urls = getUrls(baseURL)
    for url in urls:
        data =getCreelData(baseURL +url)
        for line in data:
            if(('no effor' not in str(line).lower())and (('date' not in str(line).lower()))):
                out.write(line)
        print("finished:"+ url)
out.close()