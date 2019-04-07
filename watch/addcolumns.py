#!/usr/bin/python3

import os

DMAXIND = 2
DMININD = 3
CLOSEIND = 4
MCAPIND = 6

DUMPIND = 7

for name in os.listdir("../data"):
    fin = open("../data/"+name)

    mat = [l.strip().split(',') + ["-", "-"] for l in fin.readlines()]

    passedrows = 1
    passedsome = 0

    

    for i, row in enumerate(mat):
        try:
            dumpvolume = (float(row[DMAXIND]) - float(row[DMININD])) / float(r[CLOSEIND]) * float(r[MCAPIND])
            mat[i][DUMPIND] = dumpvolume
            passedsome = 1
            # max


        except:
            #print("failed row")
            passedrows = 0
            # this currency does not have the data
            pass

    if passedsome:
        print("passed")
    foutname = "../data-more/more-"+name
    fout = open(foutname, 'w')
    print(foutname)
    for row in mat:
        fout.write(','.join(row)+'\n')
    fout.close()

    
        
    
