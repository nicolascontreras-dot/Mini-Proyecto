#Corazón del juego
#=================
from pathlib import Path
import math
import pygame, sys

pygame.init()
reloj = pygame.time.Clock()                     

#Configuración de la ventana
#===========================
ancho_pantalla = 1360                            
alto_pantalla = 820                            
tamaño_pantalla = (ancho_pantalla,alto_pantalla)
pantalla = pygame.display.set_mode((tamaño_pantalla))
pygame.display.set_caption("Prueba Pygame")

#Sección de fondos
#===================
CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

aventurero_imagen = pygame.image.load(CARPETA_IMAGENES/"Aventurero.jpg").convert_alpha()
aventurero_imagen = pygame.transform.scale_by(aventurero_imagen,0.15)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, nombre, imagen, coordenada_x, coordenada_y, zona):
        super().__init__()
        self.nombre = nombre
        self.zona = zona
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (coordenada_x,coordenada_y)
        self.velocidad = 5
        self.radio = self.rect.width*0.22
        self.desplazamiento_y = 10
        self.tiene_mochila = False
        self.centro_pies = [self.rect.midbottom[0], self.rect.midbottom[1] - self.desplazamiento_y]

    def sincronizar_pies(self):
        self.centro_pies = [self.rect.midbottom[0], self.rect.midbottom[1] - self.desplazamiento_y]   

    def mover(self, teclas):
            if teclas[pygame.K_RIGHT]:
                self.rect.x += self.velocidad
                self.sincronizar_pies()                 
            if teclas[pygame.K_LEFT]:
                self.rect.x -= self.velocidad
                self.sincronizar_pies()
            if teclas[pygame.K_UP]:
                self.rect.y -= self.velocidad
                self.sincronizar_pies() 
            if teclas[pygame.K_DOWN]:
                self.rect.y += self.velocidad
                self.sincronizar_pies()

    @property
    def posicion_y(self):
        return self.rect.bottom

jugador = Jugador("Kano",aventurero_imagen,500,500,"playa")
jugadores = pygame.sprite.Group()
jugadores.add(jugador)

encendido = True

while encendido:                                     
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:
            encendido = False

    teclas = pygame.key.get_pressed()
    
    jugador.mover(teclas)
    
    jugador.sincronizar_pies()
    
    pantalla.fill((0,0,0))
    
    jugadores.draw(pantalla)  
      
    pygame.display.flip()
    reloj.tick(60)
    
pygame.quit()