from pathlib import Path
import math
import pygame
import sys
pygame.init()
reloj = pygame.time.Clock()
DEBUG = True
ancho_pantalla = 1360
alto_pantalla = 820
tamaño_pantalla = (ancho_pantalla, alto_pantalla)
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Prueba Pygame")
CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"
pantalla_playa = pygame.image.load(CARPETA_IMAGENES/"Fondo playa limpia.jpg").convert()
pantalla_playa = pygame.transform.scale(pantalla_playa, tamaño_pantalla)
pantalla_bosque = pygame.image.load(CARPETA_IMAGENES/"fondo_bosque.png").convert()
pantalla_bosque = pygame.transform.scale(pantalla_bosque, tamaño_pantalla)
pantalla_cueva = pygame.image.load(CARPETA_IMAGENES/"fondo_cueva.png").convert()
pantalla_cueva = pygame.transform.scale(pantalla_cueva, tamaño_pantalla)
pantalla_roquerio = pygame.image.load(CARPETA_IMAGENES/"fondo_roquerio.jpg").convert()
pantalla_roquerio = pygame.transform.scale(pantalla_roquerio, tamaño_pantalla)
cuadro_imagen = pygame.image.load(CARPETA_IMAGENES/"Cuadro de texto.png").convert_alpha()
cuadro_imagen = pygame.transform.scale(cuadro_imagen, (600, 100))
fuente_mensaje = pygame.font.Font(None, 36)
aventurero_imagen = pygame.image.load(CARPETA_IMAGENES/"Aventurero.png").convert_alpha()
aventurero_imagen = pygame.transform.scale_by(aventurero_imagen, 0.15)
guia_imagen = pygame.image.load(CARPETA_IMAGENES/"Guía.png").convert_alpha()
guia_imagen = pygame.transform.scale_by(guia_imagen, 0.1)
cangrejo_imagen = pygame.image.load(CARPETA_IMAGENES/"cangrejo enemigo.png").convert_alpha()
cangrejo_imagen = pygame.transform.scale_by(cangrejo_imagen, 0.08)
mochila_imagen = pygame.image.load(CARPETA_IMAGENES/"Mochila.png").convert_alpha()
mochila_imagen = pygame.transform.scale_by(mochila_imagen, 0.1)
cuaderno_imagen = pygame.image.load(CARPETA_IMAGENES/"Cuaderno.png").convert_alpha()
cuaderno_imagen = pygame.transform.scale_by(cuaderno_imagen, 0.5)
estatuilla_imagen = pygame.image.load(CARPETA_IMAGENES/"Estatuilla.png").convert_alpha()
estatuilla_imagen = pygame.transform.scale_by(estatuilla_imagen, 0.5)
mapa_imagen = pygame.image.load(CARPETA_IMAGENES/"Mapa.png").convert_alpha()
mapa_imagen = pygame.transform.scale_by(mapa_imagen, 0.5)
roca_imagen = pygame.image.load(CARPETA_IMAGENES/"Roca_generica.png").convert_alpha()
roca_imagen = pygame.transform.scale_by(roca_imagen, 0.1)
arbol_imagen = pygame.image.load(CARPETA_IMAGENES/"Arbol individual.png").convert_alpha()
arbol_imagen = pygame.transform.scale_by(arbol_imagen, 0.35)
fuente = pygame.font.Font(None, 150)
texto_playa = fuente.render("La Playa", False, (255, 255, 255))
texto_bosque = fuente.render("El Bosque", False, (255, 255, 255))
texto_cueva = fuente.render("La Cueva", False,(255,255,255))
def colision_circulo_rectangulo(centro_circulo, radio_circulo, rect_zona):
    cx_cercano = max(rect_zona.left, min(centro_circulo[0], rect_zona.right))
    cy_cercano = max(rect_zona.top, min(centro_circulo[1], rect_zona.bottom))
    distancia_x = centro_circulo[0] - cx_cercano
    distancia_y = centro_circulo[1] - cy_cercano
    distancia_cuadrado = (distancia_x ** 2) + (distancia_y ** 2)
    return distancia_cuadrado < (radio_circulo ** 2)
