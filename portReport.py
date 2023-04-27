import argparse
import csv
import os
import sys
from collections import defaultdict

# csv failu skaitymo metodas

def readCsv(dir):
    with open (dir, 'r') as csvFile:
        delimiter = str(csv.Sniffer().sniff(csvFile.readline(),delimiters=[',','|']).delimiter)
        # tikrinam koks yra csv failo stulpeliu skirtukas
    portdict = defaultdict(list)
    with open(dir, 'r') as csv_file:
        if delimiter == ',': # kablelis reiskia paduodama nessus ataskaita
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0: # Praleidziam pirma eilute
                    line_count += 1
                elif (row[6] != '0'):
                    portdict[row[4]].append(row[5] + '/' + row[6])
        elif delimiter == '|': # vertikalus bruksnys reiskia senos portu ataskaitos faila
            csv_reader = csv.reader(csv_file, delimiter='|')
            line_count = 0
            for row in csv_reader:
                if line_count == 0: # Praleidziam pirma eilute
                    line_count += 1
                else: 
                    portdict[row[0]] = row[1].split(',') # filtravimas nereikalingas
        else:
            print('Netinkamas csv failo stulpeliu skirtukas!')
            exit(1)

    return (portdict) # Grazina atrusiuotus pagal id ip adresus ir ju portus

# Port pasikeitimu lyginimas

def comparePorts():
    changedPorts = defaultdict(list)
    if not compare: # Tikrinam ar yra lyginamas failas
        for key, value in portDict.items(): # Jei lyginamas failas nenurodytas, tiesiog agreguojam .csv faila
            ports = set(list(value))
            for item in ports:
                changedPorts[key].append(item)
    else:

        for key, value in portDict.items(): # Jei lyginamas failas nurodytas, lyginam ip adresu portus.
            for keyOld, valueOld in portDictOld.items():
                if key == keyOld: # ieskom vienodu ip adresu
                    portList = list(set(value)) # Prafiltruojami pasikartojantys port
                    portListOld = list(set(valueOld))
                    diff = [item for item in portList if item not in portListOld] # Tikrinami port sarasu skirtumai
                    for item in diff:
                        changedPorts[key].append(item) # sudedam naujai atsiradusius portus
            if key not in portDictOld.keys(): # Tikrinam ar ip adresas pries tai isvis egzistavo
                portList = list(set(value))
                for item in portList:
                    changedPorts[key].append(item) # Jei neegzistavo, reiskia atsidare nauji portai ant to ip
              
    return changedPorts # Grazina pasikeitusiu portu sarasa

print('\nNessus ataskaitos apdorojimo programa\n')

parser = argparse.ArgumentParser() # Argumentu is cmd nuskaitymas

parser.add_argument('-i', '--input', help = 'Csv failo lokacija, nurodoma tiksli .csv failo direktorija')
parser.add_argument('-c', '--compare', help = 'Lyginamo failo lokacija, nurodoma tiksli lyginamo .csv failo direktorija')
parser.add_argument('-o', '--output', help = 'Ataskaitos failo lokacija, nurodomas tiksli .csv failo lokacija. Nenurodzius lokacijos rezultatai spausdinami i stdout')
parser.add_argument('-s', '--sort', help = "Nurodoma, jei norima rikiuoti kazkuriuo budu. ip-desc ip-asc = rikiavimas pagal ip, port-desc port-asc = rikiavimas pagal port")

args = parser.parse_args() # Tikrinam, ar ivestas palyginimamas .csv failas
if args.input:
    csvDir = args.input
    if not os.path.exists(csvDir):
        print('csv failas neegzistuoja')
        exit(1)
    if not str(csvDir).endswith('.csv'):
        print('Reikia nurodyti csv faila')
        exit(1)
else:
    print('Nenurodytas csv failas')
    exit(1)
output = True
if args.output: # Tikrinama, ar nurodyta .csv pasikeitimu ataskaitos direktorija
    csvOutDir = args.output
    if not str(csvOutDir).endswith('.csv'):
        print('Nenurodytas .csv formato failas')
        exit(1)
else:
    output = False # Spausdinsim i stdout
compare = True
if args.compare: # Tikrinama, ar duodamas .csv failas su kuriuo lyginti ataskaita
    csvDirOld = args.compare
    if not os.path.exists(csvDirOld):
        print('lyginamas csv failas neegzistuoja')
        exit(1)
    if not str(csvDirOld).endswith('.csv'):
        print('Reikia nurodyti csv faila')
        exit(1)
else:
    compare = False

portDict = readCsv(csvDir) # .csv failu nuskaitymas
if compare:
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
if len(changedPorts):
    if not output: # Jei nenurodyta output direktorija rasom tiesiai i stdout
        stdoutWritter = csv.writer(sys.stdout, delimiter='|')
        stdoutWritter.writerow(['Ip address', 'port'])
        for key,value in changedPorts.items():
            stdoutWritter.writerow([key, ','.join(value)])
    else: # Jei nurodyta rasom i nurodyta faila
        with open(csvOutDir, 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter='|')
            writer.writerow(['Ip address', 'port'])
            for key, value in changedPorts.items():
                writer.writerow([key, ','.join(value)])
else:
    print('Nebuvo rasta pasikeitusiu portu')
    exit(0)

# Ataskaitos failo nuskaitymas ir rezultatu atvaizda svimas

if output: 
    with open(csvOutDir) as csv_file: 
        csv_reader = csv.reader(csv_file, delimiter='|')
        line_count = 0
        port_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                print('{:20}{}'.format(row[0], row[1]))
                print('----------------------------------')
            else:
                print('{:20}{}'.format(row[0], row[1]))
                line_count += 1
                port_count += len(str(row[1]).split(sep=','))
        if compare:
            print('\nRasta {} pasikeitusiu portu.'.format(port_count))
        else:
            print('\nRasta {} atidarytu portu.'.format(port_count))

