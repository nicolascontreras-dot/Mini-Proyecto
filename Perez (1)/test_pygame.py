from pathlib import Path
import pygame
import sys

pygame.init()
reloj= pygame.time.Clock()

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / 'images'

ancho_ventana = 1200                                            
alto_ventana = 720                                              
tamaño_ventana = (ancho_ventana,alto_ventana)                   
pantalla = pygame.display.set_mode(tamaño_ventana) 
#pantalla.fill((237, 201, 175)) #escoger color de fondo adecuado  (60,80,100) 237, 201, 175
pygame.display.set_caption('Pygame Helenanito')

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / 'images'

pantalla_playa = pygame.image.load(CARPETA_IMAGENES / 'playa.jpeg').convert()
pantalla_playa = pygame.transform.scale(pantalla_playa,tamaño_ventana)
pantalla_bifurcacion = pygame.image.load(CARPETA_IMAGENES / 'bifurcacion.jpeg').convert()
pantalla_bifurcacion = pygame.transform.scale(pantalla_bifurcacion,tamaño_ventana)
pantalla_cueva= pygame.image.load(CARPETA_IMAGENES / 'cueva.jpeg').convert()
pantalla_cueva = pygame.transform.scale(pantalla_cueva,tamaño_ventana)

prota_abajo =  pygame.image.load(CARPETA_IMAGENES/"sprite_abajo_0.png").convert_alpha()
prota_abajo_1 = pygame.image.load(CARPETA_IMAGENES/"sprite_abajo_1.png").convert_alpha()
prota_abajo_2 = pygame.image.load(CARPETA_IMAGENES/"sprite_abajo_2.png").convert_alpha()

imagenes_abajo = [
    prota_abajo,
    prota_abajo_1,
    prota_abajo_2
]

prota_arriba =  pygame.image.load(CARPETA_IMAGENES/"sprite_arriba_0.png").convert_alpha()
prota_arriba_1 = pygame.image.load(CARPETA_IMAGENES/"sprite_arriba_1.png").convert_alpha()
prota_arriba_2 = pygame.image.load(CARPETA_IMAGENES/"sprite_arriba_2.png").convert_alpha()

imagenes_arriba = [
    prota_arriba,
    prota_arriba_1,
    prota_arriba_2
]

prota_derecha_1 = pygame.image.load(CARPETA_IMAGENES/"sprite_derecha_1.png").convert_alpha()
prota_derecha_2 = pygame.image.load(CARPETA_IMAGENES/"sprite_derecha_2.png").convert_alpha()

imagenes_derecha = [
    prota_derecha_1,
    prota_derecha_2
]

prota_izquierda_1 = pygame.image.load(CARPETA_IMAGENES/"sprite_izq_1.png").convert_alpha()
prota_izquierda_2 = pygame.image.load(CARPETA_IMAGENES/"sprite_izq_2.png").convert_alpha()

imagenes_izquierda = [
    prota_izquierda_1,
    prota_izquierda_2
]

imagenes_abajo = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_abajo]
imagenes_arriba = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_arriba]
imagenes_derecha = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_derecha]
imagenes_izquierda = [pygame.transform.scale_by(imagen, 0.3) for imagen in imagenes_izquierda]

imagenes_jugador = {
    'derecha' : imagenes_derecha,
    'izquierda' : imagenes_izquierda,
    'arriba' : imagenes_arriba,
    'abajo' : imagenes_abajo
}
#tamaño 177x341
anne_imagen = pygame.image.load(CARPETA_IMAGENES / 'vision_frente_anne.png')
anne_imagen=pygame.transform.scale(anne_imagen, (53.1, 102.3))

esqueleto_imagen=pygame.image.load(CARPETA_IMAGENES / 'esqueleto.png')
esqueleto_imagen=pygame.transform.scale_by(esqueleto_imagen,0.35)

cinturon_imagen=pygame.image.load(CARPETA_IMAGENES / 'cinturon.png')
cinturon_imagen=pygame.transform.scale_by(cinturon_imagen,0.1)

espada_imagen=pygame.image.load(CARPETA_IMAGENES / 'espada (2).png')
espada_imagen=pygame.transform.scale_by(espada_imagen,0.2)

mapa_imagen= pygame.image.load(CARPETA_IMAGENES / 'objeto_mapa.png')
mapa_imagen=pygame.transform.scale_by(mapa_imagen,0.1)

