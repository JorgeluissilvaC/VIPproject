# -*- coding: utf-8 -*-
# encoding: utf-8
"""
Script entrenamiento para los dos dispositivos Emotiv Epoc
"""
import pygame
import random
import time 
import numpy as np
import scipy.io as sio
import winsound         # for sound  
from pylsl import StreamInlet, resolve_stream
"""
Tareas:
    Eliminar base de datos
    Incluir procesamiento
    Trabajar con archivos locales 
    producir el .arff
"""
class game(object):

    def __init__ (self, id_s = "unknown",rept = 1, width = 800, height = 600, fps = 30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("VIP: BCI")
        self.width = width
        self.height = height
        self.id_s = str(id_s)
        self.rept = int(rept)
        #self.height = width // 4
        self.dimensions = (self.width, self.height)
        #self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.screen.fill((255,255,255))#Fondo blanco
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 40, bold=True)
        size_screen= self.screen.get_size();
        self.x_center = size_screen[0]/2.0 - 210
        self.y_center = size_screen[1]/2.0 - 210
        
    def run(self):
        """The mainloop
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_s:
                        print ("[!] Preparation stage started")
                        self.preparation()
                        print ("[!] Preparation stage Finished")
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("BCI")
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
        pygame.quit()

    def draw_text(self, text, color = (100, 255, 100), dw = 0, dh = 0):
        """Center text in window"""
        fw, fh = self.font.size(text) # fw: font width,  fh: font height
        surface = self.font.render(text, True, color)
        # // makes integer division in python3
        self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))

    def  preparation(self):
        ntrial = 0
        t = 25; #tiempo de muestra
        datac = np.zeros((self.rept,t*500,8));
        datar = np.zeros((self.rept,t*500,8));
                        
        while(ntrial < self.rept):
            self.rest(10)
            j1 = self.concentration(t)
            winsound.Beep(800, 2000)
            self.rest(10)
            j2 = self.relaxation(t)
            self.Loading()
            datac[ntrial]=j1
            datar[ntrial]=j2
            ntrial+=1     
        self.saveDataDB(self.id_s,datac,datar)
        
    def concentration(self,t):
        g=random.randint(100,200)
        self.draw_text(str(g),(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        winsound.Beep(800, 2000)
        d = self.getDataO(t)
        return d
        
    def relaxation(self,t):
        self.draw_text("[+]",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        winsound.Beep(800, 2000)
        d = self.getDataO(t)
        return d

    def rest(self,t): 
        self.draw_text("Descanse",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(t)
    
    def Loading(self):
        self.draw_text("Cargando...",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(0.5)

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
        return data_time

    def saveDataDB(self,name,datac,datar):
        datac = np.transpose(datac,(1,2,0))
        datar = np.transpose(datar,(1,2,0))
        sio.savemat(name+'.mat',{'conc':datac, 'rel':datar})

if __name__ == '__main__':
    id_s = raw_input("[!] Digite el identificador del sujeto: ")
    rept = raw_input("[!] Digite la cantidad de pruebas a realizar: ")
    game(id_s,rept, 800, 600).run()


