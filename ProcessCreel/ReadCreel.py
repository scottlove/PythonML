import os
import fileinput
from datetime import date

DATA_DIR = r"C:/temp"




def getMonth(m):
    return {
        'Dec':12,
        'Nov':11,
        'Oct':10,
        'Sep':9,
        'Aug':8,
        'Jul':7,
        'Jun':6,
        'May':5,
        'Apr':4,
        'Mar':3,
        'Feb':2,
        'Jan':1,
    }[m]






def readLineByLine(inFile,outFile):
    d = date.today()
    try:
        out = open(outFile,'w')
        out.write('Date,Ramp,Boats,Anglers,Chinook,Coho,Chum,Pink,Sockeye,Other Species,Comments\n')
        with open(inFile,'r') as myFile:
            for line in myFile:
                parts = line.split(',')

                if(parts[0].__contains__('-')):
                    dayParts = parts[0].split('-')
                    if(len(dayParts) == 3):
                        day= int(dayParts[0])
                        month = dayParts[1]
                        year = int("20" + dayParts[2])
                        d= date(year,getMonth(month),day)
                elif (('Chinook' not in parts[3]) & (parts[0] != '')):
                    if ('\"' in parts[0]):
                        temp = parts[0].replace('\"','')
                        temp1 = parts[1].replace('\"','')
                        parts[0] = temp + temp1
                        del parts[1]

                    t = ''.join(parts[i]+',' for i in range(8))
                    nLine = str(d)+',' + t[:-1]
                    print (nLine)

                    out.write(nLine)
        out.close()
    except IOError:
        print("Error: File does not exist")
    return


inFile = os.path.join(DATA_DIR, "Creel2013.csv")
outFile = os.path.join(DATA_DIR, "CreelData.csv")
os.remove(outFile)
readLineByLine(inFile,outFile)

