from pathlib import Path
import pygame, sys

pygame.init()

reloj = pygame.time.Clock()
FPS = 60

# Configuración
ancho_pantalla = 1360
alto_pantalla = 820
tamaño_pantalla = (ancho_pantalla, alto_pantalla)

pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Prueba Pygame")

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

fondo_norte = pygame.image.load(CARPETA_IMAGENES/"fondo_norte.png").convert()
fondo_norte = pygame.transform.scale(fondo_norte, tamaño_pantalla)

aventurero_abajo = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo.png").convert_alpha()
aventurero_arriba = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba.png").convert_alpha()
aventurero_izquierda = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda.png").convert_alpha()
aventurero_derecha = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha.png").convert_alpha()

aventurero_abajo = pygame.transform.scale_by(aventurero_abajo, 0.3)
aventurero_arriba = pygame.transform.scale_by(aventurero_arriba, 0.3)
aventurero_izquierda = pygame.transform.scale_by(aventurero_izquierda, 0.3)
aventurero_derecha = pygame.transform.scale_by(aventurero_derecha, 0.3)

sala_x = 0
sala_y = 0

salas_imagenes = {
    (0,0):(30,30,30),
    (1,0):(50,20,20),
    (-1,0):(20,50,20),
    (0,1):fondo_norte,
    (0,-1):(50,50,20),
}

class Jugador(pygame.sprite.Sprite):
    def __init__(self, imagenes, x, y):
        super().__init__()
        self.imagenes = imagenes
        self.image = self.imagenes["abajo"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
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
    
    if jugador.rect.left > ancho_pantalla:
        sala_x += 1
        jugador.rect.right = 0
    elif jugador.rect.right < 0:
        sala_x -= 1
        jugador.rect.left = ancho_pantalla

    if jugador.rect.top > alto_pantalla:
        sala_y += 1
        jugador.rect.bottom = 0
    elif jugador.rect.bottom < 0:
        sala_y -= 1
        jugador.rect.top = alto_pantalla

    fondo_actual = salas_imagenes.get((sala_x,sala_y), (10,10,10)) 

    pantalla.blit(fondo_actual, (0, 0))

    jugadores.draw(pantalla)

    pygame.display.flip()

    reloj.tick(FPS)

pygame.quit()
sys.exit()