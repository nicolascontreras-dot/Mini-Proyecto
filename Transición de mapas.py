from pathlib import Path
import pygame, sys

pygame.init()
reloj = pygame.time.Clock()

# Configuración
ancho_pantalla = 1360
alto_pantalla = 820
tamaño_pantalla = (ancho_pantalla, alto_pantalla)

pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Prueba Pygame")

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

fondo = pygame.image.load(CARPETA_IMAGENES/"fondo_norte.png")
fondo = pygame.transform.scale_by(fondo,(ancho_pantalla,alto_pantalla))

imagen_aventurero = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo.png").convert_alpha()
imagen_aventurero = pygame.transform.scale_by(imagen_aventurero, 0.3)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, imagen, coordenada_x, coordenada_y):
        super().__init__()
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (coordenada_x, coordenada_y)
        self.velocidad = 5

    def mover(self, teclas):
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad

        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad

        elif teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad

        elif teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad

jugador = Jugador(imagen_aventurero, 500, 500)

jugadores = pygame.sprite.Group()
jugadores.add(jugador)

encendido = True

while encendido:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            encendido = False

    teclas = pygame.key.get_pressed()

    jugador.mover(teclas)

    jugadores.draw()
    
    pygame.display.flip()

    reloj.tick(60)
    
pygame.quit()