class Jugador(pygame.sprite.Sprite): 
    def __init__(self, nombre, imagen, coordenada_x, coordenada_y, zona):
        super().__init__()
        self.nombre = nombre
        self.zona = zona
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = (coordenada_x, coordenada_y)
        self.velocidad = 5
        self.radio = self.rect.width * 0.22
        self.desplazamiento_y = 10
        self.tiene_mochila = False
        self.centro_pies = [self.rect.midbottom[0], self.rect.midbottom[1] - self.desplazamiento_y]
    def sincronizar_pies(self):
        self.centro_pies = [self.rect.midbottom[0], self.rect.midbottom[1] - self.desplazamiento_y]
    def mover(self, teclas, obstaculos):
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.sincronizar_pies()
            if self.colision_obstaculos(obstaculos):
                self.rect.x -= self.velocidad
                self.sincronizar_pies()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.sincronizar_pies()
            if self.colision_obstaculos(obstaculos):
                self.rect.x += self.velocidad
                self.sincronizar_pies()
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
            self.sincronizar_pies()
            if self.colision_obstaculos(obstaculos):
                self.rect.y += self.velocidad
                self.sincronizar_pies()
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
            self.sincronizar_pies()
            if self.colision_obstaculos(obstaculos):
                self.rect.y -= self.velocidad
                self.sincronizar_pies()
    def colision_obstaculos(self, obstaculos):
        centro_x, centro_y = self.centro_pies
        for obstaculo in obstaculos:
            if getattr(obstaculo, "tipo_forma", "circulo") == "rectangulo":
                if colision_circulo_rectangulo(self.centro_pies, self.radio, obstaculo.rect):
                    return True
            else:
                distancia_x = centro_x - obstaculo.centro[0]
                distancia_y = centro_y - obstaculo.centro[1]
                if math.hypot(distancia_x, distancia_y) < (self.radio + obstaculo.radio):
                    return True
        return False
    def recoger(self, objetos, inventario, zona_actual):
        for objeto in objetos: 
            if objeto.zona == zona_actual and self.rect.colliderect(objeto.rect):  
                if objeto.nombre == "Mochila":  
                    self.tiene_mochila = True  
                    inventario.append(objeto.nombre) 
                    objetos.remove(objeto)   
                    return objeto.nombre  
                elif self.tiene_mochila:    
                    inventario.append(objeto.nombre)  
                    objetos.remove(objeto)   
                    return objeto.nombre  
                else:  
                    return "NO_MOCHILA" 
        return None
    @property 
    def posicion_y(self): 
        return self.rect.bottom 
class Aliado(pygame.sprite.Sprite):
    def __init__(self, imagen, x, y, zona): 
        super().__init__()  
        self.image = imagen  
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)  
        self.velocidad = 3  
        self.zona = zona     
class Cangrejo(pygame.sprite.Sprite):   
    def __init__(self, imagen, x, y): 
        super().__init__()  
        self.image = imagen  
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y) 
        self.velocidad = 2 
    def perseguir(self, jugador):  
        if jugador.rect.centerx > self.rect.centerx + 2:
            self.rect.x += self.velocidad  
        elif jugador.rect.centerx < self.rect.centerx - 2: 
            self.rect.x -= self.velocidad 
class Objeto(pygame.sprite.Sprite): 
    def __init__(self, nombre, imagen, x, y, zona): 
        super().__init__()  
        self.nombre = nombre 
        self.image = imagen   
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y) 
        self.zona = zona 
class Roca(pygame.sprite.Sprite):       
    def __init__(self, imagen, coordenada_x, coordenada_y): 
        super().__init__()     
        self.image = imagen              
        self.rect = self.image.get_rect()
        self.rect.topleft = (coordenada_x, coordenada_y) 
        self.centro = list(self.rect.center)  
        self.radio = self.rect.width * 0.3  
    @property          
    def posicion_y(self):  
        return self.rect.bottom 
