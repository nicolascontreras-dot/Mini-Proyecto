from pathlib import Path
import pygame
import sys

pygame.init()
reloj = pygame.time.Clock()

#CONFIGURACIÓN PANTALLA
ancho_pantalla=720
alto_pantalla=480
tamaño_pantalla = (ancho_pantalla,alto_pantalla) 
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("juego") 

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

# SECCIÓN IMAGENES
pantalla_sala_de_estar = pygame.image.load(CARPETA_IMAGENES/"saladeestar.png")
pantalla_sala_de_estar = pygame.transform.scale(pantalla_sala_de_estar,tamaño_pantalla)

jugador_imagen = pygame.image.load(CARPETA_IMAGENES/"player3.png")
jugador_imagen = pygame.transform.scale(jugador_imagen,(50,95))

tele_imagen = pygame.image.load(CARPETA_IMAGENES/"tele.png")
tele_imagen = pygame.transform.scale(tele_imagen,(50,95))

zombie_imagen = pygame.image.load(CARPETA_IMAGENES/"zombie.png")
zombie_imagen = pygame.transform.scale(zombie_imagen,(80,140)) 

#COLISIONES SALA DE ESTAR
colisiones_sala_de_estar=[]

arboles_rect = pygame.Rect(0,0,700,135)
tele_rect = pygame.Rect(0,380,700,380)

colisiones_sala_de_estar.append(arboles_rect)
colisiones_sala_de_estar.append(tele_rect)

#SECCIÓN TEXTO
fuente = pygame.font.Font(None,100)
texto_sala_de_estar = fuente.render("sala de estar",False,(255,255,255))

#JUGADOR
class Jugador(pygame.sprite.Sprite):
    
    def __init__(self, imagen,x,y):
        super().__init__()
        self.image=imagen
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.velocidad=5
        
    def mover(self,teclas,colisiones,enemigos):      #Corrección: se agregaron enemigos a los parámetros
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
        
    def perseguir(self,jugador,colisiones,teclas):      #Corrección: se agregaron teclas a los parámetros porque se mueve si el jugador se mueve
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

class Tele(pygame.sprite.Sprite):
    def __init__(self, imagen,x,y,zona):
        super().__init__()
        self.image=imagen
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        #self.velocidad=2           #Corrección: la tele no necesita velocidad
        self.zona = zona
        
    def draw(self, superficie):          #Corrección: se agregó el símbolo : y los parámetros self y superficie
        superficie.blit(self.image, self.rect)
        
jugador = Jugador(jugador_imagen,200,200)
enemigo = Zombie(zombie_imagen,50,200,"saladeestar")

jugadores = pygame.sprite.Group()
jugadores.add(jugador)

enemigos = pygame.sprite.Group()
enemigos.add(enemigo)                  

#pantalla_actual = "saladeestar"
estado_juego = "saladeestar"
#obstaculos_actuales = pantalla_sala_de_estar        #Corrección: Se usaron variables separadas para el estado del juego y la imagen de fondo

ejecutando = True

while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        
        #elif event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_e:
                #Lógica para mostrar el noticiario
                
    teclas=pygame.key.get_pressed()  
    
    if estado_juego == "saladeestar":           #Corrección: se cambio la pantalla por el estado del juego y se modificó su lógica completa
        obstaculos_actuales = colisiones_sala_de_estar
        
        # Mover jugador (pasándole los obstáculos y los enemigos para las colisiones)
        jugador.mover(teclas, obstaculos_actuales, enemigos)
        
        # Mover zombie (pasándole el jugador, obstáculos y las teclas actuales)
        enemigo.perseguir(jugador, obstaculos_actuales, teclas)
        
        # Cambio de zona si el jugador llega al borde derecho de la pantalla
        if jugador.rect.right >= ancho_pantalla:          
            estado_juego = "refugio"           
            jugador.rect.left = 0
      
    #jugador.mover(teclas,obstaculos_actuales)      #Corrección: se movió al jugador en el bloque de la sala de estar
    
    # DIBUJADO EN PANTALLA
    pantalla.fill((0, 0, 0)) # Limpiar pantalla para evitar rastros visuales
    
    if estado_juego == "saladeestar":
        pantalla.blit(pantalla_sala_de_estar, (0, 0))
        pantalla.blit(texto_sala_de_estar, (50, 50)) # Ajustada la posición del texto para que no quede tapado en (0,0)
        enemigos.draw(pantalla)
        
    jugadores.draw(pantalla)
    
    #Corrección: todo lo que definió en la sala de estar por separado, se movió todo junto al bloque de la sala de estar
    #if pantalla_actual == "saladeestar":
    #    if jugador.rect.right >= ancho_pantalla:          
    #        zona_actual = "refugio"             
    #        jugador.rect.left = 0     
            
    #pantalla.blit(pantalla_actual,(0,0))
    #pantalla.blit(texto_actual,(0,0))
 
    #if pantalla_actual == "saladeestar":
        #enemigo.perseguir(jugador,obstaculos_actuales)         #Corrección: se movió al enemigo en el bloque de la sala de estar
    #    enemigos.draw(pantalla)
    
    #jugadores.draw(pantalla)

    pygame.display.flip()
    reloj.tick(60)
    
pygame.quit()
sys.exit()