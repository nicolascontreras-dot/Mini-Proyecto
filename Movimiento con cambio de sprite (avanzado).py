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
aventurero_abajo_1 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo_1.png").convert_alpha()
aventurero_abajo_2 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo_2.png").convert_alpha()
aventurero_abajo_3 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo_3.png").convert_alpha()
aventurero_abajo_4 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_abajo_4.png").convert_alpha()

imagenes_abajo = [
    aventurero_abajo,
    aventurero_abajo_1,
    aventurero_abajo_2,
    aventurero_abajo_3,
    aventurero_abajo_4
]

aventurero_arriba = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba.png").convert_alpha()
aventurero_arriba_1 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba_1.png").convert_alpha()
aventurero_arriba_2 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba_2.png").convert_alpha()
aventurero_arriba_3 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba_3.png").convert_alpha()
aventurero_arriba_4 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_arriba_4.png").convert_alpha()

imagenes_arriba = [
    aventurero_arriba,
    aventurero_arriba_1,
    aventurero_arriba_2,
    aventurero_arriba_3,
    aventurero_arriba_4
]

aventurero_izquierda = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda.png").convert_alpha()
aventurero_izquierda_1 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda_1.png").convert_alpha()
aventurero_izquierda_2 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda_2.png").convert_alpha()
aventurero_izquierda_3 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda_3.png").convert_alpha()
aventurero_izquierda_4 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_izquierda_4.png").convert_alpha()

imagenes_izquierda = [
    aventurero_izquierda,
    aventurero_izquierda_1,
    aventurero_izquierda_2,
    aventurero_izquierda_3,
    aventurero_izquierda_4
]

aventurero_derecha = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha.png").convert_alpha()
aventurero_derecha_1 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha_1.png").convert_alpha()
aventurero_derecha_2 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha_2.png").convert_alpha()
aventurero_derecha_3 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha_3.png").convert_alpha()
aventurero_derecha_4 = pygame.image.load(CARPETA_IMAGENES/"Aventurero_derecha_4.png").convert_alpha()

imagenes_derecha = [
    aventurero_derecha,
    aventurero_derecha_1,
    aventurero_derecha_2,
    aventurero_derecha_3,
    aventurero_derecha_4
]

imagenes_abajo = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_abajo]
imagenes_arriba = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_arriba]
imagenes_izquierda = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_izquierda]
imagenes_derecha = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_derecha]

imagenes_jugador = {
    "derecha" : imagenes_derecha,
    "izquierda" : imagenes_izquierda,
    "arriba" : imagenes_arriba,
    "abajo" : imagenes_abajo
}

class Jugador(pygame.sprite.Sprite):
    def __init__(self, imagenes, coordenada_x, coordenada_y):
        super().__init__()
        self.imagenes = imagenes
        self.direccion = "abajo"
        self.frame = 0
        self.contador_animacion = 0
        self.image = self.imagenes[self.direccion][self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (coordenada_x, coordenada_y)
        self.velocidad = 5
    
    def cambiar_direccion(self, nueva_direccion):
        if self.direccion != nueva_direccion:
            
            self.direccion = nueva_direccion
            self.frame = 0
            
    def animar(self):
        self.contador_animacion += 1
        
        if self.contador_animacion >= 10:
            
            self.frame += 1
            self.contador_animacion = 0
            
            if self.frame >= len(self.imagenes[self.direccion]):
                self.frame = 0
        
        self.image = self.imagenes[self.direccion][self.frame]

    def mover(self, teclas):
        
        moviendose = False
        
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.cambiar_direccion("derecha")
            moviendose = True

        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.cambiar_direccion("izquierda")
            moviendose = True
            
        elif teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
            self.cambiar_direccion("arriba")
            moviendose = True
            
        elif teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
            self.cambiar_direccion("abajo")
            moviendose = True
        
        if moviendose:
            self.animar()
        
        else:
            self.frame = 0
            self.image = self.imagenes[self.direccion][self.frame]
        
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