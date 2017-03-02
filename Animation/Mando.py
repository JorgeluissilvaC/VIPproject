import pygame
from math import * # Trigonometria 
# Definimos algunos colores
NEGRO   = (0, 0 ,0)
BLANCO  = (255, 255, 255)
VERDE   = (0, 255, 0)
ROJO    = (255, 0, 0)
AZUL    = (0, 0, 255)
VIOLETA = (98, 0, 255)
# Definimos algunas constantes 
PI = 3.14159265359
x=325
y=225
r=5
# Definimos algunas variables
t = 0
pygame.init()
# Establecemos las dimensiones de la pantalla [largo,altura]
dimensiones = [700,500]
pantalla = pygame.display.set_mode(dimensiones) 
pygame.display.set_caption("Starstim Game")
#El bucle se ejecuta hasta que el usuario hace click sobre el botón de cierre.
hecho = False
# Se usa para establecer cuan rápido se actualiza la pantalla
 
reloj = pygame.time.Clock()
 
# -------- Bucle principal del Programa -----------
while not hecho:
    # --- Bucle principal de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: 
            print("Se precionó el boton cerrar")
            hecho = True
            
        if evento.type == pygame.KEYDOWN:
        # Resuelve que ha sido una tecla de flecha, por lo que
        # ajusta la velocidad.
            if evento.key == pygame.K_UP:
                y=y-r
                pygame.draw.rect(pantalla, ROJO, [x, y, 50, 50])
            if evento.key == pygame.K_DOWN:
                y=y+r
                pygame.draw.rect(pantalla, ROJO, [x, y, 50, 50])
            if evento.key == pygame.K_LEFT:
                x=x-r
                pygame.draw.rect(pantalla, ROJO, [x, y, 50, 50])
            if evento.key == pygame.K_RIGHT:
                x=x+r
                pygame.draw.rect(pantalla, ROJO, [x, y, 50, 50])
    # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ
  
    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ
    
    # Primero, limpia la pantalla con blanco. No vayas a poner otros comandos de dibujo encima 
    # de esto, de otra forma serán borrados por este comando:
    pantalla.fill(BLANCO)
    pygame.draw.rect(pantalla, ROJO, [x,y, 50, 50])
    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
 
    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    reloj.tick(60)
     
# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()