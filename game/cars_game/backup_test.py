# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:16:35 2017

@author: User
"""

# -*- coding: utf-8 -*-
import pygame
import threading
import resources.images as imgs
import processing.eeg as pss
from pylsl import StreamInlet, resolve_stream
from scipy import signal
import numpy as np
import scipy.io as sio
from collections import deque
from sklearn import preprocessing
from sklearn import svm

# Colors
Green   = (0, 255, 150)
Yellow = (255,200,0)

class App(object):
	def __init__ (self,ID="unknown", n_trials = 2, t_act = 5, width=800, height=600, fps=60):
		"""Initialize pygame, window, background, font,..."""
		pygame.init()
		pygame.display.set_caption("VIP: BCI@GAME")
		self.ID = ID
		self.width = width
		self.n_trials = n_trials
		self.height = height
		self.dimensions = (self.width, self.height)
		#self.screen = pygame.display.set_mode(self.dimensions, pygame.DOUBLEBUF)
		self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
		self.background = pygame.Surface(self.screen.get_size()).convert()
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('mono', 40, bold=False)
		self.fps = fps
		self.playtime = 0.0
		self.opt = 0
		self.threads = list()
		self.data_from_ss = np.zeros((2500,8))
		self.lock = True
		self.t_act = t_act #seconds save data
		self.datal = np.zeros((self.n_trials,self.t_act*500,8)); #left training data
		self.datar = np.zeros((self.n_trials,self.t_act*500,8)); #Right training data
		self.beep = pygame.mixer.Sound('resources/sounds/beep.wav')
		self.databuffer = deque([], 500)

	def run(self):
		gameover = False
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
					self.training(self.n_trials)
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
		initial_x = (self.width/2) - 15
		player_car.rect.x = initial_x-1
		player_car.rect.y = (self.height/2) + 175
		show_left_sign = False
		show_right_sign = False

		#------------------Main Loop-------------------------------------------
		count = 0
		amount_count = 0
		cont = 0
		direction = "left"
		self.lock = True
		while (count < n):
			finish = False
			sonido = True
			while not finish:
				for evento in pygame.event.get():
					if evento.type == pygame.KEYDOWN:
						if evento.key == pygame.K_ESCAPE:
							print("ESC pressed")
							finish = True

				if self.lock and count < n:
					if (self.playtime - starttime > 1):
						if (direction == "left" and (player_car.rect.x > initial_x-(self.width/4)/2) and (player_car.rect.x < initial_x)):
							show_right_sign = False
							show_left_sign = True
							if cont == amount_count:
								player_car.moveLeft()
								self.screen.blit(self.background,player_car.rect,player_car.rect)
								self.screen.blit(self.background,arrow_l.rect,arrow_l.rect)
								cont = 0
							else:
								cont += 1
							if sonido == True:
								self.beep.play()
								sonido = False
						elif(direction == "left" and (player_car.rect.x == initial_x-(self.width/4)/2)):
							direction = "right"
						elif(direction == "right" and (player_car.rect.x < initial_x)):
							show_right_sign = False
							show_left_sign = False
							if cont == amount_count:
								player_car.moveRight()
								self.screen.blit(self.background,player_car.rect,player_car.rect)
								cont = 0
							else:
								cont += 1
						elif(direction == "right" and (player_car.rect.x == initial_x)):
							if self.lock == True: # Thread left
								get_data_t = threading.Thread(target= self.getData, args=(5,"left",count))
								get_data_t.start()
								self.lock = False
								player_car.moveRight()
								self.screen.blit(self.background,player_car.rect,player_car.rect)
						elif(direction == "right" and (player_car.rect.x < initial_x+(self.width/4)/2) and (player_car.rect.x > initial_x)):
							show_right_sign = True
							show_left_sign = False
							if cont == amount_count:
								player_car.moveRight()
								self.screen.blit(self.background,player_car.rect,player_car.rect)
								self.screen.blit(self.background,arrow_r.rect,arrow_r.rect)
								cont = 0
							else:
								cont += 1
							#sonido = True
							if sonido == False:
								self.beep.play()
								sonido = True
						elif(direction == "right" and (player_car.rect.x == initial_x+(self.width/4)/2)):
							direction = "left"
						elif(direction == "left" and (player_car.rect.x > initial_x)):
							show_right_sign = False
							show_left_sign = False
							if cont == amount_count:
								player_car.moveLeft()
								self.screen.blit(self.background,player_car.rect,player_car.rect)
								cont = 0
							else:
								cont += 1
						elif(direction == "left" and (player_car.rect.x == initial_x)):
							if self.lock == True: # Thread right
								get_data_t = threading.Thread(target= self.getData, args=(5,"right",count))
								get_data_t.start()
								self.lock = False
								player_car.moveLeft()
								self.screen.blit(self.background,player_car.rect,player_car.rect)
								if (count < n-1):
									count += 1
									finish = True
								else:
									count += 1
				elif self.lock:
					finish = True
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
		print("Training finished for " +self.ID+", "+str(self.n_trials)+" trials done.")
		self.saveData(self.ID, self.datal,self.datar)

	def game(self):
		training_data, Labels = pss.getDataExt(self.ID)
		feats_old= self.processing(training_data)
		scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
		X_train_minmax = scaler.fit_transform(feats_old)
		clf = svm.SVC(kernel='linear', C=1)
		#Se entrena el clasificador con las mejores características
		clf.fit(X_train_minmax, Labels)
		print "entrenado"
		gameover = False
		#----------------------------------------------------------------------
		bg = imgs.bg["green"]
		bg_y = -bg.get_height()/2
		self.screen.blit(bg, (0, bg_y))
		pygame.display.flip()
		player_car = Car(imgs.car["blue"])
		player_car.rect.x = (self.width/2) - 15
		player_car.rect.y = (self.height/2) + 175
		auto_update_buffer_t = threading.Thread(target= self.AutoupdateBuffer, args=())
		print "auto"
		auto_update_buffer_t.start()
		print "start"
		#------------------Main Loop-------------------------------------------
		while not gameover:
			for evento in pygame.event.get():
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_ESCAPE:
						print("ESC pressed")
						gameover = True

			if len(self.databuffer) == 500:
					print "array"
					eeg_data = np.array(self.databuffer)
					eeg_data = np.transpose(eeg_data,(1,0))
					print "eeg data"
					feats = self.processing(eeg_data)
					X_test_min = scaler.transform(feats)
					cls=clf.predict(X_test_min)
					if cls == 2:
						self.screen.blit(self.background,player_car.rect,player_car.rect) 
						# Erase car from the screen.
						player_car.moveLeft()
					if cls == 1:
						self.screen.blit(self.background,player_car.rect,player_car.rect) 
						# Erase car from the screen.
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

	def getData(self, tm, direction, n):
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
		data_time = np.zeros((N,8))
		while c < N:
			sample, timestamp = inlet.pull_sample()
			muestras.append(sample)
			c += 1
		# Array con los datos de los electrodos
		data_time = np.array(muestras)
		if direction == "left":
				self.datal[n] = data_time
				print("left data, trial "+str(n) + " saved")
		elif direction == "right":
				self.datar[n] = data_time
				print("right data, trial "+str(n) + " saved")
		self.lock = True

	def AutoupdateBuffer(self):
		stream_name = 'NIC'
		streams = resolve_stream('type', 'EEG')
		try:
			for i in range(len(streams)):

				if streams[i].name() == stream_name:
					index = i
					print ("NIC stream available")
			print ("Connecting to NIC stream... \n")
			inlet = StreamInlet(streams[index])

		except NameError:
			print ("Error: NIC stream not available\n\n\n")
		while True:
			sample, timestamp = inlet.pull_sample()
			self.databuffer.append(sample)
	
	def saveData(self,name,d1,d2,tipo = 2):
		if tipo==1:
			datac = np.transpose(d1,(1,2,0))
			datar = np.transpose(d2,(1,2,0))
			sio.savemat(name+'.mat',{'conc':datac, 'rel':datar})
		elif tipo == 2:
			dataLI= np.transpose(d1,(1,2,0))
			dataRI= np.transpose(d2,(1,2,0))
			sio.savemat(name+'.mat',{'izq':dataRI,'der':dataLI})
			
	def processing(self,dataTime):
		print dataTime.shape
		eeg_car = pss.car_data(dataTime)
		print "CAR"
		[D_DC, m_v] = pss.remove_dc(eeg_car)
		print "remove DC"
		Y = pss.butter_filter(D_DC)
		print "DC filter"
		print eeg_car.shape
		SCALE = 1
		FS = 500/SCALE # esto es porque fue submuestreado 
		DIV = 500.0/SCALE
		SUB_SIGNAL = pss.down_sampling(Y, int(SCALE), DIV) # Sub muestreo
		Wsize = round(0.7*FS)
		Wnover = round(0.6*FS)
		Windw = signal.hamming(Wsize)
		SUB_SIGNAL.shape
		F, T, S = signal.spectrogram(SUB_SIGNAL, fs=FS, window=Windw,nperseg=Wsize, noverlap=Wnover)
		#F, T, S = signal.spectrogram(Y, fs=FS, window=Windw,nperseg=Wsize, noverlap=int(Wnover))
		ff = SUB_SIGNAL.shape # Tamaño del array
		dimen = len(ff)
		frang = ((F>=8)*(F<=13))#+((F>=14)*(F<=31))# Solo se debe cambiar el rango ((F>=16)*(F<=31))
		#freq_rang = F[frang]
		print S.shape
		if (dimen == 3):
			Sig_S = S[:,:,frang,:]
			M_F = np.mean(Sig_S, axis=3) # Potencia promedio para cada frecuencia
			FEATS = np.reshape(M_F, (ff[0], M_F.shape[2]*ff[1]))
		elif (dimen == 2):    
			Sig_S = S[:,frang,:]
			M_F = np.mean(Sig_S, axis=2) # Potencia promedio para cada frecuencia
			FEATS = M_F
			FEATS = np.reshape(FEATS, (M_F.shape[0]*M_F.shape[1],1))
			FEATS = FEATS.T
		return FEATS

class Car(pygame.sprite.Sprite):
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.surface = image.convert()
		self.surface.set_colorkey((255,255,255))
		self.image = image
		self.rect = self.image.get_rect()
	def moveLeft(self,d = 1):
		self.rect.x -= d
	def moveRight(self,d = 1):
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
	nombre = raw_input("[!] ID: ")
	n = int(raw_input("[!] Trials: "))
	App(ID = nombre,n_trials = n).run()