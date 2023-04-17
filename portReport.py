import argparse
import csv
import os

# csv failu skaitymo metodas

def readCsv(dir):
    with open (dir, 'r') as csvFile:
        delimiter = str(csv.Sniffer().sniff(csvFile.readline(),delimiters=[',','|']).delimiter)
        # tikrinam koks yra csv failo stulpeliu skirtukas
    portList = {}
    with open(dir) as csv_file:
        if delimiter == ',': # kablelis reiskia paduodama nessus ataskaita
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0: # Praleidziam pirma eilute
                    line_count += 1
                elif (row[0] == '11219' or row[0] == '166602'): # tikrinam, ar atitinka ID
                    portList[row[4]]= row[5] + '/' + row[6] # jei tinka, pasiimam ip adresa ir port
        elif delimiter == '|': # vertikalus bruksnys reiskia senos portu ataskaitos faila
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                if line_count == 0: # Praleidziam pirma eilute
                    line_count += 1
                else: 
                    portList[row[0]]= row[1] # filtravimas nereikalingas
        else:
            print('Netinkamas csv failo stulpeliu skirtukas!')
            exit(1)


    return (portList) # Grazina atrusiuotus pagal id ip adresus ir ju portus

# Port pasikeitimu lyginimas

def comparePorts():
    changedPorts = {}
    for key, value in portDict.items():
        for keyOld, valueOld in portDictOld.items():
            if key == keyOld: # ieskom vienodu ip adresu
                if not str(value).split(',')[0] == str(valueOld).split(',')[0]: # tikrinam, ar pasikeite portas ar ne
                    changedPorts[key] = str(valueOld).split(',')[0] + ',' + str(value).split(',')[0]


    return changedPorts # Grazina pasikeitusiu portu sarasa

print('\nNessus ataskaitos apdorojimo programa\n')

parser = argparse.ArgumentParser() # Argumentu is cmd nuskaitymas

parser.add_argument('-i', '--input', help = 'csv failo lokacija')
parser.add_argument('-c', '--compare', help = 'lyginamo failo lokacija')
parser.add_argument('-o', '--output', help = 'ataskaitos failo lokacija')
parser.add_argument('-s', '--sort', help = "Nurodoma, jei norima sortint kazkuriuo")

args = parser.parse_args() # Tikrinam, ar ivestas palyginimamas .csv failas
if args.input:
    csvDir = args.input
    if not os.path.exists(csvDir):
        print('csv failas neegzistuoja')
        exit(1)
else:
    print('Nenurodytas csv failas')
    exit(1)
if args.output: # Tikrinama, ar nurodyta .csv pasikeitimu ataskaitos direktorija
    csvOutDir = args.output
    if not os.path.exists(csvOutDir):
        print('Raporto failo saugojimo direktorija neegzistuoja')
        exit(1)
else:
    csvOutDir = './nessusAtaskaita.csv' # Default direktorija
if args.compare: # Tikrinama, ar duodamas .csv failas su kuriuo lyginti ataskaita
    csvDirOld = args.compare
    if not os.path.exists(csvDirOld):
        print('lyginamas csv failas neegzistuoja')
        exit(1)
else:
    csvDirOld = './nessusAtaskaita.csv' # Jei neduota, lygina su pries tai atlikta palyginimo ataskaita\
    if not os.path.exists(csvDirOld):
        print('nessus ataskaita nebuvo rasta programos direktorijoje, butina nurodyti atliktos ataskaitos faila')
        exit(1)


portDict = readCsv(csvDir) # .csv failu nuskaitymas
portDictOld = readCsv(csvDirOld)
changedPorts = comparePorts() # Nuskaitytu ip adresu port pasikeitimu lyginimas

if args.sort: # Rikiavimo pasirinkimai, pagal ip, port, zemejancia aukstejancia tvarka
    if args.sort == 'ip-desc':
        changedPorts = dict(sorted(changedPorts.items(), key = lambda x:x[0], reverse=True))
    elif args.sort == 'ip-asc':
        changedPorts = dict(sorted(changedPorts.items(), key = lambda x:x[0]))
    elif args.sort == 'port-desc':
        changedPorts = dict(sorted(changedPorts.items(), key = lambda x:x[1], reverse=True))
    elif args.sort == 'port-asc':
        changedPorts = dict(sorted(changedPorts.items(), key = lambda x:x[1]))

csv_columns = ['IP address', 'port']

# Ataskaitos failo sukurimas

with open(csvOutDir, 'w') as csvFile:
    writer = csv.writer(csvFile, delimiter='|')
    writer.writerow(['Ip address', 'port'])
    for key, value in changedPorts.items():
        writer.writerow([key, value])

# Ataskaitos failo nuskaitymas ir rezultatu atvaizda svimas

if len(changedPorts): # Tikrinam, ar isvis yra pakeistu portu
    with open(csvOutDir) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter='|')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                print('{:20}{},buves port'.format(row[0], row[1]))
                print('----------------------------------')
            else:
                print('{:20}{}'.format(row[0], row[1]))
                line_count += 1
        print('\nRasta {} pasikeitusiu portu.'.format(line_count))
else:
    print("Nebuvo rasta pasikeitusiu portu")