fuente = pygame.font.Font(None,150)         
texto_playa = fuente.render("La Playa",False,(255,255,255))
texto_bifurcacion = fuente.render("Bifurcacion",False,(255,255,255))
texto_cueva = fuente.render("La Cueva",False,(255,255,255))

#Obstáculos
mar = pygame.Rect(0,464,464,531)
mar_derecha = pygame.Rect(492,336,778,336)
palmeras_izquierda = pygame.Rect(0,0,53,434)
palmeras_2 = pygame.Rect(53,0,477,110)
palmeras_3 = pygame.Rect(669,0,531,110)
palmeras_4 = pygame.Rect(1147,0,53,434)
obstaculos_playa = [mar,mar_derecha,palmeras_izquierda,palmeras_2,palmeras_3,palmeras_4]          

arbol_esq_sup_izq = pygame.Rect(0,0,458,204)
arbol_esq_sup_der = pygame.Rect(723,0,477,204) 
tierra_barco = pygame.Rect(935,204,265,102)
lago = pygame.Rect(0,363,358,357)
tierra_lago = pygame.Rect(358, 490, 159, 255)
arbol_barco = pygame.Rect(723,414,477,306)
obstaculos_bifurcacion = [arbol_esq_sup_izq,arbol_esq_sup_der,tierra_barco,lago,tierra_lago,arbol_barco]

esquina_superior_izq = pygame.Rect(0,0,530,95)
esquina_superior_der = pygame.Rect(690.3,0,424.8,95)
columna_izq =pygame.Rect(0,0,53.1,818.4)
columna_der =pygame.Rect(1146.9,0,53.1,818.4)
esquina_inferior_izq = pygame.Rect(0,688,477,51.15)
esquina_inferior_der = pygame.Rect(690.3,688,424.8,51.15)
bloque_sup_izq = pygame.Rect(318.6,255.75,212.4,51.3)
bloque_inf_izq = pygame.Rect(185.85,454.5,265.4,51.3)
bloque_sup_der = pygame.Rect(672.9,255.75,212.4,51.3)
bloque_inf_der =pygame.Rect(672.9,454.5,265.4,51.3)
obstaculos_cueva =[esquina_superior_izq,esquina_superior_der,columna_izq,columna_der,esquina_inferior_izq,esquina_inferior_der,bloque_sup_izq,bloque_inf_izq,bloque_sup_der,bloque_inf_der]

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
        self.tiene_cinturon = False
    
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
                          #Agrega tu propio Sprite a los sprite configurados de pygame


    def mover(self, teclas, obstaculos):

        moviendose = False

        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.cambiar_direccion("derecha")
            moviendose = True
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo):
                    self.rect.x -= self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.x -= self.velocidad
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.cambiar_direccion("izquierda")
            moviendose = True
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo):
                    self.rect.x += self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
            self.cambiar_direccion("arriba")
            moviendose = True
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo):
                    self.rect.y += self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.y += self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
            self.cambiar_direccion("abajo")
            moviendose = True
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo):
                    self.rect.y -= self.velocidad
            for enemigo in enemigos:
                if self.rect.colliderect(enemigo):
                    self.rect.y -= self.velocidad
                    #pass
        if moviendose:
            self.animar()
        
        else:
            self.frame = 0
            self.image = self.imagenes[self.direccion][self.frame]
        
    def recoger (self, objetos, inventario):
        for objeto in objetos:
            if self.rect.colliderect(objeto.rect):

                if objeto.nombre == "Cinturon":
                    self.tiene_cinturon = True
                    inventario.append(objeto.nombre)
                    objetos.remove(objeto)
                    return objeto.nombre

                if self.tiene_cinturon:
                    inventario.append(objeto.nombre)
                    objetos.remove(objeto)
                    return objeto.nombre
                else:
                    return "NO_CINTURON"
        return None      

