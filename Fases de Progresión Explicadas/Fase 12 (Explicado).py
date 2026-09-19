# Final del juego y botón de reinicio
#====================================
# --- BREVE EXPLICACIÓN ---
# Desde la fase 9 a 11 se estableció la estructura básica del juego, de aquí en adelante
# solo se pulen y actualizan para mejorar la fluidez y mecánicas del juego. Por lo tanto,
# los pasos de reinician y se asume que todo lo anterior se comprende a la perfección.
from pathlib import Path
import pygame
import sys

pygame.init()
pygame.font.init()
CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "imagenes"

# --- HERRAMIENTAS ---
reloj = pygame.time.Clock()
FPS = 60
fuente = pygame.font.SysFont("arial", 22, bold=True)

# --- CONFIGURACIÓN DE LA PANTALLA ---
ancho_pantalla = 1280
alto_pantalla = 720
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))
pygame.display.set_caption("Mi Juego de Aventura")

# --- CARGA DE IMÁGENES / SPRITES ---
hoja_sprites = pygame.image.load(CARPETA_IMAGENES/"aventurero_spritesheet.png").convert_alpha()
ancho_hoja = hoja_sprites.get_width()
alto_frame = hoja_sprites.get_height()
ancho_frame = ancho_hoja // 4

imagenes_jugador = {
    "abajo" : pygame.transform.scale_by(hoja_sprites.subsurface(pygame.Rect(0, 0, ancho_frame, alto_frame)), 0.2),
    "derecha" : pygame.transform.scale_by(hoja_sprites.subsurface(pygame.Rect(ancho_frame, 0, ancho_frame, alto_frame)), 0.2),
    "izquierda" : pygame.transform.scale_by(hoja_sprites.subsurface(pygame.Rect(ancho_frame*2, 0, ancho_frame, alto_frame)), 0.2),
    "arriba" : pygame.transform.scale_by(hoja_sprites.subsurface(pygame.Rect(ancho_frame*3, 0, ancho_frame, alto_frame)), 0.2)
}
# --- CLASE DE SISTEMA DE DIÁLOGOS ---
class SistemaDialogo:
    # --- ATRIBUTOS ---
    def __init__(self):
        self.activo = False
        self.texto_actual = ""
        self.nombre_hablante = ""
        self.caja_rect = pygame.Rect(50, alto_pantalla - 150, ancho_pantalla - 100, 120)
    # --- MÉTODO PARA INICIAR EL DIÁLOGO
    def iniciar(self, nombre, texto):
        self.nombre_hablante = nombre
        self.texto_actual = texto
        self.activo = True
    # --- MÉTODO PARA CERRAR EL DIÁLOGO
    def cerrar(self):
        self.activo = False
    # --- MÉTODO PARA MOSTRAR CAJA DE TEXTO ---
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
# --- CLASE DE PERSONAJE FINAL ---
class Principe:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 80)
        self.color = (240, 200, 50)
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        return "Príncipe", "¡Has traído la Reliquia Antigua! El reino está a salvo gracias a ti."
    # --- MÉTODO PARA MOSTRAR AL PERSONAJE ---
    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 35)
# --- CLASE PERSONAJE NO JUGADOR ---
class NPC:
    # --- ATRIBUTOS ---
    def __init__(self, x, y, nombre, linea_dialogo, color):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.nombre = nombre
        self.dialogo = linea_dialogo
        self.color = color
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        return self.nombre, self.dialogo
    # --- MÉTODO PARA MOSTRAR AL PERSONAJE ---    
    def dibujar(self,superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 50)
# --- CLASE DE PERSONAJE DE INTERCAMBIO ---
class Mercader:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.color = (200, 100, 50) 
        self.espada_entregada = False
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        # Si ya intercambió
        if self.espada_entregada:
            return "Herrero", "¡Ve a probar esa Espada! Presiona [A] cerca del enemigo."
        # Contar cuántas monedas tienes
        cantidad_monedas = inventario.objetos.count("Moneda de Oro")
        # Si todavía no intercambió
        if cantidad_monedas >= 2:
            # Quitar las dos monedas
            inventario.objetos.remove("Moneda de Oro")
            inventario.objetos.remove("Moneda de Oro")
            # Entregar el objeto
            inventario.agregar("Espada")
            self.espada_entregada = True
            return "Herrero", "¡Trato hecho! Aquí tienes tu Espada."
        else:
            return "Herrero", "Necesito 2 Monedas de Oro para entregarte un arma."
    # --- MÉTODO PARA MOSTRAR AL PERSONAJE ---               
    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 40)     
