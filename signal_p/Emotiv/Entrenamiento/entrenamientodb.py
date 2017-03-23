
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
Script entrenamiento para los dos dispositivos Emotiv Epoc
"""
import pygame 
from emokit.emotiv import Emotiv
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time 
import json
from pylsl import StreamInlet, resolve_stream
import sqlite3
# import winsound

class game(object):

    def __init__ (self, n, width = 800, height = 600, fps = 30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("VIP: BCI")
        self.width = width
        self.height = height
        self.n = n
        #self.height = width // 4
        self.dimensions = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 20, bold=True)


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
                        self.n = str(int(self.n) + 1)
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("BCI")
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
        pygame.quit()


    def draw_text(self, text, color = (0, 255, 150), dw = 0, dh = 0):
        """Center text in window"""
        fw, fh = self.font.size(text) # fw: font width,  fh: font height
        surface = self.font.render(text, True, color)
        # // makes integer division in python3
        self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))

    def  preparation(self):  
        # Delays and constants
        trela1 = 5
        trela2 = 5
        tcont1 = 5
        tcont2 = 5
        freq = 60 #Hz
        t = 1000 #miliseconds
        #   Instructions - Etapa de relajacion 1
        self.draw_text("Etapa de preparación: Instrucciones")
        self.draw_text("Inhale:7s Mantenga:7s Exhale:7s",(100,255,100),dh = -self.width // 10)
        pygame.display.flip()
        time.sleep(3)
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Hagalo hasta escuchar una alerta de sonido",(100,255,100))
        self.draw_text("Cierre los ojos",(100,255,100),dh = -self.width // 6)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))   
        #   Se obtienen los datos
        r0 = self.getDataO(trela1)
        # winsound.Beep(freq,t)
        #   Etapa de concentracion 
        self.draw_text("Concentrese en el punto")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        pygame.draw.circle(self.screen, (255,255,255), (400,300), 5, 0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        #   Se obtienen los datos
        c0 = self.getDataO(tcont1)
        #   Etapa de relajacion 
        self.draw_text("Relajese")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(1)
        #   Se obtienen los datos
        r1 = self.getDataO(trela2)
        #   Etapa de concentracion 2
        self.draw_text("Imagine que mueve el cuadrado")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        pygame.draw.rect(self.screen, (255,255,255), [self.width//2 - 50,self.height//2 - 50, 100, 100],0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        #   Se obtienen los datos
        c1 = self.getDataO(tcont2)
        #   Se guardan los datos
        self.saveDataDB(r0, "r0")
        self.saveDataDB(c0, "c0")
        self.saveDataDB(c1, "c1")
        self.saveDataDB(r1, "r1") 

    def getDataO(self, tm):
        fs = 128.0    #Frecuencia de muestreo
        N = fs*tm     #Numero de muestras
        ct = 0        #Contador
        dt = []       #Vector de datos
        with Emotiv(display_output=False, verbose=True) as headset:
            while ct < N:
                packet = headset.dequeue()
                if packet is not None:
                    # print packet.sensors
                    # print "########################" 
                    dic = {}
                    for key, value in packet.sensors.iteritems():
                        value = packet.sensors[key]['value']
                        quality = packet.sensors[key]['quality']
                        dic[key] = (value,quality)                
                    dt.append(dic)                
                    ct+=1
                time.sleep(0.007)
                
        return dt

    def saveDataDB(self, list_of_dic, test_type):
        conn = sqlite3.connect('database.db') #connection object
        c = conn.cursor()
        # Create table
        
        c.execute('''CREATE TABLE IF NOT EXISTS '''+"s"+self.n+'''
                (n_sample INTEGER PRIMARY KEY,
                test_type TEXT NOT NULL,
                AF3 REAL NOT NULL,
                AF4 REAL NOT NULL,
                F3 REAL NOT NULL,
                F4 REAL NOT NULL,
                F7 REAL NOT NULL,
                F8 REAL NOT NULL,
                FC5 REAL NOT NULL,
                FC6 REAL NOT NULL,
                T7 REAL NOT NULL,
                T8 REAL NOT NULL,
                P7 REAL NOT NULL,
                P8 REAL NOT NULL,
                O1 REAL NOT NULL,
                O2 REAL NOT NULL)''')
        sn_m = []
        for n_s in list_of_dic :
            sn = [0]*15
            sn[0] = test_type
            for key, value in n_s.iteritems():
                if key == "AF3":
                    sn[1] = value[0]
                elif key == "AF4":
                    sn[2] = value[0]
                elif key == "F3":
                    sn[3] = value[0]
                elif key == "F4":
                    sn[4] = value[0]
                elif key == "F7":
                    sn[5] = value[0]
                elif key == "F8":
                    sn[6] = value[0]
                elif key == "FC5":
                    sn[7] = value[0]
                elif key == "FC6":
                    sn[8] = value[0]
                elif key == "T7":
                    sn[9] = value[0]
                elif key == "T8":
                    sn[10] = value[0]
                elif key == "P7":
                    sn[11] = value[0]
                elif key == "P8":
                    sn[12] = value[0]
                elif key == "01":
                    sn[13] = value[0]
                elif key == "02":
                    sn[14] = value[0]
            sn_m.append(tuple(sn))
        #print sn_m
        c.executemany('''INSERT INTO '''+"s"+self.n+''' VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', sn_m)
        conn.commit()
        conn.close()
        print "[!]Table: '"+"s"+self.n+"' added/updated"

if __name__ == '__main__':
    n = 0
    game(str(n), 800, 600).run()

