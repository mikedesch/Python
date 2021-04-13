import timeit



def fixText(text):
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

def createTuple(oldFile):
    ## oldFile is filename (e.g. 'sheet.csv')
    f1 = open(oldFile, "r")
    tup = []
    while 1:
        text = f1.readline()
        if text == "":  break
        else:   pass
        if text[-1] == '\n':
            text = text[:-1]
        else:   pass
        row = fixText(text)
        tup.append(row)
    return tup




matrix = createTuple("./parsedGT_4.txt")

# print(matrix)

import numpy as np

dim = np.shape(matrix)

# writing #rows to var
rows = dim[0]

# writing #cols to var
cols = dim[1]

print(rows, cols)

GTResultsMatrixPerSample = np.empty([100,4])

print(" dim of GTResultsMatrixPerSample is ")
print(np.shape(GTResultsMatrixPerSample))

for c in range (0, cols):

    numberGTNotAvailable = 0
    numberGTHomozygousRef = 0
    numberGTHomozygousAlt = 0
    numberGTHeterozygous = 0
    
    for r in range (0, rows):
        if matrix[r][c] == "./.":
            numberGTNotAvailable += 1
        if matrix[r][c] == "0/0":
            numberGTHomozygousRef += 1
        if matrix[r][c] == "1/1":
            numberGTHomozygousAlt += 1
        if matrix[r][c] == "0/1":
            numberGTHeterozygous += 1

    GTResultsMatrixPerSample[c,0] = numberGTNotAvailable
    GTResultsMatrixPerSample[c,1] = numberGTHomozygousRef
    GTResultsMatrixPerSample[c,2] = numberGTHomozygousAlt
    GTResultsMatrixPerSample[c,3] = numberGTHeterozygous
    


for i in range(0,4):
    print(GTResultsMatrixPerSample[0,i])



