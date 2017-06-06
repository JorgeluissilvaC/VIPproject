#### 		Read from Enobio EEG Data		####
# Este script lee los datos del Starstim y los almacena en un archivo .json

from pylsl import StreamInlet, resolve_stream
import json
import numpy as np

stream_name = 'NIC'
streams = resolve_stream('type', 'EEG')
fs = 500 # Frecuencia de muestreo
time = 1 # tiempo de muestreo
N=fs*time #Numero de muestras 
c=0;
muestras = []
trial = 3
tr=0
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
    data_time = np.array(muestras)
    
with open('prueba1' + '.json','w') as fp:
    json.dump(data_time,fp)