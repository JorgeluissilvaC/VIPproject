import os
import pygame

car_img_pth = "resources/images/car"
car_files = sorted(os.listdir(car_img_pth))
bg_img_pth = "resources/images/background"
bg_files = sorted(os.listdir(bg_img_pth))
s_img_pth = "resources/images/sign"
s_files = sorted(os.listdir(s_img_pth))

car = {}
bg = {}
sign = {}

for i in bg_files:
	idx = i.split(".")
	
	bg[idx[0]] = pygame.image.load(os.path.join(bg_img_pth, i))

for i in car_files:
	idx = i.split(".")

	car[idx[0]] = pygame.image.load(os.path.join(car_img_pth, i))

for i in s_files:
	idx = i.split(".")
	
	sign[idx[0]] = pygame.image.load(os.path.join(s_img_pth, i))