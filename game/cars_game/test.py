# -*- coding: utf-8 -*-
import pygame
import threading
import resources.images as imgs
from starstimcon.conection import Ssc
import numpy as np
import os

# Colors
Green   = (0, 255, 150)
Yellow = (255,200,0)

class App(object):
	def __init__ (self,ID="unknown", width=800, height=600, fps=60):
		"""Initialize pygame, window, background, font,..."""
		pygame.init()
		pygame.display.set_caption("VIP: BCI@GAME")
		self.width = width
		self.height = height
		self.dimensions = (self.width, self.height)
		self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
		#self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('mono', 40, bold=False)
		self.fps = fps
		self.playtime = 0.0
		self.opt = 0
		self.threads = list()
		self.x = list()
		

	def saveData(self, result):
		self.x.append(result)

	def run(self):
		gameover = False
		x = (self.width/2)-50
		y = (self.height/2)-50
		#----------------------------------------------------------------------
		self.screen.blit(self.background, (0, 0))
		self.draw_text("BCI:GAME",dh = 200)
		self.draw_text("Training",color = Yellow,fontmod = -10)
		self.draw_text("Play",dh = -100,fontmod = -10)
		pygame.display.flip()


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
			keys = pygame.key.get_pressed()
			if keys[pygame.K_UP]:
				self.draw_text("Training",color = Yellow,fontmod = -10)
				self.draw_text("Play",dh = -100,fontmod = -10)
				self.opt = 0
			if keys[pygame.K_DOWN]:
				self.draw_text("Training",fontmod = -10)
				self.draw_text("Play",color = Yellow,dh = -100,fontmod = -10)
				self.opt = 1
			if keys[pygame.K_SPACE]:
				if (self.opt == 1):
					self.game()
					self.background.fill((0,0,0))
					self.screen.blit(self.background, (0,0))
					self.draw_text("BCI:GAME",dh = 200)
					self.draw_text("Training",fontmod = -10)
					self.draw_text("Play",color = Yellow,dh = -100,fontmod = -10)
				else:
					self.training(2)
					self.background.fill((0,0,0))
					self.screen.blit(self.background, (0,0))
					self.draw_text("BCI:GAME",dh = 200)
					self.draw_text("Training",fontmod = -10)
					self.draw_text("Play",color = Yellow,dh = -100,fontmod = -10)
			#------------------------------------------------------------------
			pygame.display.update()
			milliseconds = self.clock.tick(self.fps)
			self.playtime += milliseconds / 1000.0
		pygame.quit()

	def training(self,n):
		starttime = self.playtime
		#----------------------------------------------------------------------
		bg = imgs.bg["green"]
		bg_y = -bg.get_height()/2
		self.screen.blit(bg, (0, bg_y))
		pygame.display.flip()
		player_car = Car(imgs.car["blue"])
		arrow_l = Sign(imgs.sign["arrow_l"],self.width,self.height)
		arrow_l.moveLeftPosition()
		arrow_r = Sign(imgs.sign["arrow_r"],self.width,self.height)
		arrow_r.moveRightPosition()
		player_car.rect.x = (self.width/2) - 15
		player_car.rect.y = (self.height/2) + 175
		show_left_sign = False
		show_right_sign = False
		con = Ssc(self)
		get_data_t = threading.Thread(target=con.getData, args=(5,))
		#------------------Main Loop-------------------------------------------
		count = 0
		while (count < n):
			finish = False
			while not finish:
				for evento in pygame.event.get():
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_ESCAPE:
							print("ESC pressed")
							finish = True

				if(self.playtime - starttime > 1 and self.playtime - starttime < 2 ):
					show_right_sign = False
					show_left_sign = True
					self.screen.blit(self.background,player_car.rect,player_car.rect) # Erase car from the screen.
					self.screen.blit(self.background,arrow_l.rect,arrow_l.rect) # Erase sign from the screen.
					player_car.moveLeft(3)
				if (self.playtime - starttime > 2 and self.playtime - starttime < 3 ):
					show_right_sign = False
					show_left_sign = False
					self.screen.blit(self.background,player_car.rect,player_car.rect) 
					self.screen.blit(self.background,arrow_r.rect,arrow_r.rect) 
					player_car.moveRight(3)
				elif(self.playtime - starttime > 3 and self.playtime - starttime < 8 ):
					show_right_sign = False
					show_left_sign = False
					self.screen.blit(self.background,arrow_r.rect,arrow_r.rect)
					self.screen.blit(self.background,player_car.rect,player_car.rect)
					#Aquí metes izquierda
					get_data_t.start()
				elif(self.playtime - starttime > 8 and self.playtime - starttime < 9 ):
					show_right_sign = True
					show_left_sign = False
					self.screen.blit(self.background,player_car.rect,player_car.rect)
					self.screen.blit(self.background,arrow_r.rect,arrow_r.rect)
					player_car.moveRight(3)
				elif(self.playtime - starttime > 9 and self.playtime - starttime < 10 ):
					show_right_sign = False
					show_left_sign = False
					self.screen.blit(self.background,player_car.rect,player_car.rect)
					self.screen.blit(self.background,arrow_l.rect,arrow_l.rect)
					player_car.moveLeft(3)

				elif(self.playtime - starttime > 10 and self.playtime - starttime < 15 ):
					show_right_sign = False
					show_left_sign = False
					self.screen.blit(self.background,arrow_r.rect,arrow_r.rect)
					self.screen.blit(self.background,player_car.rect,player_car.rect)
					#Aquí metes Derecha
				elif(self.playtime - starttime >= 15):
					show_right_sign = False
					show_left_sign = False
					starttime = self.playtime
					count += 1
					finish = True
				else:
					show_right_sign = False
					if (self.playtime - starttime > 0.5 and self.playtime - starttime < 1 ):
						show_left_sign = True
					self.screen.blit(self.background,arrow_l.rect,arrow_l.rect)
					self.screen.blit(self.background,player_car.rect,player_car.rect)
				#------------------------------------------------------------------
				if bg_y == 0:
					bg_y = -bg.get_height()/2
				else:
					bg_y += 1
				self.screen.blit(bg, (0, bg_y))
				if show_left_sign == True:
					self.screen.blit(arrow_l.surface,arrow_l.rect)
				elif show_right_sign == True:
					self.screen.blit(arrow_r.surface,arrow_r.rect)
				self.screen.blit(player_car.surface,player_car.rect)
				self.screen.blit(player_car.surface,player_car.rect)
				pygame.display.update()
				milliseconds = self.clock.tick(self.fps)
				self.playtime += milliseconds / 1000.0

	def game(self):
		gameover = False
		#----------------------------------------------------------------------
		bg = imgs.bg["green"]
		bg_y = -bg.get_height()/2
		self.screen.blit(bg, (0, bg_y))
		pygame.display.flip()
		player_car = Car(imgs.car["blue"])
		player_car.rect.x = (self.width/2) - 15
		player_car.rect.y = (self.height/2) + 175
		#------------------Main Loop-------------------------------------------
		while not gameover:
			for evento in pygame.event.get():
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_ESCAPE:
						print("ESC pressed")
						gameover = True
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				self.screen.blit(self.background,player_car.rect,player_car.rect) # Erase car from the screen.
				player_car.moveLeft()
			if keys[pygame.K_RIGHT]:
				self.screen.blit(self.background,player_car.rect,player_car.rect) # Erase car from the screen.
				player_car.moveRight()

			#------------------------------------------------------------------
			if bg_y == 0:
				bg_y = -bg.get_height()/2
			else:
				bg_y += 1
			self.screen.blit(bg, (0, bg_y))
			self.screen.blit(player_car.surface,player_car.rect)
			self.screen.blit(player_car.surface,player_car.rect)
			pygame.display.update()
			milliseconds = self.clock.tick(self.fps)
			self.playtime += milliseconds / 1000.0

	def draw_text(self, text, color = Green, dw = 0, dh = 0,fontmod = 0):
		if fontmod != 0:
			self.font = pygame.font.SysFont('mono', 40+fontmod, bold=False)
		fw, fh = self.font.size(text) # fw: font width,  fh: font height
		surface = self.font.render(text, True, color)
		# // makes integer division in python3
		self.font = pygame.font.SysFont('mono', 40, bold=True)
		self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))
class Car(pygame.sprite.Sprite):
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.surface = image.convert()
		self.surface.set_colorkey((255,255,255))
		self.image = image
		self.rect = self.image.get_rect()
	def moveLeft(self,d = 2):
		self.rect.x -= d
	def moveRight(self,d = 2):
		self.rect.x += d

class Sign(pygame.sprite.Sprite):
	def __init__(self, image, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.surface = image.convert()
		self.surface.set_colorkey((255,255,255))
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = width/2-self.rect.w/2
		self.rect.y = height/2-self.rect.h/2
		self.master_w = width
		self.master_h = height
	def moveLeftPosition(self):
		self.rect.x = self.master_w/2-self.rect.w/2 - 2 * self.rect.w
	def moveRightPosition(self):
		self.rect.x = self.master_w/2-self.rect.w/2 + 2 * self.rect.w
	def moveCentralPosition(self):
		self.rect.x = self.master_w/2-self.rect.w/2

if __name__ == '__main__':
	App().run()