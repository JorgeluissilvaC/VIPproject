# -*- coding: utf-8 -*-


import pygame 
from GetData import *

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
		# credits to http://www.bensound.com/
		pygame.mixer.music.load('bensound-relaxing.mp3')
		pygame.mixer.music.play(0)
		while pretime < 5:
			milliseconds = self.clock.tick(self.fps)
			pretime += milliseconds / 1000.0
			self.draw_text("Preparation Stage")
			self.draw_text("Inhale:7s Retain:7s Exhale:7sec",(100,255,100),dh = -self.width // 10)
			self.draw_text("Do it until the sound stops",(100,255,100),dh = -self.width // 6)
			self.draw_text("You will have 50s to concentrate",(100,255,100),dh = -self.width // 2)
			# self.draw_text("Inhale:7s Retain:7s Exhale:7sec",(100,255,100),dh = -self.width // 10)
			# self.draw_text("Do it until the sound stops",(100,255,100),dh = -self.width // 6)
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
			print pretime
		y = GetDataO(5)
		pygame.mixer.music.stop()
####

if __name__ == '__main__':

	game(800,600).run()
#print y