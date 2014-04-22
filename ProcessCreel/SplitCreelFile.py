import os
import fileinput
from datetime import date

DATA_DIR = r"C:\Dev\Data\CreelData"




def CreateFiles(inFile):
    try:
        with open(inFile,'r') as myFile:
            line = myFile.readline()
            parts = line.split(',')
            t = ''.join(parts[i]+',' for i in range(2,len(parts)))
            header =  parts[0]+',' + t.rstrip(',');


            line = myFile.readline()
            parts = line.split(',')
            siteName = parts[1].rstrip()
            fileName = siteName +".csv"
            outFile = os.path.join(DATA_DIR, fileName)
            out = open(outFile,'w')
            out.write(header)
            for line in myFile:
                parts = line.split(',')
                if  (parts[1].rstrip() != siteName):
                    out.close();
                    siteName = parts[1]
                    fileName = siteName +".csv"
                    fileName = fileName.replace('/',' ')
                    fileName = fileName.replace('\"','')

                    outFile = os.path.join(DATA_DIR, fileName)
                    out = open(outFile,'w')
                    out.write(header)
                t = ''.join(parts[i]+',' for i in range(2,len(parts)))

                nLine = parts[0]+',' + t.rstrip(',');
                out.write(nLine)
        out.close()
    except IOError:
        print("Error: File does not exist")
    return



inFile = os.path.join(DATA_DIR, "CreelData05-12-clean.csv")
CreateFiles(inFile)