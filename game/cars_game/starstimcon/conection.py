from pylsl import StreamInlet, resolve_stream
import numpy as np

class Ssc:
	def __init__ (self, master):
		self.master = master
		
	def getData(self, tm):
		stream_name = 'NIC'
		streams = resolve_stream('type', 'EEG')
		fs = 500  # Frecuencia de muestreo
		N = fs * tm  # Numero de muestras
		c = 0;
		muestras = []
		try:
			for i in range(len(streams)):

				if streams[i].name() == stream_name:
					index = i
					print ("NIC stream available")

			print ("Connecting to NIC stream... \n")
			inlet = StreamInlet(streams[index])

		except NameError:
			print ("Error: NIC stream not available\n\n\n")
		data_time = np.zeros((N,8))
		while c < N:
			sample, timestamp = inlet.pull_sample()
			muestras.append(sample)
			c += 1

		# Diccionario con los datos de los electrodos
		data_time = np.array(muestras)      
		self.master.saveData(data_time)