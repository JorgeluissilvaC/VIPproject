#from scipy.signal import butter, lfilter
"""
Filtro Pasabanda Butterworth 
"""
from scipy import signal
import numpy as np

def butter_bandpass_filter(data,lowcut=8, highcut=12,fs=500, order=6):
	nyq = 0.5*fs;
	low = lowcut/nyq
	high= highcut/nyq
	b, a = signal.butter(order, [low,high], btype ='band')
	y = signal.lfilter(b, a, data)
	f, pxx = signal.welch(y, fs)  
	max_value = np.amax(pxx)
	return y,max_value, pxx, f

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	fs = 500
	N = 1e5
	amp = 2*np.sqrt(2)
	freq = 20
	noise_power = 0.001 * fs / 2
	time = np.arange(N) / fs
	x = amp*np.sin(2*np.pi*freq*time)
	x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
	rs,mv,pxx, f = butter_bandpass_filter(x)
	plt.figure()    
	plt.semilogy(f, pxx)
	plt.ylim([0.5e-3, 1])
	plt.xlabel('frequency [Hz]')
	plt.ylabel('PSD [V**2/Hz]')
	plt.show()
	plt.figure()
	plt.semilogy(f, pxx)
	plt.ylim([0.5e-3, 1])
	plt.xlabel('frequency [Hz]')
	plt.ylabel('PSD [V**2/Hz]')
	plt.show()
