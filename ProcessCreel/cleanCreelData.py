
import os
import fileinput
from datetime import date

DATA_DIR = r"C:\Dev\Data\CreelData\temp"




def readDict(mapFile):
    try:

        map = dict()
        with open(mapFile,'r') as myFile:
            for line in myFile:
                parts = line.split(',')
                map[parts[0]] = str(parts[2])[:-1]
        return map

    except IOError:
        print("Error: File does not exist")


def updateFile(infile, outfile,map):
    out = open(outfile,'w')
    with open(infile,'r') as myFile:
        for line in myFile:
            parts = line.split(',')
            if (map.has_key(parts[1])):
                parts[1] = map[parts[1]]
            s = str()
            for part in parts:
                s = s + part +','
            s = s[:-1]
            out.write(s)

    out.close()

infile = os.path.join(DATA_DIR, "CreelData05-12.csv")
mapfile = os.path.join(DATA_DIR, "map.csv")
outfile = os.path.join(DATA_DIR, "CreelData05-12-clean.csv")
map = readDict(mapfile)
updateFile(infile,outfile,map)

