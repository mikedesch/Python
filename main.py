import time
import pandas as pd
import numpy as np
import csv
import vcfpy
import os
import tracemalloc

## os.remove("./parsedGT.txt")

def parseVCF():

    # Open file, this will read in the header
    reader = vcfpy.Reader.from_path('variants.vcf')

    file1 = open("parsedGT.txt","a+")

    # Build and print header
    # header = reader.header.samples.names
    # print('\t'.join(header))
    for record in reader:
        if not record.is_snv():
            continue
        line = [call.data.get('GT') or './.' for call in record.calls]
 
        file1.write('\t'.join(map(str, line)) + "\n")


## parseVCF()











## File Description:
##
##	creating a 2-D array out of the parsed output from (vcfpy) readVCF.py
##
##

## tokenizing each row on "\t" character
def extractGT(text):
    row = []
    z = text.find("\t")
    if z == 0:  row.append('')
    else:   row.append(text[:z])
    for x in range(len(text)):
        if text[x] != '\t':  pass
        else:
            if x == (len(text)-1):  row.append('')
            else:
                if '\t' in text[(x+1):]:
                    y = text.find('\t', (x+1))
                    c = text[(x+1):y]
                else:   c = text[(x+1):]
                row.append(c)
    return row

## using the above tokenizing function to iterate on all rows from the input file
## -> this appends the individual tokenized elements to a 2-D array
def createArray(rawData):
    f1 = open(rawData, "r")
    arr = []
    while 1:
        text = f1.readline()
        if text == "":  break
        else:   pass
        if text[-1] == '\n':
            text = text[:-1]
        else:   pass
        row = extractGT(text)
        arr.append(row)
    return arr




## zygosityMatrix = createArray("./parsedGT.txt")


def zygosityCountsPerSample(GTMatrix):

    dim = np.shape(GTMatrix)
    GTResultsMatrixPerSample = np.empty([100,4])

    # writing #rows to var
    rows = dim[0]

    # writing #cols to var
    cols = dim[1]

    for c in range (0, cols):

        numberGTNotAvailable = 0
        numberGTHomozygousRef = 0
        numberGTHomozygousAlt = 0
        numberGTHeterozygous = 0
    
        for r in range (0, rows):
            if GTMatrix[r][c] == "./.":
                numberGTNotAvailable += 1
            if GTMatrix[r][c] == "0/0":
                numberGTHomozygousRef += 1
            if GTMatrix[r][c] == "1/1":
                numberGTHomozygousAlt += 1
            if GTMatrix[r][c] == "0/1":
                numberGTHeterozygous += 1

        GTResultsMatrixPerSample[c,0] = numberGTNotAvailable
        GTResultsMatrixPerSample[c,1] = numberGTHomozygousRef
        GTResultsMatrixPerSample[c,2] = numberGTHomozygousAlt
        GTResultsMatrixPerSample[c,3] = numberGTHeterozygous

    with open("GTResultsMatrixPerSample_PYTHON.csv","w+") as my_csv:
        newarray = csv.writer(my_csv,delimiter=',')
        newarray.writerows(GTResultsMatrixPerSample)


## zygosityCountsPerSample(zygosityMatrix)


def getRunTimePerformance(number):

    RunTimePerformanceResultsMatrix = np.empty([number,1])

    for i in range(0,number):

        if os.path.isfile('./parsedGT.txt'):
            os.remove("./parsedGT.txt")

        startTime = time.time()

        parseVCF()
        zygosityMatrix = createArray("./parsedGT.txt")
        zygosityCountsPerSample(zygosityMatrix)

        runTime = (time.time() - startTime)
        RunTimePerformanceResultsMatrix[i,0] = runTime
    
    with open("RunTimePerformanceResultsMatrix_PYTHON.csv","w+") as my_csv:
        newarray = csv.writer(my_csv,delimiter=',')
        newarray.writerows(RunTimePerformanceResultsMatrix)


getRunTimePerformance(10)

         
def getMemoryPerformance(number):

    MemoryPerformanceResultsMatrix = np.empty([number,2])

    for i in range(0,number):

        if os.path.isfile('./parsedGT.txt'):
            os.remove("./parsedGT.txt")

        tracemalloc.start()

        parseVCF()
        zygosityMatrix = createArray("./parsedGT.txt")
        zygosityCountsPerSample(zygosityMatrix)

        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        MemoryPerformanceResultsMatrix[i,0] = current / 1000
        MemoryPerformanceResultsMatrix[i,1] = peak / 1000
    
    with open("MemoryPerformanceResultsMatrix_PYTHON.csv","w+") as my_csv:
        newarray = csv.writer(my_csv,delimiter=',')
        newarray.writerows(MemoryPerformanceResultsMatrix)


getMemoryPerformance(10)
