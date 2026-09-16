# Mapas y Transición por Bordes
#==============================
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
jugador_tamaño = 40
jugador_x = ancho_pantalla//2 - jugador_tamaño//2
jugador_y = alto_pantalla//2 - jugador_tamaño//2
jugador_velocidad = 6
jugador_color = (0, 200, 100)
# --- CONFIGURACIÓN DE LAS SALAS ---
sala_x = 0
sala_y = 0

salas_colores = {
    (0,0):(30,30,30),
    (1,0):(50,20,20),
    (-1,0):(20,50,20),
    (0,1):(20,20,50),
    (0,-1):(50,50,20),
}

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
    # --- TRANSICIÓN DE LAS SALAS ---
    if jugador_x > ancho_pantalla:
        sala_x += 1
        jugador_x = 0

    elif jugador_x < -jugador_tamaño:
        sala_x -= 1
        jugador_x = ancho_pantalla - jugador_tamaño

    if jugador_y > alto_pantalla:
        sala_y += 1
        jugador_y = 0

    elif jugador_y < -jugador_tamaño:
        sala_y -= 1
        jugador_y = alto_pantalla - jugador_tamaño

    fondo_color = salas_colores.get((sala_x,sala_y),(10,10,10)) 
    # --- DIBUJADO DEL FONDO ---
    pantalla.fill(fondo_color)
    # --- DIBUJADO DEL PERSONAJE ---
    pygame.draw.rect(pantalla,jugador_color,(jugador_x,jugador_y,jugador_tamaño,jugador_tamaño))
    # --- ACTUALIZACIÓN DE LA PANTALLA ---
    pygame.display.flip()

    reloj.tick(FPS)

pygame.quit()

sys.exit()