# --- CLASE DE NPC CON CONTROL DE ACCESO ---
class Guardia:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 80)
        self.color = (150, 150, 250)
        self.permitido = False
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        # Si ya tienes lo necesario
        if self.permitido:
            return "Guardián", "Puedes pasar. Alguien muy importante te espera más adelante."
        if "Reliquia" in inventario.objetos:
            self.permitido = True
            self.rect.y = 200
            return "Guardián", "¡Es la Reliquia! Tienes permiso para avanzar hacia el Salón."
        else:
            return "Guardián", "No puedes pasar. Solo quienes posean la Reliquia tienen acceso."
    # --- MÉTODO PARA MOSTRAR AL PERSONAJE ---
    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 50)
# --- CLASE PARED / OBSTÁCULOS ---
class Pared:
    # --- ATRIBUTOS ---
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = (120, 120, 120)
    # --- MÉTODO PARA MOSTRAR LA PARED U OBSTÁCULO ---
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
# --- CLASE ALMACENAMIENTO LIBRE ---
class Cofre:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.abierto = False
        self.color_cerrado = (150, 90, 30)
        self.color_abierto = (220, 180, 50)
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        if not self.abierto:
            self.abierto = True
            inventario.agregar("Moneda de Oro")
            return "Sistema", "¡Abriste un cofre y obtuviste una Moneda de Oro!"
        return "Sistema", "El cofre ya está vacío."
    # --- MÉTODO PARA MOSTRAR EL OBJETO ---    
    def dibujar(self, superficie):
        color = self.color_abierto if self.abierto else self.color_cerrado
        pygame.draw.rect(superficie, color, self.rect)
# --- CLASE CUEVA/PUERTA ---
class Cueva:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.color = (10, 10, 10)
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        return "Sistema", "Entraste a la cueva misteriosa..."
    # --- MÉTODO PARA MOSTRAR EL OBJETO ---        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
# --- CLASE PERSONAJE JUGABLE ---
class Jugador:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.velocidad = 5
        self.direccion = "abajo"
        self.imagen = imagenes_jugador[self.direccion]
        self.rect = self.imagen.get_rect(topleft=(x, y))
                
    # --- MÉTODO DE MOVIMIENTO --- 
    def mover(self, teclas, obstaculos):
        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT]:
            dx -= self.velocidad
            self.direccion = "izquierda"
        if teclas[pygame.K_RIGHT]:
            dx += self.velocidad
            self.direccion = "derecha"
        if teclas[pygame.K_UP]:
            dy -= self.velocidad
            self.direccion = "arriba"
        if teclas[pygame.K_DOWN]:
            dy += self.velocidad
            self.direccion = "abajo"
            
        self.imagen = imagenes_jugador[self.direccion]
            
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
                    
    # --- MÉTODO DE INTERACCIÓN CON EL MUNDO ---
    def obtener_zona_interaccion(self):
        return self.rect.inflate(30,30)
    # --- MÉTODO PARA MOSTRAR EL PERSONAJE ---
    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)
