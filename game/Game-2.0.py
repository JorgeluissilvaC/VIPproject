# -*- coding: utf-8 -*-
import pygame
import time 
from scipy import signal
import scipy.io as sio
import numpy as np
from sklearn import preprocessing
from sklearn import svm
from pylsl import StreamInlet, resolve_stream

# Colors
Green   = (0, 255, 150)
#-------------------------------------------------------------------------------------
class game(object):

    def __init__ (self,ID="unknown", width=800, height=600, fps=60):
        """Initialize pygame, window, background, font,..."""
        pygame.init()
        pygame.display.set_caption("VIP: BCI")
        self.width = width
        self.height = height
        self.dimensions = (self.width, self.height)
        #self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('mono', 40, bold=True)
        self.fps = fps
        self.playtime = 0.0
        self.r=5
        self.ID=ID
        
    def run(self):
        """The mainloop"""
        #Training of the clasificator.
        [data_ext, label]= self.getDataExt(self.ID)
        feats = self.processing(data_ext)
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
        X_train_minmax = min_max_scaler.fit_transform(feats)
        ind = self.modelInd(self.ID)#Importing the model of clasificator.
        X_train = X_train_minmax[:,ind]
        """
        classification
        """
        # Creating clasifictor. 
        clf = svm.SVC(kernel='linear', C=1)
        #Training the clasificator with the best features. 
        clf.fit(X_train, label)
        #----------------------------------------------------------------------
        hecho = False
        x = (self.width/2)-50
        y = (self.height/2)-50
        #----------------------------------------------------------------------
        self.draw_text("BCI Game")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(3)
        #----------------------------------------------------------------------
        self.draw_text("Instrucciones ",Green,  0, 300)
        self.draw_text("-Solo usa tu mente-",Green, 0 ,100)
        self.draw_text(".:COMIENZA:.",Green, 0 ,0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(5)        
        #----------------------------------------------------------------------
        while not hecho:            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: 
                    print("Se presionó el boton cerrar")
                    hecho = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        hecho = True
                        print("Se presionó la techa escape")
            #----------------------------------------        
            dtTem = self.getDataO(5)
            FEATS1 = self.processing(dtTem)
            X_test_min = min_max_scaler.transform(FEATS1)
            X_test = X_test_min[:,ind]
            dtPs = X_test
            #--------------------------------------------------------------------
            cls=clf.predict(dtPs)
            print cls
            if (cls == 1):
                y=y-self.r
                
            elif (cls == 2):
                y=y+self.r
            #----------------------------------------
            pygame.draw.rect(self.screen,Green, [x,y, 100, 100])
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
        pygame.quit()
         
    def draw_text(self, text, color = Green, dw = 0, dh = 0):
        """Center text in window"""
        fw, fh = self.font.size(text) # fw: font width,  fh: font height
        surface = self.font.render(text, True, color)
        # // makes integer division in python3
        self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))
        

    def getDataO(self, tm):
        """ getData(tm)
            .:Description:
            Getting the data from STARSTIM. The rate is of 500 samples per second.
            
            .:Input parameters:.
            tm: Time to obtain data.
            
            .:Ouput:.
            data_time: Numpy array. 2D [8 electrodes][500*tm Sample] 
        """
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
        data_time = np.transpose(data_time,(1,0))
        """
        data_time = np.random.random((8,tm*500))
        #data_time = np.transpose(data_time,(1,0))
        """
        return data_time
    
    def getDataExt(self,id_s):
        """ getDataExt(id_s)
            .:Description:
            Getting training data of dataset for specific person.
            
            .:Input parameters:.
            Id_s:Username
            
            .:Ouput:.
            data_time:3D[trials][8 electrodes][500*(Test time) Samples]
            LABELS:labels of different trials. 
        """
        mat_contents = sio.loadmat(id_s)
        conc = mat_contents['conc']
        rel = mat_contents['rel']
        dim=len(rel.shape)
        if (dim==3):
            conc = np.transpose(conc, (2, 1, 0))
            rel = np.transpose(rel, (2, 1, 0))
            data_time = np.zeros((len(conc)*2, len(conc[0]), len(conc[0][0])))
            data_time[0:len(conc)] = conc
            data_time[len(conc)::] = rel
            
        if (dim ==2):
            data_time = np.zeros((2,len(conc), len(conc[0])))
            data_time[0:len(conc)] = conc
            data_time[len(conc)::] = rel
        
        LABELS = np.zeros((data_time.shape[0]))
        LABELS[0:len(LABELS)/2] = 1
        LABELS[len(LABELS)/2::] = 2
        return data_time, LABELS

    def processing(self,dataTime):
        """ processing(dataTime)
            .:Description:
            Creating the features array.
            1-Removing DC.
            2-Filtering the signals in the time on a betha band.
            3-Reducing the quantity of samples.
            4-Making the spectrogram of the data. Parameters:Sample frequency.
            5-Mean of data in time for each frequency band of spectrogram.
            6-Organising features array for the clasificator.
            .:Input parameters:.
            dataTime: Samples in the time for get the features array.
                      2D[8 electrodes][500*(Test time) Samples] or 
                      3D [trials][8 electrodes][500*(Test time) Samples]
            .:Ouput:.
            FEATS:2D [Trial][(8 Electrodes)*(N Spectrogram frequency) Features]
        """
        D_DC = self.remove_dc(dataTime)
        Y = self.butter_filter(D_DC)
        SCALE = 8
        FS = 500/SCALE # esto es porque fue submuestreado a SCALE
        DIV = 500.0/SCALE
        SUB_SIGNAL = self.down_sampling(Y, int(SCALE), DIV)
        F, T, S = signal.spectrogram(SUB_SIGNAL, fs=FS)
        ff = SUB_SIGNAL.shape # Tamaño del array
        dimen = len(ff)
        if (dimen == 3):
            M_F = np.mean(S, axis=3) # Potencia promedio para cada frecuencia
            FEATS = np.reshape(M_F, (ff[0], M_F.shape[2]*ff[1]))
        elif (dimen == 2):    
            M_F = np.mean(S, axis=2) # Potencia promedio para cada frecuencia
            FEATS = M_F
            FEATS = np.reshape(FEATS, (M_F.shape[0]*M_F.shape[1],1))
            FEATS = FEATS.T

        return FEATS

    def saveDataDB(self,name,d1,d2):
        """saveDataDB(name,d1,d2)
            .:Description:
            Save the information in Matlab format on a local file.
            .:Input parameters:.
            name: This is the name with the file will be saved.
            d1:Data for save.
            d2:Data for save.
                
            .:Ouput:.
            Username.mat: The file on the folder where the algorithm is saved.
            Data description:...
        """
        datac = np.transpose(d1,(1,2,0))
        datar = np.transpose(d2,(1,2,0))
        sio.savemat(name+'.mat',{'conc':datac, 'rel':datar})

        
    def butter_filter(self,d, highcut=25, fqc=500, order=6):
        """Filtro pasabajas.
            .:Description:
            Low pass filter with highcut on 25 Hz.
            .:Input parameters:.
            d: Signal to filter.
            .:Ouput:.
            filt_sig: Filtered signal. It has the same way that the input.
        """
        nyq = 0.5*fqc
        high = highcut/nyq
        [b_c, a_c] = signal.butter(order, high, btype='low')
        filt_sig = signal.lfilter(b_c, a_c, d)
        return filt_sig
    
    def remove_dc(self,dta):
        """ remove_dc(dta)
            .:Description:
            Delete the mean of each signal for each electrode.
            .:Input parameters:.
            dta:Data time on with DC. 
            .:Ouput:. 
            ndata:Data time on without DC. It has the same way that the input.
        """
        
        dim = len(dta.shape)
        ndata = np.zeros(np.shape(dta))
        if (dim == 3):
            mean_v = np.mean(dta, axis=2)
            for trial in range(0, len(dta)):
                for electrode in range(0, len(dta[trial])):
                    # Señal original -  señal DC
                    v_trial = (dta[trial][electrode] - mean_v[trial][electrode])
                    ndata[trial][electrode] = v_trial # guardamos señal sin DC
        
        elif (dim == 2):
            mean_v = np.mean(dta, axis=1)
            for electrode in range(0, len(dta)):
                    # Señal original -  señal DC
                    v_trial = (dta[electrode] - mean_v[electrode])
                    ndata[electrode] = v_trial # guardamos señal sin DC
        return ndata
     
    def down_sampling(self,da, sc_v, div):
        """down_sampling(data, sc_v, div)
            .:Description:
            Reducing the sample frequency.
            
            .:Input parameters:.
            da: Data with complete samples.
            sc_v: Desired factor.
            div: 	Desired subdivision.
            .:Ouput:.  
            sub_signals: Signal with less samples. This reduction is with a particular factor.
            
        """
        dim = len(da.shape)
        if (dim == 3):
            if ((div % 2) != 0):
                sub_signals = np.zeros((len(da), len(da[0]), len(da[0][0])/sc_v+1))
            else:
                sub_signals = np.zeros((len(da), len(da[0]), len(da[0][0])/sc_v))
        
            for trial in range(0, len(da)):
                for electrode in range(0, len(da[trial])):
                    sub_signals[trial][electrode] = da[trial][electrode][::sc_v]
        
        elif (dim == 2):    
            if ((div % 2) != 0):
                sub_signals = np.zeros((len(da), len(da[0])/sc_v+1))
            else:
                sub_signals = np.zeros((len(da), len(da[0])/sc_v))
            for number in range(0, len(da)):
                    sub_signals[number] = da[number][::sc_v]
        return sub_signals
    
    def modelInd(self, S_ID):
        """Reduce la frecuencia de muestreo de una señal.
            .:Description:
            Importing the model created on the training. This is specific for each person.
            
            .:Input parameters:.
            ID_S:Username
            
            .:Ouput:.
            indm: Model's indexes.
        """
        indm = np.load('ind'+S_ID+'.npy')
        return indm

if __name__ == '__main__':
    # call with width of window and fps
    #S_ID = raw_input("[!] Digite el identificador del sujeto: ")
    S_ID="dayan0407"
    game(S_ID).run()