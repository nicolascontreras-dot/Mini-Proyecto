# Creando la estructura base (El Game Loop)
#==========================================
import pygame
import sys

pygame.init()
# --- CONFIGURACIÓN PANTALLA ---
ancho_pantalla = 1280
alto_pantalla = 720
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("Mi Juego de Aventura")

reloj = pygame.time.Clock()
FPS = 60

encendido = True
# --- GAME LOOP --- 
while encendido:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            encendido = False
    # --- DIBUJADO DE FONDO ---
    pantalla.fill((30,30,30))
    # --- ACTUALIZACIÓN DE LA PANTALLA ---
    pygame.display.flip()

    reloj.tick(FPS)
# --- CIERRE DEL PROGRAMA ---
pygame.quit()

sys.exit()