# --- CLASE PERSONAJE AGRESIVO ---
class Enemigo:
    # --- ATRIUTOS ---
    def __init__(self, x, y, limite_arriba, limite_abajo):
        self.rect = pygame.Rect(x, y, 45, 45)
        self.color = (220, 50, 50)
        self.velocidad_y = 3
        self.limite_arriba = limite_arriba      
        self.limite_abajo = limite_abajo
        self.derrotado = False
    # --- MÉTODO DE MOVIMIENTO AUTOMÁTICO ---
    def actualizar(self):
        if not self.derrotado:
            self.rect.y += self.velocidad_y
            if self.rect.y <= self.limite_arriba or self.rect.y >= self.limite_abajo:
                self.velocidad_y *= -1
    # --- MÉTODO DE DIÁLOGO ---   
    def interactuar(self, inventario):
        if self.derrotado:
            return "Sistema", "El enemigo ya ha sido derrotado."
        return "Enemigo", "¡Grrr! ¡No te me acerques!"
    # --- MÉTODO DE ENFRENTAMIENTO ---
    def recibir_ataque(self, inventario):
        if not self.derrotado:
            if "Espada" in inventario.objetos:
                self.derrotado = True
                inventario.agregar("Llave")
                return "Sistema", "¡Derrotaste al enemigo y obtuviste una Llave!"
            else:
                return "Sistema", "¡Necesitas un arma para derrotar a este enemigo!"
        return None, None
    # --- MÉTODO PARA MOSTRAR AL PERSONAJE ---
    def dibujar(self, superficie):
        if not self.derrotado:
            pygame.draw.rect(superficie, self.color, self.rect)
# --- CLASE DE ALMACEMIENTO PROPIO ---
class Inventario:
    # --- ATRIBUTOS ---
    def __init__(self):
        self.objetos = []
        self.abierto = False
        self.rect = pygame.Rect(ancho_pantalla - 250, 50, 200, 300)
    # --- MÉTODO PARA GUARDAR OBJETOS ---
    def agregar(self, item):
        self.objetos.append(item)
    # --- MÉTODO PARA ABRIR Y CERRAR ---
    def alternar(self):
        self.abierto = not self.abierto
    # --- MÉTODO PARA MOSTRAR EL ALMACEMIENTO ---
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
# --- CLASE ENTRADA/SALIDA CUEVA ---
class PuertaTeleport:
    # --- ATRIBUTOS ---
    def __init__(self, x, y, destino_sala, destino_pos, etiqueta="Entrada"):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.color = (10, 10, 10)
        self.destino_sala = destino_sala
        self.destino_pos = destino_pos
        self.etiqueta = etiqueta
    # --- MÉTODO DE DIÁLOGO ---   
    def interactuar(self, inventario):
        return "Sistema", f"Usaste la {self.etiqueta}..."
    # --- MÉTODO PARA MOSTRAR LA ENTRADA/SALIDA ---
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
# --- CLASE DE ALMACENAMIENTO CON LLAVE ---
class CofreEspecial:
    # --- ATRIBUTOS ---
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.abierto = False
        self.color_cerrado = (180, 50, 50)
        self.color_abierto = (220, 180, 50)
    # --- MÉTODO DE DIÁLOGO ---
    def interactuar(self, inventario):
        if self.abierto:
            return "Sistema", "El cofre ya está vacío."
        if "Llave" in inventario.objetos:
            inventario.objetos.remove("Llave")
            inventario.agregar("Reliquia")
            self.abierto = True
            return "Sistema", "¡Usaste la Llave, abriste el cofre y encontraste la Reliquia Antigua!"
        else:
            return "Sistema", "El cofre está cerrado con candado. Necesitas una Llave para abrirlo."
    # --- MÉTODO PARA MOSTRAR EL OBJETO ---
    def dibujar(self, superficie):
        color = self.color_abierto if self.abierto else self.color_cerrado
        pygame.draw.rect(superficie, color, self.rect)