class Aliado(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 3
    def perseguir(self,jugador,obstaculos):
        
        if self.rect.x<jugador.rect.x:
                self.rect.x += self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.x -= self.velocidad
        
        if self.rect.x>jugador.rect.x:
                self.rect.x -= self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.x += self.velocidad
    
        if self.rect.y>jugador.rect.y:
                self.rect.y -= self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.y += self.velocidad
        
        if self.rect.y<jugador.rect.y:
                self.rect.y += self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.y -= self.velocidad
    


class Enemigo(pygame.sprite.Sprite):

    def __init__(self, imagen, x, y):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = 2.5

    def perseguir(self,jugador,obstaculos):
        if teclas[pygame.K_RIGHT]:
            if self.rect.x<jugador.rect.x:
                self.rect.x += self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.x -= self.velocidad
        if teclas[pygame.K_LEFT]:
            if self.rect.x>jugador.rect.x:
                self.rect.x -= self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            if self.rect.y>jugador.rect.y:
                self.rect.y -= self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.y += self.velocidad
        if teclas[pygame.K_DOWN]:
            if self.rect.y<jugador.rect.y:
                self.rect.y += self.velocidad
                for obstaculo in obstaculos:
                    if self.rect.colliderect(obstaculo):
                        self.rect.y -= self.velocidad       

class Objeto(pygame.sprite.Sprite):
    def __init__(self, nombre, imagen, x, y,zona):
        super().__init__()
        self.nombre = nombre
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.zona = zona

#class ZonaRectangular(pygame.sprite.Sprite)




#Variables de "objetos" tipo class
#=================================    
jugador = Jugador(imagenes_jugador,500,200,)
enemigo = Enemigo(esqueleto_imagen,800,400)
cinturon = Objeto('Cinturon',cinturon_imagen,100,100,'playa')
aliado = Aliado(anne_imagen, 300, 300)

espada = Objeto('Espada',espada_imagen,250,439,'playa')
mapa = Objeto('Mapa',mapa_imagen,850,150,'playa')

    #... en caso de tener varios jugadores o personajes de una misma facción
    #=======================================================================
jugadores = pygame.sprite.Group()                               #Representa un Grupo de sprites configurados de pygame
jugadores.add(jugador)

aliados = pygame.sprite.Group()
aliados.add(aliado)

    #... en caso de tener varios jugadores o personajes de una misma facción
    #=======================================================================
enemigos = pygame.sprite.Group()
enemigos.add(enemigo)

objetos = pygame.sprite.Group()
objetos.add(cinturon)
objetos.add(mapa)
objetos.add(espada)

#Zona actual
texto_actual = texto_playa
obstaculos_actuales = obstaculos_playa
zona_actual = "playa"

inventario = []



#Motor del juego
#============================
ejecutando = True 
while ejecutando:                                               
    for event in pygame.event.get():                            
        if event.type == pygame.QUIT:
            ejecutando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                objeto_recogido = jugador.recoger(objetos,inventario)
                if objeto_recogido == "NO_CINTURON":
                    print("Necesitas un cinturon para guardar el objeto.")
                elif objeto_recogido:
                    print("Has recogido:",objeto_recogido)

    teclas = pygame.key.get_pressed() 
    if zona_actual == "playa":
        pantalla_actual = pantalla_playa
        texto_actual = texto_playa
        obstaculos_actuales = obstaculos_playa
    elif zona_actual == "bifurcacion":
        pantalla_actual = pantalla_bifurcacion
        texto_actual = texto_bifurcacion
        obstaculos_actuales = obstaculos_bifurcacion 
    elif zona_actual == 'cueva':
        pantalla_actual = pantalla_cueva
        texto_actual = texto_cueva
        obstaculos_actuales = obstaculos_cueva

        
    jugador.mover(teclas,obstaculos_actuales)
    aliado.perseguir(jugador,obstaculos_actuales)

    if zona_actual == "playa":
        if jugador.rect.top <= 0:                 
            zona_actual = "bifurcacion"             
            jugador.rect.bottom = alto_ventana      
            aliado.rect.midbottom = (jugador.rect.centerx,alto_ventana + 50)
    elif zona_actual == "bifurcacion":
        if jugador.rect.bottom>=alto_ventana:
            zona_actual = "playa"
            jugador.rect.top = 0
            aliado.rect.midbottom = (jugador.rect.centerx,0)
   # elif zona_actual == 'cueva':
        #if jugador.rect.bottom>=alto_ventana:
         #   zona_actual = 'bifurcacion'
          #  jugador.rect.top = 0
           # aliado.rect.midbottom = (jugador.rect.centerx,0)



    
            
   
   
    pantalla.blit(pantalla_actual,(0,0))
    pantalla.blit(texto_actual,(0,0))
    

  
    for objeto in objetos:
        if objeto.zona == zona_actual:
            pantalla.blit(objeto.image,objeto.rect)

    aliados.draw(pantalla)
    jugadores.draw(pantalla)

   

    pygame.display.flip()   

    reloj.tick(60)  

pygame.quit()