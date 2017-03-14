# -*- coding: utf-8 -*-
"""
Script entrenamiento para los dos dispositivos Emotiv Epoc & Starstim
disp = 1 Emotiv 
disp = 0 Starstim
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
        self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
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
                        print ("Preparation stage started")
                        self.preparation()
                        print ("Preparation stage Finished")
                    elif event.key == pygame.K_t:
                        print ("Training stage started")
                        print ("Training stage finished")
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
        #   Credits to Mike Koenig - Se carga la cancion 
        #pygame.mixer.music.load('drop.mp3')
        trela1 = 2
        trela2 = 2
        tcont1 = 2
        tcont2 = 2
        #   Instructions - Etapa de relajacion 1
        self.draw_text("Preparation stage: Instrunctions")
        self.draw_text("Inhale:7s Retain:7s Exhale:7s",(100,255,100),dh = -self.width // 10)
        pygame.display.flip()
        time.sleep(3)
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Do it until you hear the alert sound",(100,255,100))
        self.draw_text("Close your eyes",(100,255,100),dh = -self.width // 6)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))   
        #   Se obtienen los datos
        y,dic_raw = self.getDataO(trela1)
        #pygame.mixer.music.play(0)
        #   Se guardan los datos
        # with open('relajacion1.json', 'w') as fp:
        #     json.dump(y, fp)
        self.saveDataDB(dic_raw, "r0")
        #   Etapa de concentracion 
        self.draw_text("Concentrese en el punto")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        pygame.draw.circle(self.screen, (255,255,255), (400,300), 5, 0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))

        #   Se obtienen los datos
        del y , dic_raw
        y,dic_raw = self.getDataO(tcont1)
        #       Se guardan los datos
        # with open('concentration1.json', 'w') as fp:
        #     json.dump(y, fp)
        self.saveDataDB(dic_raw, "c0")
        #   Etapa de relajacion 
        self.draw_text("Relax")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        #   Se obtienen los datos
        del y, dic_raw
        y,dic_raw = self.getDataO(trela2)
        #   Se guardan los datos
        # with open('Relajacion2.json', 'w') as fp:
        #     json.dump(y, fp)
        self.saveDataDB(dic_raw, "r1")        
        #   Etapa de concentracion 2
        self.draw_text("Imagine que mueve el cuadrado")
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        pygame.draw.rect(self.screen, (255,255,255), [self.width//2 - 50,self.height//2 - 50, 100, 100],0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))

        #   Se obtienen los datos
        del y , dic_raw
        y ,dic_raw= self.getDataO(tcont2)
        #   Se guardan los datos
        with open('concentration2.json', 'w') as fp:
            json.dump(y, fp)
        

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
        ldic = dt[:]
        dicx = ldic[0].copy()
        for key,value in dicx.iteritems():
            dicx[key] = []

        for i in ldic:
            for key, value in i.iteritems():
                value = i[key][0]
                quality = i[key][1]
                dicx[key].append((quality,value))
                pass
        return dicx, ldic

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

            c.execute('''INSERT INTO '''+"s"+self.n+''' VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', sn)
            conn.commit()
        conn.close()
        print "[!]Table: '"+"s"+self.n+"' added/updated"

if __name__ == '__main__':
    n = 0
    while(True):
        game(str(n), 800, 600).run()
        n += 1
