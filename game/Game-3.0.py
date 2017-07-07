# -*- coding: utf-8 -*-
import pygame
import time 
from scipy import signal
import scipy.io as sio
import numpy as np
from sklearn import preprocessing
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from pylsl import StreamInlet, resolve_stream
import random
import winsound
from sklearn.model_selection import cross_val_score
# Definimos algunos colores
VERDE   = (0, 255, 150)
#-------------------------------------------------------------------------------------

class game(object):

    def __init__ (self,ID="unknown", width=800, height=600, fps=60):
        """Initialize pygame, window, background, font,..."""
        pygame.init()
        pygame.display.set_caption("VIP: BCI")
        self.width = width
        self.height = height
        self.dimensions = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
        #self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('mono', 40, bold=True)
        self.fps = fps
        self.playtime = 0.0
        self.r=5
        self.ID=ID
        
    def run(self):
        """The mainloop"""
        #Entrenamiento del clasificador
        [data_ext, label]= self.getDataExt(self.ID)
        feats = self.processing(data_ext)
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
        X_train_minmax = min_max_scaler.fit_transform(feats)
        ind = self.modelInd(self.ID)
        X_train = X_train_minmax[:,ind]
        """
        Clasificación
        """
        # Se crea el clasificador
        clf = svm.SVC(kernel='linear', C=1)
        #Se entrena el clasificador con las mejores características
        clf.fit(X_train, label)
        #Seleccionar los indicies de las características importantes -----------
        ntrial = 0
        #----------------------------------------------------------------------
        hecho = False
        #----------------------------------------------------------------------
        self.draw_text("BCI Game")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(1)
        #----------------------------------------------------------------------
        self.draw_text("Instrucciones ",VERDE,  0, 300)
        self.draw_text("-Solo usa tu mente-",VERDE, 0 ,100)
        self.draw_text(".:COMIENZA:.",VERDE, 0 ,0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(1)        
        #----------------------------------------------------------------------
        while not hecho:
            # --- Bucle principal de eventos            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: 
                    print("Se presionó el boton cerrar")
                    hecho = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        hecho = True
                        print("Se presionó la techa escape")
            #----------------------------------------       
            
            dtTem1 = self.concentration(5,3)
            FEATS1 = self.processing(dtTem1)
            #Se escalan los datos 
            X_test_min = min_max_scaler.transform(FEATS1)
            X_test = X_test_min[:,ind]
            dtPs = X_test
            lab1 = 0
            #--------------------------------------------------------------------
            winsound.Beep(800,1000)
            cls=clf.predict(dtPs)
            print str(cls) +"tem1"
            if (cls == 1):
                self.good()
                time.sleep(2)
                lab1 = 1
            elif (cls == 2):
                self.bad()
                time.sleep(2)
                
            self.rest(3)
            #----------------------------------------

            dtTem2 = self.relaxation(5,3)
            FEATS2 = self.processing(dtTem2)
            #Se escalan los datos 
            X_test_min = min_max_scaler.transform(FEATS2)
            X_test = X_test_min[:,ind]
            
            dtPs = X_test
            #--------------------------------------------------------------------
            lab2=0
            cls=clf.predict(dtPs)
            print str(cls) +"tem2"
            winsound.Beep(800,1000)
            if (cls == 1):
                self.bad()
                time.sleep(2)
                
            elif (cls == 2):
                self.good()
                time.sleep(2)
                lab2=1 
            
            ntrial+=1
            self.saveDataDB(self.ID+str(ntrial),dtTem1,dtTem2,lab1,lab2)
#            pygame.draw.rect(self.screen,VERDE, [x,y, 100, 100])
#            pygame.display.flip()
#            self.screen.blit(self.background, (0, 0))
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
        pygame.quit()
         
    def draw_text(self, text, color = VERDE, dw = 0, dh = 0):
        """Center text in window"""
        fw, fh = self.font.size(text) # fw: font width,  fh: font height
        surface = self.font.render(text, True, color)
        # // makes integer division in python3
        self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))
        
    def concentration(self,t,timeOut):
        g=random.randint(100,200)
        self.draw_text(str(g),(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(timeOut)
        d = self.getDataO(t)
        return d
    
    def good(self):
        self.draw_text("Bien :) ",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))

    def bad(self):
        self.draw_text("Mal :( ",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
   
    def relaxation(self,t,timeOut):
        self.draw_text("[+]",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(timeOut)
        d = self.getDataO(t)
        return d
    
    def saveDataDB(self,name,d1,d2,label1,label2):        
        datac = d1
        datar = d2
        sio.savemat(name+'.mat',{'conc':datac, 'rel':datar,'lab1':label1,'lab2':label2})
        
    def rest(self,t): 
        self.draw_text("Descanse",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(t)
    
    def getDataO(self, tm):
        
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
        """importa los datos del dataset.--------------------------------------
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
        [D_DC, m_v] = self.remove_dc(dataTime)
        Y = self.butter_filter(D_DC)
        SCALE = 8
        FS = 500/SCALE # esto es porque fue submuestreado a 2
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
        
    def butter_filter(self,data, highcut=30, fqc=500, order=6):
        """Filtro pasabajas.
        """
        nyq = 0.5*fqc
        high = highcut/nyq
        [b_c, a_c] = signal.butter(order, high, btype='low')
        filt_sig = signal.lfilter(b_c, a_c, data)
        return filt_sig
    
    def remove_dc(self,data):
        """ Remueve el DC de una señal."""
        
        dim = len(data.shape)
        ndata = np.zeros(np.shape(data))
        if (dim == 3):
            mean_v = np.mean(data, axis=2)
            for trial in range(0, len(data)):
                for electrode in range(0, len(data[trial])):
                    # Señal original -  señal DC
                    v_trial = (data[trial][electrode] - mean_v[trial][electrode])
                    ndata[trial][electrode] = v_trial # guardamos señal sin DC
        
        elif (dim == 2):
            mean_v = np.mean(data, axis=1)
            for electrode in range(0, len(data)):
                    # Señal original -  señal DC
                    v_trial = (data[electrode] - mean_v[electrode])
                    ndata[electrode] = v_trial # guardamos señal sin DC
        return ndata, mean_v
     
    def down_sampling(self,data, sc_v, div):
        """Reduce la frecuencia de muestreo de una señal.
        """
        dim = len(data.shape)
        if (dim == 3):
            if ((div % 2) != 0):
                sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc_v+1))
            else:
                sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc_v))
        
            for trial in range(0, len(data)):
                for electrode in range(0, len(data[trial])):
                    sub_signals[trial][electrode] = data[trial][electrode][::sc_v]
        
        elif (dim == 2):    
            if ((div % 2) != 0):
                sub_signals = np.zeros((len(data), len(data[0])/sc_v+1))
            else:
                sub_signals = np.zeros((len(data), len(data[0])/sc_v))
            for number in range(0, len(data)):
                    sub_signals[number] = data[number][::sc_v]
        return sub_signals
    
    def modelInd(self, S_ID):
        indm = np.load('ind'+S_ID+'.npy')
        return indm
    
if __name__ == '__main__':
    # call with width of window and fps
    #S_ID = raw_input("[!] Digite el identificador del sujeto: ")
    S_ID="dayan0407"
    game(S_ID).run()