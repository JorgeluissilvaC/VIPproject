#### 		Read from Enobio EEG Data		####
# Este script lee los datos del Starstim y los almacena en un archivo .json

from pylsl import StreamInlet, resolve_stream
import json

stream_name = 'NIC'
streams = resolve_stream('type', 'EEG')
fs = 500 # Frecuencia de muestreo
time = 10 # tiempo de muestreo
N=fs*time #Numero de muestras 
c=0;
muestras = []
try:
	for i in range (len(streams)):

		if (streams[i].name() == stream_name):
			index = i
			print ("NIC stream available")

	print ("Connecting to NIC stream... \n")
	inlet = StreamInlet(streams[index])   

except NameError:
	print ("Error: NIC stream not available\n\n\n")

while c<N:
    sample, timestamp = inlet.pull_sample()
    muestras.append(sample)
    c+=1
    
#Diccionario con los datos de los electrodos
dic = {} 
for electrodos in range(0,len(sample)):
    dic[electrodos+1] = []
    for muestra in muestras:
        dic[electrodos+1].append(muestra[electrodos])

print "ready"