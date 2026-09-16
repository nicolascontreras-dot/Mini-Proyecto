# Migrando nuestro Jugador a una Clase
#=====================================
import pygame
import sys

pygame.init()

ancho_pantalla = 1280
alto_pantalla = 720
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("Mi Juego de Aventura")

reloj = pygame.time.Clock()
FPS = 60

class Jugador:
    def __init__(self, x, y):
        self.tamaño = 40
        self.rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        self.velocidad = 6
        self.color = (0, 200, 100)
    
    def mover(self, teclas):       
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)

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
while encendido:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            encendido = False

    teclas = pygame.key.get_pressed()

    jugador.mover(teclas)

    if jugador.rect.x > ancho_pantalla: 
        sala_x += 1
        jugador.rect.x = 0

    elif jugador.rect.x < -jugador.tamaño:
        sala_x -= 1
        jugador.rect.x = ancho_pantalla - jugador.tamaño

    if jugador.rect.y > alto_pantalla:
        sala_y += 1
        jugador.rect.y = 0

    elif jugador.rect.y < -jugador.tamaño:
        sala_y -= 1
        jugador.rect.y = alto_pantalla - jugador.tamaño
    
    fondo_color = salas_colores.get((sala_x,sala_y),(10,10,10)) 

    pantalla.fill(fondo_color)
    
    jugador.dibujar(pantalla)
    
    pygame.display.flip()

    reloj.tick(FPS)

pygame.quit()

sys.exit()