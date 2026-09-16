# El Jugador y Movimiento Top-Down
#=================================
import pygame
import sys

pygame.init()
# --- CONFIGURACIÓN DE LA PANTALLA ---
ancho_pantalla = 1280
alto_pantalla = 720
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("Mi Juego de Aventura")

reloj = pygame.time.Clock()
FPS = 60
# --- CONFIGURACIÓN DEL JUGADOR ---
jugador_x = ancho_pantalla//2
jugador_y = alto_pantalla//2
jugador_tamaño = 40
jugador_velocidad = 5
jugador_color = (0, 200, 100)     

encendido = True
# --- GAME LOOP ---
while encendido:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            encendido = False
    # --- DETECCIÓN DE BOTONES ---
    teclas = pygame.key.get_pressed()
    # --- MOVIMIENTO DEL PERSONAJE ---
    if teclas[pygame.K_LEFT]:
        jugador_x -= jugador_velocidad
    if teclas[pygame.K_RIGHT]:
        jugador_x += jugador_velocidad
    if teclas[pygame.K_UP]:
        jugador_y -= jugador_velocidad
    if teclas[pygame.K_DOWN]:
        jugador_y += jugador_velocidad
    # --- DIBUJADO DE FONDO ---
    pantalla.fill((30,30,30))
    # --- DIBUJADO DEL PERSONAJE ---
    pygame.draw.rect(pantalla,jugador_color,(jugador_x,jugador_y,jugador_tamaño,jugador_tamaño))
    # --- ACTUALIZACIÓN DE LA PANTALLA ---
    pygame.display.flip()

    reloj.tick(FPS)

pygame.quit()

sys.exit()