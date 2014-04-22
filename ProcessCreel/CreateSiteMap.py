
import os
import fileinput
from datetime import date

DATA_DIR = r"C:\Dev\Data\CreelData\temp"




def getSiteDict(inFile):
    try:

        map = dict()
        with open(inFile,'r') as myFile:
            for line in myFile:
                parts = line.split(',')
                siteName = parts[1]
                if (map.has_key(siteName)):
                    map[siteName] = map[siteName] +1
                else:
                    map[siteName] = 1
        return map

    except IOError:
        print("Error: File does not exist")
    return





infile = os.path.join(DATA_DIR, "CreelData05-12.csv")
outfile = os.path.join(DATA_DIR, "map.csv")
out = open(outfile,'w')
dict = getSiteDict(infile)
out.write('name,count\n')
for k,v in dict.items():
    out .write(k + ',' + str(v) + '\n')



