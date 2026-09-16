# Interacción con NPC y Objetos
#==============================
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
# --- SISTEMA DE DIÁLOGOS ---
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
# --- CLASE PERSONAJE NO JUGADOR ---
class NPC:
    def __init__(self, x, y, nombre, linea_dialogo, color):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.nombre = nombre
        self.dialogo = linea_dialogo
        self.color = color

    def interactuar(self, inventario):
        return self.nombre, self.dialogo
    
    def dibujar(self,superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 50)
# Paso 1. Creación de Personaje Interactivo Aliado ---
# --- CLASE DE MERCADER ---
class Mercader:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.color = (200, 100, 50) # Un color anaranjado/cobrizo
        self.espada_entregada = False
        
    def interactuar(self, inventario):
        # Si ya te dio la espada, cambia su diálogo
        if self.espada_entregada:
            return "Herrero", "¡Ve a probar esa Espada! Presiona [A] cerca del enemigo."
        
        # Contar cuántas monedas tienes
        cantidad_monedas = inventario.objetos.count("Moneda de Oro")
        
        if cantidad_monedas >= 2:
            # Quitar las dos monedas
            inventario.objetos.remove("Moneda de Oro")
            inventario.objetos.remove("Moneda de Oro")
            
            # Entregar la espada
            inventario.agregar("Espada")
            self.espada_entregada = True
            return "Herrero", "¡Trato hecho! Aquí tienes tu Espada."
        else:
            return "Herrero", "Necesito 2 Monedas de Oro para entregarte un arma."
            
    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 40)     
# --- CLASE PARED / OBSTÁCULOS ---
class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = (120, 120, 120)
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
# --- CLASE COFRE ---
class Cofre:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.abierto = False
        self.color_cerrado = (150, 90, 30)
        self.color_abierto = (220, 180, 50)

    def interactuar(self, inventario):
        if not self.abierto:
            self.abierto = True
            inventario.agregar("Moneda de Oro")
            return "Sistema", "¡Abriste un cofre y obtuviste una Moneda de Oro!"
        return "Sistema", "El cofre ya está vacío."
    
    def dibujar(self, superficie):
        color = self.color_abierto if self.abierto else self.color_cerrado
        pygame.draw.rect(superficie, color, self.rect)

# --- CLASE CUEVA/PUERTA ---
class Cueva:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.color = (10, 10, 10)

    def interactuar(self, inventario):
        return "Sistema", "Entraste a la cueva misteriosa..."
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
        
# --- CLASE JUGADOR ---
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
# Paso 4. Creación de Personaje Interactivo Enemigo ---
# --- CLASE ENEMIGO ---
class Enemigo:
    def __init__(self, x, y, limite_arriba, limite_abajo):
        self.rect = pygame.Rect(x, y, 45, 45)
        self.color = (220, 50, 50) # Rojo
        self.velocidad_y = 3
        # Limitamos su movimiento para que se mueva de arriba hacia abajo 
        # con un patrón sencillo
        self.limite_arriba = limite_arriba      
        self.limite_abajo = limite_abajo
        # Verificamos si es derrotado o no para que desaparezca
        self.derrotado = False

    # Definimos su método de movimiento automático
    def actualizar(self):
        # Movimiento automático de patrulla
        if not self.derrotado:
            self.rect.y += self.velocidad_y
            if self.rect.y <= self.limite_arriba or self.rect.y >= self.limite_abajo:
                self.velocidad_y *= -1 # Invierte la dirección
    # Definimos su interacción en caso de intentar otras acciones con él
    def interactuar(self, inventario):
        # Respuesta por defecto si intentas hablarle con [E]
        if self.derrotado:
            return "Sistema", "El enemigo ya ha sido derrotado."
        return "Enemigo", "¡Grrr! ¡No te me acerques!"

    def recibir_ataque(self, inventario):
        if not self.derrotado:
            if "Espada" in inventario.objetos:
                self.derrotado = True
                inventario.agregar("Llave")
                return "Sistema", "¡Derrotaste al enemigo y obtuviste una Llave!"
            else:
                return "Sistema", "¡Necesitas un arma para derrotar a este enemigo!"
        return None, None

    def dibujar(self, superficie):
        if not self.derrotado:
            pygame.draw.rect(superficie, self.color, self.rect)
            
