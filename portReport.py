import argparse
import csv

def readCsv(dir):
    portList = {}
    with open(dir) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif (row[0] == '11219' or row[0] == '166602'):
                print(f'\t Host: {row[4]} Protocol: {row[5]} Port: {row[6]}.')
                portList[row[4]]= row[5] + '/' + row[6]
                line_count += 1
        print(f'Rasta {line_count} portu.')

    return (portList)

def comparePorts():
    changedPorts = {}
    for key, value in portDict.items():
        for keyOld, valueOld in portDictOld.items():
            if key == keyOld:
                #print(value, valueOld)
                if not value == valueOld:
                    print('pasikeite portai!!!')
                    print('ip adresas: {}, buves portas: {}, dabartinis portas {}'.format(key, valueOld, value))
                    changedPorts[key] = valueOld + ',' + value

    return changedPorts

print('Port ataskaitos programa')
#sortedPortList = dict(sorted(portList.items(), key = lambda x:x[1]))
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help = 'csv failo lokacija')
parser.add_argument('-c', '--compare', help = 'lyginamo failo lokacija')
parser.add_argument('-o', '--output', help = 'ataskaitos failo lokacija')

args = parser.parse_args()

if args.input:
    csvDir = args.input
    csvOutDir = args.output
    csvDirOld = args.compare
    print ('csv failo lokacija: % s' % args.input)
    print ('ataskaitos failo lokacija: % s' % args.output)
else:
    print('Nenurodytas csv failas')
    exit(1)

portDict = readCsv(csvDir)
portDictOld = readCsv(csvDirOld)

changedPorts = comparePorts()

csv_columns = ['IP address', 'port']
try:
    with open(csvOutDir, 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(['Ip address', 'port'])
        for key, value in changedPorts.items():
            writer.writerow([key, value])
except IOError:
    print("I/O error")