# --- UBICACIÓN INICIAL DEL PERSONAJE JUGABLE ---
jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)
# --- CREACIÓN DEL SISTEMA DE DIÁLOGO ---
sistema_dialogo = SistemaDialogo()
# --- CONTROL DE LA UBICACIÓN POR SALA ---
sala_x = 0
sala_y = 0
# --- MAPA DE CONEXIONES PERMITIDAS ---
# Formato: ((sala_origen_x, sala_origen_y), dirección) : (sala_destino_x, sala_destino_y)
conexiones_mapa = {
    ((0, 0), "derecha"): (1, 0),
    ((0, 0), "izquierda"): (-1, 0),
    ((0, 0), "abajo"): (0, 1),
    ((0, 0), "arriba"): (0, -1),
    ((1, 0), "izquierda"): (0, 0),
    ((0, 1), "arriba"): (0, 0),
    ((0, -1), "abajo"): (0, 0),
    ((-1, 0), "derecha"): (0, 0),
    ((-2, 0), "derecha"): (-1, 0),
}
# --- CONTROL DE CREACIÓN DEL MAPA DEL MUNDO ---
def crear_mapa():
    return {
    (-2,0) : [
        Principe(600, 300)
        ],
    (-1,0) : [
        Guardia(50, alto_pantalla//2 - 40)
        ],
    (0,-1) : [
        Cofre(400, 300),
        PuertaTeleport(200, 200, (0, -2), (640, 500), "Entrada a la Cueva")
        ],
    (0,-2) : [
        CofreEspecial(620, 200),
        PuertaTeleport(610, 580, (0, -1), (200, 280), "Salida de la Cueva")
        ],
    (0,1) : [
        Cofre(200, 200),
        Mercader(600, 300)
        ],
    (1,0) : [
        Enemigo(400, 200, 200, 500)
    ]
}
# --- CONFIGURACIÓN DE LAS SALAS ---
salas_interacciones = crear_mapa()
salas_colores = {
    (0,0):(30,30,30),
    (1,0):(50,20,20),
    (-1,0):(20,50,20),
    (-2,0):(60,40,80),
    (0,1):(20,20,50),
    (0,-1):(50,50,20),
    (0,-2):(10,10,25)
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
# --- CREACIÓN DEL ALMACENAMIENTO PROPIO ---
inventario_jugador = Inventario()
# --- CONTROL DE ESTADO DEL JUEGO ---
encendido = True
juego_ganado = False
fuente_victoria = pygame.font.SysFont("arial", 48, bold=True)
# --- MOTOR PRINCIPAL ---
while encendido:
    # --- CONFIGURACIÓN DE LAS INTERACCIONES ---
    obstaculos_actuales = salas_paredes.get((sala_x, sala_y), [])
    interacciones_actuales = salas_interacciones.get((sala_x,sala_y), [])
    lista_colisiones = list(obstaculos_actuales)
    # --- CREACIÓN DE UN BORDE TEMPORAL PARA INTERACTUAR A CIERTA DISTANCIA ---
    for obj in interacciones_actuales:
        if isinstance(obj, (NPC, Mercader, Guardia, Principe)):
            class ParedTemporal:
                def __init__(self, rect):
                    self.rect = rect
            lista_colisiones.append(ParedTemporal(obj.rect))
    # --- DETECCIÓN DE LOS EVENTOS ---
    for evento in pygame.event.get():
        # Si presiona el botón [X] de la pantalla para cerrar
        if evento.type == pygame.QUIT:
            encendido = False
        # Si se presiona un botón del teclado
        elif evento.type == pygame.KEYDOWN:
            # Inventario con la tecla [i]
            if evento.key == pygame.K_i:
                inventario_jugador.alternar()
            # Interacciones con la tecla [e]
            elif evento.key == pygame.K_e:
                if sistema_dialogo.activo:
                    sistema_dialogo.cerrar()
                else:
                    zona_jugador = jugador.obtener_zona_interaccion()
                    for objeto in interacciones_actuales:
                        if zona_jugador.colliderect(objeto.rect):
                            nombre, texto = objeto.interactuar(inventario_jugador)
                            sistema_dialogo.iniciar(nombre, texto)
                            if isinstance(objeto, PuertaTeleport):
                                sala_x, sala_y = objeto.destino_sala
                                jugador.rect.x, jugador.rect.y = objeto.destino_pos
                            if isinstance(objeto, Principe):
                                juego_ganado = True
                            break
            # Reiniciar el juego con la tecla [R]
            elif evento.key == pygame.K_r:
                if juego_ganado:
                    juego_ganado = False
                    sala_x, sala_y = 0, 0
                    jugador.rect.x = ancho_pantalla // 2 - jugador.rect.width // 2
                    jugador.rect.y = alto_pantalla // 2 - jugador.rect.height // 2
                    inventario_jugador = Inventario()
                    salas_interacciones = crear_mapa()
                    sistema_dialogo.cerrar()                
            # Atacar con la tecla [A]
            elif evento.key == pygame.K_a:
                zona_jugador = jugador.obtener_zona_interaccion()
                for objeto in interacciones_actuales:
                    if isinstance(objeto, Enemigo) and not objeto.derrotado:
                        if zona_jugador.colliderect(objeto.rect):
                            nombre, texto = objeto.recibir_ataque(inventario_jugador)
                            if nombre:
                                sistema_dialogo.iniciar(nombre, texto)
                            break
    # --- IMPLEMENTACIÓN DEL MOVIMIENTO AUTOMÁTICO ---
    for objeto in interacciones_actuales:
        if isinstance(objeto, Enemigo):
            objeto.actualizar()
    # --- PERMITIR EL MOVIMIENTO DEL JUGADOR SOLO SI NO HAY UN DIÁLOGO ---
    if not sistema_dialogo.activo:
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas, lista_colisiones)
    # --- TRANSICIÓN DE SALAS Y CONTROL DE LÍMITES DEL MAPA ---
    # Eje Horizontal (Derecha)
    if jugador.rect.x > ancho_pantalla - jugador.rect.width:
        siguiente = conexiones_mapa.get(((sala_x, sala_y), "derecha"))
        if siguiente:
            sala_x, sala_y = siguiente
            jugador.rect.x = 5  # Aparece en el borde izquierdo de la nueva sala
        else:
            jugador.rect.x = ancho_pantalla - jugador.rect.width

    # Eje Horizontal (Izquierda)
    elif jugador.rect.x < 0:
        if (sala_x, sala_y) == (-1, 0):
            guardia_permitido = any(isinstance(obj, Guardia) and obj.permitido for obj in interacciones_actuales)
            if guardia_permitido:
                sala_x = -2
                jugador.rect.x = ancho_pantalla - jugador.rect.width - 5
            else:
                jugador.rect.x = 0  # El guardia bloquea el paso al oeste
        else:
            siguiente = conexiones_mapa.get(((sala_x, sala_y), "izquierda"))
            if siguiente:
                sala_x, sala_y = siguiente
                jugador.rect.x = ancho_pantalla - jugador.rect.width - 5  # Aparece en el borde derecho
                
                # Si entramos a la sala del guardia (-1, 0), centramos verticalmente en el pasillo
                if (sala_x, sala_y) == (-1, 0):
                    jugador.rect.y = (alto_pantalla // 2) - (jugador.rect.height // 2)
            else:
                jugador.rect.x = 0

    # Eje Vertical (Abajo)
    if jugador.rect.y > alto_pantalla - jugador.rect.height:
        siguiente = conexiones_mapa.get(((sala_x, sala_y), "abajo"))
        if siguiente:
            sala_x, sala_y = siguiente
            jugador.rect.y = 5  # Aparece arriba en la nueva sala
        else:
            jugador.rect.y = alto_pantalla - jugador.rect.height

    # Eje Vertical (Arriba)
    elif jugador.rect.y < 0:
        siguiente = conexiones_mapa.get(((sala_x, sala_y), "arriba"))
        if siguiente:
            sala_x, sala_y = siguiente
            jugador.rect.y = alto_pantalla - jugador.rect.height - 5  # Aparece abajo en la nueva sala
        else:
            jugador.rect.y = 0
    # --- ACTUALIZAR LA CONFIGURACIÓN DEL JUEGO EN CADA SALA ---
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
    
    # --- CONFIGURACIÓN DE VICTORIA Y REINICIO DEL JUEGO ---
    if juego_ganado:
        texto_sombra = fuente_victoria.render("¡HAS GANADO EL JUEGO!", True, (0, 0, 0))
        pantalla.blit(texto_sombra, (ancho_pantalla // 2 - texto_sombra.get_width() // 2 + 3, 203))
        texto_v = fuente_victoria.render("¡HAS GANADO EL JUEGO!", True, (255, 215, 0))
        pantalla.blit(texto_v, (ancho_pantalla // 2 - texto_v.get_width() // 2, 200))
        texto_r = fuente.render("Presiona [R] para reiniciar la aventura", True, (200, 200, 200))
        pantalla.blit(texto_r, (ancho_pantalla // 2 - texto_r.get_width() // 2, 270))
    # --- ACTUALIZAR LOS CAMBIOS EN LA PANTALLA ---
    pygame.display.flip()
    reloj.tick(FPS)
# --- CIERRE LIMPIO DEL JUEGO ---
pygame.quit()
sys.exit()