# --- CLASE INVENTARIO ---
class Inventario:
    def __init__(self):
        self.objetos = []
        self.abierto = False
        self.rect = pygame.Rect(ancho_pantalla - 250, 50, 200, 300)
        
    def agregar(self, item):
        self.objetos.append(item)
        
    def alternar(self):
        self.abierto = not self.abierto
        
    def dibujar(self, superficie):
        if not self.abierto:
            return
        
        pygame.draw.rect(superficie, (40, 40, 50), self.rect)
        pygame.draw.rect(superficie, (200, 200, 200), self.rect, 2)

        texto_titulo = fuente.render("INVENTARIO", True, (255, 255, 255))
        superficie.blit(texto_titulo, (self.rect.x + 10, self.rect.y + 10))

        y_offset = 50
        if len(self.objetos) == 0:
            texto_vacio = fuente.render("(Vacío)", True, (150, 150, 150))
            superficie.blit(texto_vacio, (self.rect.x + 10, self.rect.y + y_offset))
        else:
            for item in self.objetos:
                texto_item = fuente.render("- " + item, True, (200, 255, 200))
                superficie.blit(texto_item, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 30

jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)
sistema_dialogo = SistemaDialogo()

sala_x = 0
sala_y = 0
# Paso 2. Integrar al mercader en el mapa a través de las salas
# Paso 5. Integramos al enemigo patrullando el mapa
salas_interacciones = {
    (-1,0) : [
        NPC(0, alto_pantalla//2 - 50, "Guardián", "No puedes seguir avanzando.",(150, 150, 250))
        ],
    (0,-1) : [
        Cofre(400, 300),
        Cueva(200, 200)
        ],
    (0,1) : [
        Cofre(200, 200),
        # Incluimos al Mercader en la sala Sur
        Mercader(600, 300)      #Actualizado
        ],
    # Incluimos al Enemigo en la sala Este, patrullando de Y=200 a Y=500
    (1,0) : [
        Enemigo(400, 200, 200, 500)     #Actualizado
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

inventario_jugador = Inventario()

encendido = True
while encendido:
    obstaculos_actuales = salas_paredes.get((sala_x, sala_y), [])
    interacciones_actuales = salas_interacciones.get((sala_x,sala_y), [])

    lista_colisiones = list(obstaculos_actuales)
    for obj in interacciones_actuales:
        # Paso 3. Incluir al mercader en la pared temporal para que no sea atravesado
        if isinstance(obj,NPC) or isinstance(obj, Mercader):        #Actualizado
            class ParedTemporal:
                def __init__(self, rect):
                    self.rect = rect
            lista_colisiones.append(ParedTemporal(obj.rect))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            encendido = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_i:
                inventario_jugador.alternar()
                
            elif evento.key == pygame.K_e:
                if sistema_dialogo.activo:
                    sistema_dialogo.cerrar()
                else:
                    zona_jugador = jugador.obtener_zona_interaccion()
                    for objeto in interacciones_actuales:
                        if zona_jugador.colliderect(objeto.rect):
                            nombre, texto = objeto.interactuar(inventario_jugador)
                            sistema_dialogo.iniciar(nombre, texto)
                            break
            # Paso 6. Agregar la detección de la tecla [A] para atacar
            elif evento.key == pygame.K_a: # Atacar
                zona_jugador = jugador.obtener_zona_interaccion()
                for objeto in interacciones_actuales:
                    if isinstance(objeto, Enemigo) and not objeto.derrotado:
                        if zona_jugador.colliderect(objeto.rect):
                            nombre, texto = objeto.recibir_ataque(inventario_jugador)
                            if nombre:
                                sistema_dialogo.iniciar(nombre, texto)
                            break
    # Paso 7. Implementar el movimiento del enemigo 
    # Actualizar movimiento de enemigos presentes en la sala actual
    for objeto in interacciones_actuales:
        if isinstance(objeto, Enemigo):
            objeto.actualizar()
            
    if not sistema_dialogo.activo:
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas, lista_colisiones)

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
        if not sistema_dialogo.activo and zona_jugador.colliderect(objeto.rect):
            texto_e = fuente.render("[E]", True, (255, 255, 255))
            pantalla.blit(texto_e,(objeto.rect.x + 5, objeto.rect.y - 25))

    jugador.dibujar(pantalla)
    
    sistema_dialogo.dibujar(pantalla)

    inventario_jugador.dibujar(pantalla)
    
    pygame.display.flip()
    
    reloj.tick(FPS)
    
pygame.quit()

sys.exit()