# Questo script serve per interfacciarsi con Arduino Due usato con lo sketch arducal.ino
# L'interfacciamento avviene attraverso:
# 1. scrittura di un carattere sulla linea seriale, necessario per far partire l'acquisizione
# 2. lettura dei dati disponibili su porta seriale

import serial # libreria per gestione porta seriale (USB)
import time # libreria per temporizzazione
import numpy

Directory='home/studenti/dati_arduino/'   # nome directory dati <<< DA CAMBIARE SECONDO NECESSITA'

FileName=Directory+'datacal.txt'  # parte comune nome file << DA CAMBIARE SECONDO NECESSITA'

outputFile = open(FileName, "w" ) # apre file dati predisposto per scrittura

print('Please wait') # scrive di aspettare sulla console


ard=serial.Serial('/dev/ttyACM0',119200)  # apre porta seriale (occhio alla sintassi, dipende dal sistema operativo!)
time.sleep(2) # aspetta due secondi per evitare casini

print('Start Acquisition') # scrive sulla console (terminale)

ard.write(b'G') # scrive un carattere sulla linea seriale; l'istruzione b indica che e' un byte (carattere ASCII)
time.sleep(2) # aspetta due secondi per evitare casini

# loop lettura dati da seriale (8192 coppie di dati: tempo in us, valore digitalizzato di d.d.p.)
runningddp=numpy.zeros(8192) # prepara il vettore per la determinazione della ddp media e std

for i in range (0,8192):
        data = ard.readline().decode() # legge il dato e lo decodifica
        if data:
            outputFile.write(data) # scrive i dati sul file
            runningddp[i]=data[data.find(' '):len(data)] # estrae le ddp e le mette nel vettore

ard.close() # chiude la comunicazione seriale con Arduino

avgddp=numpy.average(runningddp) # analizza il file per trovare la media
stdddp=numpy.std(runningddp) # e la deviazione standard

print('Average and exp std:', avgddp, '+/-',stdddp) # le scrive sulla console

outputFile.close() # chiude il file dei dati

print('end, ciao') # scrive sulla console che ha finito e vi saluta
