import os
import fileinput
from datetime import date

DATA_DIR = r"C:\Dev\Data\CreelData"




def CreateTideFile(inFile):
    try:
        with open(inFile,'r') as myFile:

            line = myFile.readline()
            parts = line.split(',')
            col0 = parts[0]
            col1 = parts[1]
            print(col0 +" " + col1)
            #fileName = siteName +".csv"
            # outFile = os.path.join(DATA_DIR, fileName)
            # out = open(outFile,'w')
            # out.write(header)
            for line in myFile:
                parts = line.split(',')
                dt_parts = parts[0].split(" ")
                date = dt_parts[0]
                hr = dt_parts[1]
                wl = parts[1]
                print(date +" " +hr + " " + wl)


    except IOError:
        print("Error: File does not exist")
    return



inFile = os.path.join(DATA_DIR, "CO-OPS__9444090__hr.csv")
CreateTideFile(inFile)