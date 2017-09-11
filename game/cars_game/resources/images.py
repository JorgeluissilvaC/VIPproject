import os
import pygame

car_img_pth = "resources/images/car"
car_files = sorted(os.listdir(car_img_pth))
bg_img_pth = "resources/images/background"
bg_files = sorted(os.listdir(bg_img_pth))

car = {}
bg = {}


for i in bg_files:
	idx = i.split(".")
	
	bg[idx[0]] = pygame.image.load(os.path.join(bg_img_pth, bg_files[0]))

for i in car_files:
	idx = i.split(".")

	car[idx[0]] = pygame.image.load(os.path.join(car_img_pth, car_files[0]))