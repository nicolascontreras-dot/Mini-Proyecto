from pathlib import Path
import pygame, sys
pygame.init()
reloj = pygame.time.Clock()

#CONFIGURACIÓN PANTALLA
ancho_pantalla=700
alto_pantalla=400
tamaño_pantalla = (ancho_pantalla,alto_pantalla) 
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Prueba pygame") 

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

# SECCIÓN IMAGENES
pantalla_bosque = pygame.image.load(CARPETA_IMAGENES/"darkforest.jpg")
pantalla_bosque = pygame.transform.scale(pantalla_bosque,tamaño_pantalla)

pantalla_refugio = pygame.image.load(CARPETA_IMAGENES/"carpa.png")
pantalla_refugio = pygame.transform.scale(pantalla_refugio,tamaño_pantalla)

zombie_imagen = pygame.image.load(CARPETA_IMAGENES/"zombie.png")
zombie_imagen = pygame.transform.scale(zombie_imagen,(80,140)) 

jugador_imagen = pygame.image.load(CARPETA_IMAGENES/"player3.png")
jugador_imagen = pygame.transform.scale(jugador_imagen,(50,95))

colisiones_bosque=[]

arboles_rect = pygame.Rect(0,0,700,135)
suelo_rect = pygame.Rect(0,380,700,380)

colisiones_bosque.append(arboles_rect)
colisiones_bosque.append(suelo_rect)

fuente = pygame.font.Font(None,150)
texto_bosque = fuente.render("bosque",False,(255,255,255))
texto_refugio = fuente.render("refugio",False,(255,255,255))

class Jugador(pygame.sprite.Sprite):
    
    def __init__(self, imagen,x,y):
        super().__init__()
        self.image=imagen
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.velocidad=5
        
    def mover(self,teclas,colisiones):
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            for colision in colisiones:
                if self.rect.colliderect(colision):
                    self.rect.x-=self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.x-=self.velocidad
        if teclas[pygame.K_LEFT]:
            self.rect.x-=self.velocidad
            for colision in colisiones:
                if self.rect.colliderect(colision):
                    self.rect.x+=self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.x+=self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y-=self.velocidad
            for colision in colisiones:
                if self.rect.colliderect(colision):
                    self.rect.y+=self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.y+=self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y+=self.velocidad
            for colision in colisiones:
                if self.rect.colliderect(colision):
                    self.rect.y-=self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.y-=self.velocidad
                    
class Zombie(pygame.sprite.Sprite):
    def __init__(self, imagen,x,y,zona):
        super().__init__()
        self.image=imagen
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.velocidad=2
        self.zona = zona
        
    def perseguir(self,jugador,colisiones):
        if teclas[pygame.K_RIGHT]:
            if self.rect.x<jugador.rect.x:
                self.rect.x += self.velocidad
                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.x -= self.velocidad
        if teclas[pygame.K_LEFT]:
            if self.rect.x>jugador.rect.x:
                self.rect.x -= self.velocidad
                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            if self.rect.y>jugador.rect.y:
                self.rect.y -= self.velocidad
                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.y += self.velocidad
        if teclas[pygame.K_DOWN]:
            if self.rect.y<jugador.rect.y:
                self.rect.y += self.velocidad
                for colision in colisiones:
                    if self.rect.colliderect(colision):
                        self.rect.y -= self.velocidad  

jugador = Jugador(jugador_imagen,200,200)
enemigo = Zombie(zombie_imagen,50,200,"darkforest")

jugadores = pygame.sprite.Group()
jugadores.add(jugador)

enemigos = pygame.sprite.Group()
enemigos.add(enemigo)

zona_actual = "darkforest"
obstaculos_actuales = colisiones_bosque

#MOTOR DEL JUEGO
ejecutando = True
while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
            
    teclas=pygame.key.get_pressed()  
    
    if zona_actual == "darkforest":
        pantalla_actual = pantalla_bosque
        texto_actual = texto_bosque
        obstaculos_actuales = colisiones_bosque

    elif zona_actual == "refugio":
        pantalla_actual = pantalla_refugio
        texto_actual = texto_refugio
    
        
    jugador.mover(teclas,obstaculos_actuales)
    
    if zona_actual == "darkforest":
        if jugador.rect.right >= ancho_pantalla:          
            zona_actual = "refugio"             
            jugador.rect.left = 0     
            
    pantalla.blit(pantalla_actual,(0,0))
    pantalla.blit(texto_actual,(0,0))
 
    if zona_actual == "darkforest":
        enemigo.perseguir(jugador,obstaculos_actuales)
        enemigos.draw(pantalla)
    
    jugadores.draw(pantalla)

    pygame.display.flip()
    reloj.tick(60)
pygame.quit()