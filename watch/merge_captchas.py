fim = open('tgimages.csv')
fcap = open('captchas.csv')

fout = open('solved.csv', 'w')

caps = dict()

for line in fcap:
    fcs = line.strip().split(',')
    caps[fcs[0]] = fcs[1]

for line in fim:
    fms = line.strip().split(',')
    if fms[0] in caps:
        fout.write(line.strip()+','+caps[fms[0]]+"\n")

fout.close()
