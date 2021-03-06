"""
Created on Tue Mar 07 14:06:46 2017
Script para el entramiento con Starstim
"""

# -*- coding: utf-8 -*-
import pygame 
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time 
import json
from pylsl import StreamInlet, resolve_stream

class game(object):

	def __init__ (self, width=800, height=600, fps=30):
		"""Initialize pygame, window, background, font,...


		"""
		pygame.init()
		pygame.display.set_caption("VIP: BCI")
		self.width = width
		self.height = height
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
#		Credits to Mike Koenig - Se carga la cancion 
		pygame.mixer.music.load('drop.mp3')
#		Instructions - Etapa de relajacion 1
		self.draw_text("Preparation stage: Instrunctions")
		self.draw_text("Inhale:7s Retain:7 Exhale:7ec",(100,255,100),dh = -self.width // 10)
		self.draw_text("Do it until the sound stops",(100,255,100),dh = -self.width // 6)
		self.draw_text("Close your eyes",(100,255,100),dh = -self.width // 4)
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))	
#		Se obtienen los datos
		y = self.getDataO(25)
		pygame.mixer.music.play(0)
#		Se guardan los datos
		with open('relajacion1.json', 'w') as fp:
		    json.dump(y, fp)
#		Etapa de concentracion 
		self.draw_text("Concentrese en el punto")
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))
		time.sleep(4)
		pygame.draw.circle(self.screen, (255,255,255), (400,300), 5, 0)
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))

#		Se obtienen los datos
		del y 
		y = self.getDataO(7)
#		Se guardan los datos
		with open('concentration1.json', 'w') as fp:
		    json.dump(y, fp)
#		Etapa de relajacion 
		self.draw_text("Relax")
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))
#		Se obtienen los datos
		del y
		y = self.getDataO(7)
#		Se guardan los datos
		with open('Relajacion2.json', 'w') as fp:
		    json.dump(y, fp)
#		Etapa de concentracion 2
		self.draw_text("Imagine que mueve el cuadrado")
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))
		time.sleep(4)
		pygame.draw.rect(self.screen, (255,255,255), [400, 300, 100, 100],0)
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))

#		Se obtienen los datos
		del y 
		y = self.getDataO(7)
#		Se guardan los datos
		with open('concentration2.json', 'w') as fp:
		    json.dump(y, fp)

	def getDataO(self, tm):
		stream_name = 'NIC'
		streams = resolve_stream('type', 'EEG')
		fs = 500 # Frecuencia de muestreo
		N=fs*tm #Numero de muestras 
		c=0;
		muestras = []
		try:
			for i in range (len(streams)):

				if (streams[i].name() == stream_name):
					index = i
					print ("NIC stream available")

			print ("Connecting to NIC stream... \n")
			inlet = StreamInlet(streams[index])   

		except NameError:
			print ("Error: NIC stream not available\n\n\n")

		while c<N:
		    sample, timestamp = inlet.pull_sample()
		    muestras.append(sample)
		    c+=1
		    
		#Diccionario con los datos de los electrodos
		dic = {} 
		for electrodos in range(0,len(sample)):
		    dic[electrodos+1] = []
		    for muestra in muestras:
		        dic[electrodos+1].append(muestra[electrodos])

		return dic

if __name__ == '__main__':
	game(800,600).run()
