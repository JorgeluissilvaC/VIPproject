# -*- coding: utf-8 -*-
# encoding: utf-8
"""
Script entrenamiento para los dos dispositivos Emotiv Epoc
"""
import mysql.connector
import numpy as np
import pygame
import time 
import random
from pylsl import StreamInlet, resolve_stream
import winsound         # for sound  


class game(object):

    def __init__ (self, id_s = "unknown", width = 800, height = 600, fps = 30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("VIP: BCI")

        cnx = mysql.connector.connect(user =     'root', 
                                      password = '1234',
                                      host =     'localhost',
                                      database = 'Datos_temp')
        cursor = cnx.cursor()
        
        cursor.execute("show tables like 's_"+id_s+"'")
        lock = cursor.fetchall()
        print lock
        if lock != []:
            cursor.execute("SELECT MAX(n_trial) FROM s_"+id_s)
            n = cursor.fetchall()
            print n
            self.n = n[0][0]+1
            print n
        else:
            self.n = 0
            
        cursor.close()
        cnx.close()
        self.width = width
        self.height = height
        self.id_s = str(id_s)
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
        #self.f = [self.moveRightHand,self.moveLeftHand,self.moveObjectUp,self.moveObjectDown]
        self.f = [self.moveRightHand,self.moveLeftHand]
        self.imagenR= pygame.image.load("R1.png").convert()
        self.imagenL= pygame.image.load("R2.png").convert()
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
                        self.n = self.n + 1
                        #self.f = [self.moveRightHand,self.moveLeftHand,self.moveObjectUp,self.moveObjectDown]
                        self.f = [self.moveRightHand,self.moveLeftHand]
            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            self.draw_text("BCI")
            self.draw_text("Prueba: "+str(self.n)+" de s_"+self.id_s,(100,255,100),dh = -self.width // 6)
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
        d1=self.rest(4)     
        j1,cl1=random.choice(self.f)(7)
        d2=self.rest(4)
        j2,cl2=random.choice(self.f)(7)
        self.Loading()

        self.saveDataDB(d1, "r")
        self.saveDataDB(d2, "r")
        self.saveDataDB(j1, cl1)
        self.saveDataDB(j2, cl2)
        
    def moveRightHand(self,t):
        self.draw_text("X",(100,255,100))
        pygame.display.flip()
        winsound.Beep(440, 1000)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.imagenR, [self.x_center, self.y_center])
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        d = self.getDataO(t)
        self.f.remove(self.moveRightHand)
        clas="mrh"
        return d,clas

    def moveLeftHand(self,t):
        self.draw_text("X",(100,255,100))
        pygame.display.flip()
        winsound.Beep(440, 1000)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.imagenL, [self.x_center, self.y_center])
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        d = self.getDataO(t)
        self.f.remove(self.moveLeftHand)
        clas="mlh"
        return d,clas

    def rest(self,t): 
        self.draw_text("Descanse",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(0.5)
        d = self.getDataO(t)
        
        return d
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

        while c < N:
            sample, timestamp = inlet.pull_sample()
            muestras.append(sample)
            c += 1

        # Diccionario con los datos de los electrodos
        dic = {}
        for electrodos in range(0, len(sample)):
            dic[electrodos + 1] = []
            for muestra in muestras:
                dic[electrodos + 1].append(muestra[electrodos])

        return dic

    def saveDataDB(self, dic_of_list, test_type):
        add_table = (
            "CREATE TABLE IF NOT EXISTS `s_"+self.id_s+"` ("
            "  `n_sample` int(11) NOT NULL AUTO_INCREMENT,"
            "  `n_trial` int(11) NOT NULL,"
            "  `test_type` varchar(14) NOT NULL,"
            "   `e1` REAL NOT NULL,"
            "   `e2` REAL NOT NULL,"
            "   `e3` REAL NOT NULL,"
            "   `e4` REAL NOT NULL,"
            "   `e5` REAL NOT NULL,"
            "   `e6` REAL NOT NULL,"
            "   `e7` REAL NOT NULL,"
            "   `e8` REAL NOT NULL,"
            "  PRIMARY KEY (`n_sample`)"
            ") ENGINE=InnoDB")
        
        add_data = ("INSERT INTO s_"+self.id_s+
                       "(n_trial,test_type,e1,e2,e3,e4,e5,e6,e7,e8) "
                       "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        cnx = mysql.connector.connect(user =     'root', 
                                      password = '1234',
                                      host =     'localhost',
                                      database = 'Datos_temp')
        cursor = cnx.cursor()
        if (test_type == "mrh"):
            test_type=0
        elif (test_type == "mlh"):
            test_type=1
        elif (test_type == "mou"):
            test_type=2
        elif (test_type == "mod"):
            test_type=3
        elif (test_type == "r"):
            test_type=4
        cursor.execute(add_table)
        #sn = [[self.n,test_type]+[0]*8]*len(dic_of_list[1])
        #sn = np.zeros(len(dic_of_list[1]), dtype = "int8, string14, float32, float32, float32, float32, float32,float32,float32, float32")
        
        sn = np.zeros((len(dic_of_list[1]),len(dic_of_list)+2))
        for i in range(0,len(dic_of_list[1])):
            sn[i][0] = self.n
            sn[i][1] = (test_type)
        for key, value in dic_of_list.iteritems():
            for i in range(len(dic_of_list[key])):
                sn[i][key+1] = dic_of_list[key][i]
        cursor.executemany(add_data,sn.tolist())
        cnx.commit()
        cursor.close()
        cnx.close()
        print "[!]Table '"+"s_"+self.id_s+"' added/updated"
        

if __name__ == '__main__':
    id_s = raw_input("[!] Digite el identificador del sujeto: ")
    game(id_s, 800, 600).run()


