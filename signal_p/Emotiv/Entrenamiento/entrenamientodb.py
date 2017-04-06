
# -*- coding: utf-8 -*-
# encoding: utf-8
"""
Script entrenamiento para los dos dispositivos Emotiv Epoc
"""
import mysql.connector
import pygame
from emokit.emotiv import Emotiv
import time 
import random
# import winsound

class game(object):

    def __init__ (self, id_s = "unknown", width = 800, height = 600, fps = 30):
        """Initialize pygame, window, background, font,...
        """
        pygame.init()
        pygame.display.set_caption("VIP: BCI")
        cnx = mysql.connector.connect(user =     'root', 
                                      password = 'uniatlantico',
                                      host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                      database = 'vipdb')
        cursor = cnx.cursor()
        
        cursor.execute("show tables like 's_"+id_s+"'")
        lock = cursor.fetchall()
        print lock
        if lock != []:
            cursor.execute("SELECT MAX(n_trial) FROM s_"+id_s)
            n = cursor.fetchall()
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
        self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 20, bold=True)
        self.f = [self.moveRightArm,self.moveLeftArm,self.moveObjectUp,self.moveObjectDown]

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
                        self.f = [self.moveRightArm,self.moveLeftArm,self.moveObjectUp,self.moveObjectDown]
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
        self.rest(4)
        random.choice(self.f)(7)
        self.rest(4)
        random.choice(self.f)(7)
        self.rest(4)
        random.choice(self.f)(7)
        self.rest(4)
        random.choice(self.f)(7)


    def moveRightArm(self,t):
        self.draw_text("Imagine que mueve la mano derecha",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        d = self.getDataO(t)
        self.saveDataDB(d, "mra")
        self.f.remove(self.moveRightArm)

    def moveLeftArm(self,t):
        self.draw_text("Imagine que mueve la mano izquierda",(100,255,100))
        pygame.display.flip()
        time.sleep(4)
        self.screen.blit(self.background, (0, 0))
        d = self.getDataO(t)
        self.saveDataDB(d, "mla")
        self.f.remove(self.moveLeftArm)

    def moveObjectUp(self,t): 
        self.draw_text("Imagine que mueve el objeto hacia arriba",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        pygame.draw.rect(self.screen, (225,225,255), [self.width//2 - 50,self.height//2 - 50, 100, 100],0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        d = self.getDataO(t)
        self.saveDataDB(d, "mou")
        self.f.remove(self.moveObjectUp)

    def moveObjectDown(self,t): 
        self.draw_text("Imagine que mueve el objeto hacia abajo",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        pygame.draw.circle(self.screen, (255,255,255), (400,300), 5, 0)
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        d = self.getDataO(t)
        self.saveDataDB(d, "mod")
        self.f.remove(self.moveObjectDown)

    def rest(self,t): 
        self.draw_text("Descanse",(100,255,100))
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        time.sleep(4)
        d = self.getDataO(t)
        self.saveDataDB(d, "r")

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
        add_table = (
            "CREATE TABLE IF NOT EXISTS `s_"+self.id_s+"` ("
            "  `n_sample` int(11) NOT NULL AUTO_INCREMENT,"
            "  `n_trial` int(11) NOT NULL,"
            "  `test_type` varchar(14) NOT NULL,"
            "   `AF3` REAL NOT NULL,"
            "   `AF4` REAL NOT NULL,"
            "   `F3` REAL NOT NULL,"
            "   `F4` REAL NOT NULL,"
            "   `F7` REAL NOT NULL,"
            "   `F8` REAL NOT NULL,"
            "   `FC5` REAL NOT NULL,"
            "   `FC6` REAL NOT NULL,"
            "   `T7` REAL NOT NULL,"
            "   `T8` REAL NOT NULL,"
            "   `P7` REAL NOT NULL,"
            "   `P8` REAL NOT NULL,"
            "   `O1` REAL NOT NULL,"
            "   `O2` REAL NOT NULL,"
            "  PRIMARY KEY (`n_sample`)"
            ") ENGINE=InnoDB")
        
        add_data = ("INSERT INTO s_"+self.id_s+
                       "(n_trial,test_type,AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8,O1,O2) "
                       "VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)")
        
        cnx = mysql.connector.connect(user =     'root', 
                                      password = 'uniatlantico',
                                      host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                      database = 'vipdb')
        cursor = cnx.cursor()
        
        cursor.execute(add_table)
        
        sn_m = []
        for n_s in list_of_dic :
            sn = [0]*16
            sn[0] = self.n
            sn[1] = test_type
            for key, value in n_s.iteritems():
                if key == "AF3":
                    sn[2] = value[0]
                elif key == "AF4":
                    sn[3] = value[0]
                elif key == "F3":
                    sn[4] = value[0]
                elif key == "F4":
                    sn[5] = value[0]
                elif key == "F7":
                    sn[6] = value[0]
                elif key == "F8":
                    sn[7] = value[0]
                elif key == "FC5":
                    sn[8] = value[0]
                elif key == "FC6":
                    sn[9] = value[0]
                elif key == "T7":
                    sn[10] = value[0]
                elif key == "T8":
                    sn[11] = value[0]
                elif key == "P7":
                    sn[12] = value[0]
                elif key == "P8":
                    sn[13] = value[0]
                elif key == "01":
                    sn[14] = value[0]
                elif key == "02":
                    sn[15] = value[0]
            sn_m.append(tuple(sn))
        #print sn_m
        cursor.executemany(add_data,sn_m)
        cnx.commit()
        cursor.close()
        cnx.close()
        print "[!]Table '"+"s_"+self.id_s+"' added/updated"

if __name__ == '__main__':
    id_s = raw_input("[!] Digite el identificador del sujeto: ")
    game(id_s, 800, 600).run()