class Arbol(pygame.sprite.Sprite):  
    def __init__(self, imagen, coordenada_x, coordenada_y, zona):
        super().__init__()     
        self.image = imagen    
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (coordenada_x, coordenada_y)  
        desplazamiento_y = 30    
        self.centro = [self.rect.midbottom[0], self.rect.midbottom[1] - desplazamiento_y]    
        self.radio = self.rect.width * 0.2
        self.zona = zona   
    @property    
    def posicion_y(self):   
        return self.rect.bottom
class ZonaRectangular(pygame.sprite.Sprite):    
    def __init__(self, x, y, ancho, alto, zona="playa"):  
        super().__init__()            
        self.rect = pygame.Rect(x, y, ancho, alto) 
        self.tipo_forma = "rectangulo"  
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)   
        self.image.fill((0, 0, 0, 0))  
        self.zona = zona    
    @property       
    def posicion_y(self): 
        return self.rect.bottom  
class ZonaTransicion(pygame.sprite.Sprite):      
    def __init__(self, x, y, ancho, alto, destino_zona, punto_aparicion):
        super().__init__()          
        self.rect = pygame.Rect(x, y, ancho, alto)  
        self.destino_zona = destino_zona   
        self.punto_aparicion = punto_aparicion 
transiciones_playa = [                  
    ZonaTransicion(600,0,150,10,"bosque",(600, 620)),
    ZonaTransicion(0,200,10,150,"cueva",(1200,275)),
]
transiciones_bosque = [
    ZonaTransicion(600,800,150,10,"playa",(620, 20))
]
jugador = Jugador("Kano", aventurero_imagen, 500, 500, "playa")
jugadores = pygame.sprite.Group()   
jugadores.add(jugador)  
cangrejo = Cangrejo(cangrejo_imagen, 900, 700)
guia = Aliado(guia_imagen, 1000, 400, "playa")
mochila = Objeto("Mochila", mochila_imagen, 300, 400, "playa")
cuaderno = Objeto("Cuaderno", cuaderno_imagen, 900, 550, "bosque")
mapa = Objeto("Mapa", mapa_imagen, 1100, 550, "playa")
estatuilla = Objeto("Estatuilla", estatuilla_imagen, 1300, 550, "bosque")
aliados = pygame.sprite.Group()
aliados.add(guia)
enemigos = pygame.sprite.Group()
enemigos.add(cangrejo)
objetos = pygame.sprite.Group()
objetos.add(mochila, cuaderno, mapa, estatuilla)
roca1 = Roca(roca_imagen, 1255, 320)
roca2 = Roca(roca_imagen, 1265, 420)
roca3 = Roca(roca_imagen, 1255, 520)
roca4 = Roca(roca_imagen, 1265, 620)
roca5 = Roca(roca_imagen, 1255, 720)
obstaculos = pygame.sprite.Group()
zona_mar = ZonaRectangular(0, 720, ancho_pantalla, alto_pantalla, "playa")
obstaculos_playa = [
    Arbol(arbol_imagen, 700, 80, "playa"), Arbol(arbol_imagen, 800, 80, "playa"),
    Arbol(arbol_imagen, 900, 80, "playa"), Arbol(arbol_imagen, 1000, 80, "playa"),
    Arbol(arbol_imagen, 1100, 80, "playa"), Arbol(arbol_imagen, 1200, 80, "playa"),
    Arbol(arbol_imagen, 750, 170, "playa"), Arbol(arbol_imagen, 850, 170, "playa"),
    Arbol(arbol_imagen, 950, 170, "playa"), Arbol(arbol_imagen, 1050, 170, "playa"),
    Arbol(arbol_imagen, 1150, 170, "playa"), Arbol(arbol_imagen, 1250, 170, "playa"),
    Arbol(arbol_imagen, 700, 260, "playa"), Arbol(arbol_imagen, 800, 260, "playa"),
    Arbol(arbol_imagen, 900, 260, "playa"), Arbol(arbol_imagen, 1000, 260, "playa"),
    Arbol(arbol_imagen, 1100, 260, "playa"), Arbol(arbol_imagen, 1200, 260, "playa"),
    Arbol(arbol_imagen, 750, 350, "playa"), Arbol(arbol_imagen, 850, 350, "playa"),
    Arbol(arbol_imagen, 950, 350, "playa"), Arbol(arbol_imagen, 1050, 350, "playa"),
    Arbol(arbol_imagen, 1150, 350, "playa"),
    Arbol(arbol_imagen, 500, 80, "playa"), Arbol(arbol_imagen, 400, 80, "playa"),
    Arbol(arbol_imagen, 300, 80, "playa"), Arbol(arbol_imagen, 200, 80, "playa"),
    Arbol(arbol_imagen, 100, 80, "playa"), Arbol(arbol_imagen, 0, 80, "playa"),
    Arbol(arbol_imagen, 450, 170, "playa"), Arbol(arbol_imagen, 350, 170, "playa"),
    Arbol(arbol_imagen, 250, 170, "playa"), Arbol(arbol_imagen, 150, 170, "playa"),
    Arbol(arbol_imagen, 50, 170, "playa"),
    Arbol(arbol_imagen, 500, 260, "playa"), Arbol(arbol_imagen, 400, 260, "playa"),
    Arbol(arbol_imagen, 300, 260, "playa"), Arbol(arbol_imagen, 200, 260, "playa"),
    Arbol(arbol_imagen, 100, 260, "playa"), Arbol(arbol_imagen, 0, 260, "playa"),
    Arbol(arbol_imagen, 450, 350, "playa"), Arbol(arbol_imagen, 350, 350, "playa"),
    Arbol(arbol_imagen, 250, 350, "playa"), Arbol(arbol_imagen, 150, 350, "playa"),
    Arbol(arbol_imagen, 50, 350, "playa"),           
]
obstaculos_bosque = [
    ZonaRectangular(0, 650, 600, 200, "bosque"),
    ZonaRectangular(850, 650, 580, 200, "bosque"),
    ZonaRectangular(0, 0, 180, 520, "bosque"),
    ZonaRectangular(1400, 0, 130, 520, "bosque"),
    ZonaRectangular(0, 0, 1562, 150, "bosque")
]
zona_actual = "playa"  
inventario = []  
mensaje_texto = ""      
tiempo_mensaje = 0  
encendido = True  
def transicion_fundido(pantalla, reloj, tipo="out", velocidad=15): 
    fundido = pygame.Surface((ancho_pantalla, alto_pantalla))  
    fundido.fill((0, 0, 0)) 
    if tipo == "out": 
        for alpha in range(0, 256, velocidad):
            fundido.set_alpha(alpha)  
            pantalla.blit(fundido, (0, 0))  
            pygame.display.flip() 
            reloj.tick(60)     
    elif tipo == "in":                     
        for alpha in range(255, -1, -velocidad):
            pantalla.blit(pantalla_actual, (0, 0))
            for objeto in objetos:         
                if objeto.zona == zona_actual:
                    pantalla.blit(objeto.image, objeto.rect)
            elementos_visibles = list(obstaculos) + [jugador]
            if zona_actual == "playa":
                elementos_visibles.extend(aliados.sprites() + enemigos.sprites())
            elementos_visibles.sort(key=lambda elemento: elemento.rect.bottom)
            for elemento in elementos_visibles:
                pantalla.blit(elemento.image, elemento.rect)
            fundido.set_alpha(alpha)
            pantalla.blit(fundido, (0, 0))
            pygame.display.flip()
            reloj.tick(60)
