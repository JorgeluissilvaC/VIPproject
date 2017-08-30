# -*- coding: utf-8 -*-
import pygame
import os
# Colors
Green   = (0, 255, 150)

class Game(object):

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
		gameover = False
		x = (self.width/2)-50
		y = (self.height/2)-50
		#----------------------------------------------------------------------
		self.draw_text("BCI Game")
		#pygame.draw.rect(self.screen,Green, [x,y, 100, 100])
		pygame.display.flip()
		self.screen.blit(self.background, (0, 0))
		player_car = Car(pygame.image.load(os.path.join('data', 'car_blue.png')))
		player_pos = player_car.rect
		player_pos.x = (self.width/2) - 15
		player_pos.y = (self.height/2) - 25
		#------------------Main Loop-------------------------------------------
		while not gameover:            
			for evento in pygame.event.get():
				if evento.type == pygame.QUIT: 
					print("Close pressed")
					gameover = True
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_ESCAPE:
						print("ESC pressed")
						gameover = True
					if evento.key == pygame.K_LEFT:
						print("LEFT pressed")
						self.screen.blit(self.background,player_pos,player_pos) # Erase the player from the screen.
						player_pos.x -= 2
					if evento.key == pygame.K_RIGHT:
						print("RIGHT pressed")
						self.screen.blit(self.background,player_pos,player_pos)
						player_pos.x += 2
			#------------------------------------------------------------------
			self.screen.blit(player_car.surface,player_pos)
			pygame.display.update()
			milliseconds = self.clock.tick(self.fps)
			self.playtime += milliseconds / 1000.0
		pygame.quit()

	def draw_text(self, text, color = Green, dw = 0, dh = 0):
		fw, fh = self.font.size(text) # fw: font width,  fh: font height
		surface = self.font.render(text, True, color)
		# // makes integer division in python3
		self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))

class Car(pygame.sprite.Sprite):

	def __init__(self, image):
	   pygame.sprite.Sprite.__init__(self)
	   self.surface = image.convert()
	   self.image = image
	   self.rect = self.image.get_rect()

if __name__ == '__main__':
	Game().run()