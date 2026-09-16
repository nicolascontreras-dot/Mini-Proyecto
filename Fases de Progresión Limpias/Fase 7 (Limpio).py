# NPCs y diálogos
#================
import pygame
import sys

pygame.init()

pygame.font.init()

ancho_pantalla = 1280
alto_pantalla = 720
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))

pygame.display.set_caption("Mi Juego de Aventura")

reloj = pygame.time.Clock()
FPS = 60

fuente = pygame.font.SysFont("arial", 22, bold=True)

class SistemaDialogo:
    def __init__(self):
        self.activo = False
        self.texto_actual = ""
        self.nombre_hablante = ""
        self.caja_rect = pygame.Rect(50, alto_pantalla - 150, ancho_pantalla - 100, 120)
    
    def iniciar(self, nombre, texto):
        self.nombre_hablante = nombre
        self.texto_actual = texto
        self.activo = True
        
    def cerrar(self):
        self.activo = False
        
    def dibujar(self, superficie):
        if not self.activo:
            return
        caja_superficie = pygame.Surface((self.caja_rect.width,self.caja_rect.height))
        caja_superficie.set_alpha(200)
        caja_superficie.fill((20, 20, 20))
        superficie.blit(caja_superficie, (self.caja_rect.x, self.caja_rect.y))
        
        pygame.draw.rect(superficie,(255, 255, 255),self.caja_rect, 3)
        
        texto_nombre = fuente.render(self.nombre_hablante + ":", True, (255, 200, 0))
        superficie.blit(texto_nombre, (self.caja_rect.x + 20, self.caja_rect.y +15))
        
        texto_dialogo = fuente.render(self.texto_actual, True, (255, 255, 255))
        superficie.blit(texto_dialogo, (self.caja_rect.x + 20, self.caja_rect.y + 50))
        
        texto_cerrar = fuente.render("[E] para cerrar", True, (150, 150, 150))
        superficie.blit(texto_cerrar, (self.caja_rect.x + self.caja_rect.width - 150, self.caja_rect.y + self.caja_rect.height - 30))

class NPC:
    def __init__(self, x, y, nombre, linea_dialogo, color):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.nombre = nombre
        self.dialogo = linea_dialogo
        self.color = color
    
    def interactuar(self):
        return self.nombre, self.dialogo
    
    def dibujar(self,superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 20)        

class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = (120, 120, 120)
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

class Cofre:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.abierto = False
        self.color_cerrado = (150, 90, 30)     
        self.color_abierto = (220, 180, 50)    
    
    def interactuar(self):
        if not self.abierto:
            self.abierto = True
            return "Sistema", "¡Abriste un cofre y encontraste una moneda!"
        return "Sistema", "El cofre ya está vacío."
    
    def dibujar(self, superficie):
        color = self.color_abierto if self.abierto else self.color_cerrado
        pygame.draw.rect(superficie, color, self.rect)

class Cueva:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.color = (10, 10, 10)   
    
    def interactuar(self):
        return "Entraste a la cueva misteriosa..."
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
        
class Jugador:
    def __init__(self, x, y):
        self.tamaño = 40
        self.rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        self.velocidad = 6
        self.color = (0, 200, 100)

    def mover(self, teclas, obstaculos):
        dx = 0
        dy = 0
               
        if teclas[pygame.K_LEFT]:
            dx -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            dx += self.velocidad
        if teclas[pygame.K_UP]:
            dy -= self.velocidad
        if teclas[pygame.K_DOWN]:
            dy += self.velocidad

        self.rect.x += dx
        for pared in obstaculos:
            if self.rect.colliderect(pared.rect):
                if dx > 0:
                    self.rect.right = pared.rect.left
                if dx < 0:
                    self.rect.left = pared.rect.right
        
        self.rect.y += dy
        for pared in obstaculos:
            if self.rect.colliderect(pared.rect):
                if dy > 0:      
                    self.rect.bottom = pared.rect.top
                if dy < 0:      
                    self.rect.top = pared.rect.bottom
    
    def obtener_zona_interaccion(self):
        return self.rect.inflate(30,30)
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)

sala_x = 0
sala_y = 0

salas_interacciones = {
    (0,-1) : [
        Cofre(400, 300),
        Cueva(200, 200)
        ],
    (0,1) : [
        Cofre(200, 200)
        ]
}

salas_colores = {
    (0,0):(30,30,30),
    (1,0):(50,20,20), 
    (-1,0):(20,50,20), 
    (0,1):(20,20,50),  
    (0,-1):(50,50,20),
}

salas_paredes = {
    (0,0) : [
        Pared(300, 200, 150, 100),
        Pared(800, 400, 200, 150)
        ],
    (1,0) : [
        Pared(500, 150, 280, 420)
    ],
    (-1,0) : [
        Pared(0, 0, 1280, 150),
        Pared(0, 570, 1280, 150)   
    ]
}

mensaje_pantalla = ""
tiempo_mensaje = 0

encendido = True
while encendido:
    if tiempo_mensaje > 0:
        tiempo_mensaje -= 1
    else:
        mensaje_pantalla = ""
    
    obstaculos_actuales = salas_paredes.get((sala_x, sala_y), [])
    interacciones_actuales = salas_interacciones.get((sala_x,sala_y), [])
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:    
            encendido = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e:
                zona_jugador = jugador.obtener_zona_interaccion()
                for objeto in interacciones_actuales:
                    if zona_jugador.colliderect(objeto.rect):
                        mensaje_pantalla = objeto.interactuar()
                        tiempo_mensaje = 120      
                        break
    teclas = pygame.key.get_pressed()
    
    jugador.mover(teclas, obstaculos_actuales)
    
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
    
    for pared in obstaculos_actuales:
        pared.dibujar(pantalla)

    zona_jugador = jugador.obtener_zona_interaccion()
    for objeto in interacciones_actuales:
        objeto.dibujar(pantalla)
        if zona_jugador.colliderect(objeto.rect):
            texto_e = fuente.render("[E]", True, (255, 255, 255))
            pantalla.blit(texto_e,(objeto.rect.x + 5, objeto.rect.y - 25))

    jugador.dibujar(pantalla)
    
    if mensaje_pantalla:
        texto_renderizado = fuente.render(mensaje_pantalla, True, (255, 255, 0))
        pantalla.blit(texto_renderizado, (ancho_pantalla//2 - texto_renderizado.get_width()//2, 50))
    pygame.display.flip()
    reloj.tick(FPS)
pygame.quit()
sys.exit()