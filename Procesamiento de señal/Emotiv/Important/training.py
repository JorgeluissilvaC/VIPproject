# -*- coding: utf-8 -*-
import pygame 
from emokit.emotiv import Emotiv
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time 
import json

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

#			Instructions
			self.draw_text("Preparation stage: Instrunctions")
			self.draw_text("Inhale:7s Retain:7 Exhale:7ec",(100,255,100),dh = -self.width // 10)
			self.draw_text("Do it until the sound stops",(100,255,100),dh = -self.width // 6)
			self.draw_text("Close your eyes",(100,255,100),dh = -self.width // 4)
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))	
			y = self.getDataO(2)
#			Credits to Mike Koenig
			pygame.mixer.music.load('drop.mp3')
			pygame.mixer.music.play(0)
			with open('relajacion1.json', 'w') as fp:
			    json.dump(y, fp)

			self.draw_text("Concentrese en el punto")
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			time.sleep(2)
			pygame.draw.circle(self.screen, (255,255,255), (400,300), 5, 0)
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			del y		
			y = self.getDataO(5)
			with open('concentration.json', 'w') as fp:
			    json.dump(y, fp)

			self.draw_text("Relax")
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			del y
			y = self.getDataO(5)
			with open('Relajacion2.json', 'w') as fp:
			    json.dump(y, fp)

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
