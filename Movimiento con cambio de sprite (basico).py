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

aventurero_abajo = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo.png").convert_alpha()
aventurero_arriba = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba.png").convert_alpha()
aventurero_izquierda = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda.png").convert_alpha()
aventurero_derecha = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha.png").convert_alpha()

aventurero_abajo = pygame.transform.scale_by(aventurero_abajo, 0.3)
aventurero_arriba = pygame.transform.scale_by(aventurero_arriba, 0.3)
aventurero_izquierda = pygame.transform.scale_by(aventurero_izquierda, 0.3)
aventurero_derecha = pygame.transform.scale_by(aventurero_derecha, 0.3)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, imagenes, coordenada_x, coordenada_y):
        super().__init__()
        self.imagenes = imagenes
        self.image = self.imagenes["abajo"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (coordenada_x, coordenada_y)
        self.velocidad = 5

    def cambiar_imagen(self, nueva_imagen):
        posicion = self.rect.center
        self.image = nueva_imagen
        self.rect = self.image.get_rect()
        self.rect.center = posicion

    def mover(self, teclas):
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.cambiar_imagen(self.imagenes["derecha"])

        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.cambiar_imagen(self.imagenes["izquierda"])

        elif teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
            self.cambiar_imagen(self.imagenes["arriba"])

        elif teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
            self.cambiar_imagen(self.imagenes["abajo"])

imagenes_jugador = {
    "arriba" : aventurero_arriba,
    "abajo" : aventurero_abajo,
    "izquierda" : aventurero_izquierda,
    "derecha" : aventurero_derecha
}

jugador = Jugador(imagenes_jugador, 500, 500)

jugadores = pygame.sprite.Group()
jugadores.add(jugador)

encendido = True

while encendido:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            encendido = False

    teclas = pygame.key.get_pressed()

    jugador.mover(teclas)

    pantalla.fill((0, 0, 0))

    jugadores.draw(pantalla)

    pygame.display.flip()

    reloj.tick(60)


pygame.quit()