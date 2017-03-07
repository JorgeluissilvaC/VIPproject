# -*- coding: utf-8 -*-
import pygame 
from emokit.emotiv import Emotiv
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time 
import csv

class game(object):

	def __init__ (self, width=800, height=600, fps=30):
		"""Initialize pygame, window, background, font,..."""
		pygame.init()
		pygame.display.set_caption("VIP: BCI")
		self.width = width
		self.height = height
		#self.height = width // 4
		self.dimensions = (self.width, self.height)
		self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.clock = pygame.time.Clock()
		self.fps = fps
		self.playtime = 0.0
		self.font = pygame.font.SysFont('mono', 20, bold=True)


	def run(self):
		"""The mainloop"""
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
		pretime = 0
		while True:
			milliseconds = self.clock.tick(self.fps)
			pretime += milliseconds / 1000.0
#			if pretime < 0.01:  #Instructions
			self.draw_text("Preparation stage: Instrunctions")
			self.draw_text("Inhale:7s Retain:7s Exhale:5sec",(100,255,100),dh = -self.width // 10)
			self.draw_text("Do it until the sound stops",(100,255,100),dh = -self.width // 6)
			self.draw_text("Close your eyes",(100,255,100),dh = -self.width // 4)
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			
			y = self.getDataO(5)
			w = csv.writer(open("Preparacion.csv", "w"))
			for key, val in y.items():
				w.writerow([key, val])

#			elif pretime < 1: # should be 52
				# credits to http://www.bensound.com/			
			pygame.mixer.music.load('bensound-relaxing.mp3')
			pygame.mixer.music.play(0)
			self.draw_text("Relax")
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			self.screen.blit(self.background, (0, 0))
			del w,y
			y = self.getDataO(5)
			w = csv.writer(open("Relajacion.csv", "w"))
			for key, val in y.items():
				w.writerow([key, val])

#			elif pretime < 1: # should be 57
			pygame.mixer.music.stop()
			self.draw_text("Concentrese en el punto")
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			self.screen.blit(self.background, (0, 0))
			del w,y
			y = self.getDataO(2)
			w = csv.writer(open("PreConcentracion.csv", "w"))
			for key, val in y.items():
				w.writerow([key, val])

#			else: # should be 107
			pygame.draw.circle(self.screen, (255,255,255), (400,300), 5, 0)
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))		
			y = self.getDataO(5)
			w = csv.writer(open("PreConcentracion.csv", "w"))
			for key, val in y.items():
				w.writerow([key, val])
			break
#			print pretime
		



	def getDataO(self, tm):
		fs = 128.0     #Frecuencia de muestreo
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
		ldic = dt
		dicx = ldic[0].copy()
		for key,value in dicx.iteritems():
			dicx[key] = []

		for i in ldic:
			for key, value in i.iteritems():
				value = i[key][0]
				quality = i[key][1]
				dicx[key].append((quality,value))
				pass
		return dicx

if __name__ == '__main__':
	game(800,600).run()

#print y