while encendido:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encendido = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                DEBUG = not DEBUG
            if event.key == pygame.K_e:
                objeto_recogido = jugador.recoger(objetos, inventario, zona_actual)
                if objeto_recogido == "NO_MOCHILA":
                    mensaje_texto = "¡Necesitas una mochila!"
                    tiempo_mensaje = pygame.time.get_ticks()
                elif objeto_recogido:
                    mensaje_texto = f"Has recogido: {objeto_recogido}"
                    tiempo_mensaje = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()
    obstaculos.empty()
    if zona_actual == "playa":
        pantalla_actual = pantalla_playa
        texto_actual = texto_playa
        obstaculos.add(zona_mar, roca1, roca2, roca3, roca4, roca5)
        for arbol in obstaculos_playa:
            obstaculos.add(arbol)
    elif zona_actual == "bosque":
        pantalla_actual = pantalla_bosque
        texto_actual = texto_bosque
        for limite in obstaculos_bosque:
            obstaculos.add(limite)
    jugador.mover(teclas, obstaculos)
    if zona_actual == "playa":
        cangrejo.perseguir(jugador)
    transiciones_actuales = transiciones_playa if zona_actual == "playa" else transiciones_bosque
    for puerta in transiciones_actuales:
        if colision_circulo_rectangulo(jugador.centro_pies, jugador.radio, puerta.rect):
            transicion_fundido(pantalla, reloj, tipo="out", velocidad=15)
            zona_actual = puerta.destino_zona
            jugador.rect.topleft = puerta.punto_aparicion
            jugador.sincronizar_pies()
            obstaculos.empty()
            if zona_actual == "playa":
                pantalla_actual = pantalla_playa
                texto_actual = texto_playa
                obstaculos.add(zona_mar, roca1, roca2, roca3, roca4, roca5)
                for arbol in obstaculos_playa:
                    obstaculos.add(arbol)
            elif zona_actual == "bosque":
                pantalla_actual = pantalla_bosque
                texto_actual = texto_bosque
                for limite in obstaculos_bosque:
                    obstaculos.add(limite)
            transicion_fundido(pantalla, reloj, tipo="in", velocidad=15)
            break
    pantalla.blit(pantalla_actual, (0, 0))
    for objeto in objetos:
        if objeto.zona == zona_actual:
            pantalla.blit(objeto.image, objeto.rect)
    elementos_visibles = list(obstaculos) + [jugador]
    if zona_actual == "playa":
        elementos_visibles.extend(aliados.sprites() + enemigos.sprites())
    elementos_visibles.sort(key=lambda elemento: elemento.rect.bottom)
    for elemento in elementos_visibles:
        pantalla.blit(elemento.image, elemento.rect)
    pantalla.blit(texto_actual, (0, 0))
    if DEBUG:
        for obstaculo in obstaculos:
            if getattr(obstaculo, "tipo_forma", "circulo") == "rectangulo":
                pygame.draw.rect(pantalla, (255, 0, 0), obstaculo.rect, 2)
            else:
                pygame.draw.circle(pantalla, (255, 0, 0), obstaculo.centro, obstaculo.radio, 2)
        pygame.draw.rect(pantalla, (0, 255, 0), jugador.rect, 2)
        pygame.draw.circle(pantalla, (0, 255, 0), jugador.centro_pies, jugador.radio, 2)
        if zona_actual == "playa":
            for enemigo in enemigos:
                pygame.draw.rect(pantalla, (255, 0, 255), enemigo.rect, 2)
            for aliado in aliados:
                pygame.draw.rect(pantalla, (0, 0, 255), aliado.rect, 2)
        for objeto in objetos:
            if objeto.zona == zona_actual:
                pygame.draw.rect(pantalla, (255, 255, 0), objeto.rect, 2)
        for puerta in transiciones_actuales:
            pygame.draw.rect(pantalla, (0, 0, 255), puerta.rect, 2)
    if mensaje_texto and pygame.time.get_ticks() - tiempo_mensaje < 2500:
        pos_x = (ancho_pantalla - cuadro_imagen.get_width()) // 2
        pos_y = alto_pantalla - 140
        pantalla.blit(cuadro_imagen, (pos_x, pos_y))
        txt_surface = fuente_mensaje.render(mensaje_texto, True, (0, 0, 0))
        txt_rect = txt_surface.get_rect(center=(pos_x + cuadro_imagen.get_width() // 2, pos_y + cuadro_imagen.get_height() // 2))
        pantalla.blit(txt_surface, txt_rect)
    else:
        mensaje_texto = ""
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()
sys.exit()