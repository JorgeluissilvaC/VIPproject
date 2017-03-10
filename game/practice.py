# -*- coding: utf-8 -*-
import pygame

class game(object):

	def __init__ (self, width=800, height=600, fps=30):
		"""Initialize pygame, window, background, font,..."""
		pygame.init()
		pygame.display.set_caption("VIP: BCI")
		self.width = width
		self.height = height
		self.dimensions = (self.width, self.height)
		self.screen = pygame.display.set_mode(self.dimensions, pygame.FULLSCREEN)
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
			milliseconds = self.clock.tick(self.fps)
			self.playtime += milliseconds / 1000.0
			self.draw_text("BCI")
			pygame.draw.circle(self.screen, (255,255,255), (300, 50), 5, 0)
			pygame.display.flip()
			self.screen.blit(self.background, (0, 0))
		pygame.quit()


	def draw_text(self, text, color = (0, 255, 150), dw = 0, dh = 0):
		"""Center text in window"""
		fw, fh = self.font.size(text) # fw: font width,  fh: font height
		surface = self.font.render(text, True, color)
		# // makes integer division in python3
		self.screen.blit(surface, ((self.width - fw - dw) // 2, (self.height - dh) // 2))

if __name__ == '__main__':

	# call with width of window and fps
	game(400,300).run()