# Final del juego y botón de reinicio
#====================================
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
# Paso 16. Creamos el NPC que nos ayudará a terminar el juego
# --- CLASE DEL PERSONAJE FINAL ---
class Principe:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 80)
        self.color = (240, 200, 50)  # Color dorado/real

    def interactuar(self, inventario):
        return "Príncipe", "¡Has traído la Reliquia Antigua! El reino está a salvo gracias a ti."

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 35)

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
# Paso 10. Creamos clase del NPC que actuará como guardia
# --- BREVE EXPLICACIÓN ---
# El NPC solo tiene un comportamiento fijo de mostrar mensaje, por otra parte el guardián
# estará condicionado y tendrá un diálogo dependiendo del estado del jugador, ya nos sirve la clase NPC
# para el "Guardia"
# --- CLASE DE NPC CONDICIONADO ---
class Guardia:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 80)
        self.color = (150, 150, 250)
        self.permitido = False

    def interactuar(self, inventario):
        if self.permitido:
            return "Guardián", "Puedes pasar. Alguien muy importante te espera más adelante."

        if "Reliquia" in inventario.objetos:
            self.permitido = True
            self.rect.y = 80  # Se desplaza hacia arriba despejando la puerta del oeste
            return "Guardián", "¡Es la Reliquia! Tienes permiso para avanzar hacia el Salón."
        else:
            return "Guardián", "No puedes pasar. Solo quienes posean la Reliquia tienen acceso."

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 30)
        
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

# Paso 8. Agregamos la clase que permita una transición a salas interiores
# --- CLASE ENTRADA/SALIDA CUEVA ---
class PuertaTeleport:
    def __init__(self, x, y, destino_sala, destino_pos, etiqueta="Entrada"):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.color = (10, 10, 10)
        self.destino_sala = destino_sala  # Tupla (x, y) de la sala destino
        self.destino_pos = destino_pos    # Tupla (x, y) de las coordenadas donde aparece el jugador
        self.etiqueta = etiqueta

    def interactuar(self, inventario):
        return "Sistema", f"Usaste la {self.etiqueta}..."

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

# Paso 9. Agregamos el objeto interactivo que está condicionado a tener un objeto en el inventario
# --- CLASE COFRE CON LLAVE ---
class CofreEspecial:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.abierto = False
        self.color_cerrado = (180, 50, 50)  # Color rojizo/especial
        self.color_abierto = (220, 180, 50)

    def interactuar(self, inventario):
        if self.abierto:
            return "Sistema", "El cofre ya está vacío."

        if "Llave" in inventario.objetos:
            inventario.objetos.remove("Llave")  # La llave se consume y desaparece
            inventario.agregar("Reliquia")
            self.abierto = True
            return "Sistema", "¡Usaste la Llave, abriste el cofre y encontraste la Reliquia Antigua!"
        else:
            return "Sistema", "El cofre está cerrado con candado. Necesitas una Llave para abrirlo."

    def dibujar(self, superficie):
        color = self.color_abierto if self.abierto else self.color_cerrado
        pygame.draw.rect(superficie, color, self.rect)
        
jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)
sistema_dialogo = SistemaDialogo()

sala_x = 0
sala_y = 0
# Paso 2. Integrar al mercader en el mapa a través de las salas
# Paso 5. Integramos al enemigo patrullando el mapa
# Paso 11. Reemplazamos el NPC de la sala Oeste para que se convierta en el Guardia
# Paso 17. Agrupamos la creación de salas en una función para permitir el reinicio del juego.
def crear_mapa():
    return {
    # Implementamos la sala con el personaje final
    (-2,0) : [
        Principe(600, 300)          #Actualizado
        ],
    (-1,0) : [
        Guardia(50, alto_pantalla//2 - 40)
        ],
    # Paso 12. Implementamos la entrada de la Cueva
    (0,-1) : [
        Cofre(400, 300),
        PuertaTeleport(200, 200, (0, -2), (640, 500), "Entrada a la Cueva")         #Actualizado
        ],
    # Paso 13. Creamos la sala del interior de la Cueva para implementar la salida
    (0,-2) : [
        CofreEspecial(620, 200),
        PuertaTeleport(610, 580, (0, -1), (200, 280), "Salida de la Cueva")
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
    
salas_interacciones = crear_mapa()
# Paso 18. Implementar el color de la sala final
salas_colores = {
    (0,0):(30,30,30),
    (1,0):(50,20,20),
    (-1,0):(20,50,20),
    (-2,0):(60,40,80),          #Actualizado (Salón Púrpura)
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

inventario_jugador = Inventario()

encendido = True

# Paso 19. Implementamos las variables que nos permitirán controlar el estado final del juego
# Variable de estado de victoria
juego_ganado = False
fuente_victoria = pygame.font.SysFont("arial", 48, bold=True)

while encendido:
    obstaculos_actuales = salas_paredes.get((sala_x, sala_y), [])
    interacciones_actuales = salas_interacciones.get((sala_x,sala_y), [])

    lista_colisiones = list(obstaculos_actuales)
    for obj in interacciones_actuales:
        # Paso 3. Incluir al mercader en la pared temporal para que no sea atravesado
        # Paso 14. Actualizar la pared temporal para incluir al guardia
        # Paso 20. Actualizar la pared temporal para incluir al personaje final
        if isinstance(obj, (NPC, Mercader, Guardia, Principe)):        #Actualizado
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
                            # Paso 15. Implementar el método para que el jugador entre a la cueva con la tecla [E]
                            if isinstance(objeto, PuertaTeleport):
                                sala_x, sala_y = objeto.destino_sala
                                jugador.rect.x, jugador.rect.y = objeto.destino_pos
                            # Paso 21. Implementar el método para que termine el juego despues de hablar con [E]
                            if isinstance(objeto, Principe):
                                juego_ganado = True
                            break
            # Paso 22. Agregar la detección de la tecla [R] para reiniciar
            elif evento.key == pygame.K_r:
                if juego_ganado:
                    juego_ganado = False
                    sala_x, sala_y = 0, 0
                    jugador.rect.x = ancho_pantalla // 2 - 20
                    jugador.rect.y = alto_pantalla // 2 - 20
                    inventario_jugador = Inventario()
                    salas_interacciones = crear_mapa()
                    sistema_dialogo.cerrar()           
                    
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
    # Paso 22. Dibujar el mensaje de victoria en la pantalla
    if juego_ganado:
        # Sombra del texto
        texto_sombra = fuente_victoria.render("¡HAS GANADO EL JUEGO!", True, (0, 0, 0))
        pantalla.blit(texto_sombra, (ancho_pantalla // 2 - texto_sombra.get_width() // 2 + 3, 203))

        # Texto principal en dorado
        texto_v = fuente_victoria.render("¡HAS GANADO EL JUEGO!", True, (255, 215, 0))
        pantalla.blit(texto_v, (ancho_pantalla // 2 - texto_v.get_width() // 2, 200))

        # Indicación de reinicio
        texto_r = fuente.render("Presiona [R] para reiniciar la aventura", True, (200, 200, 200))
        pantalla.blit(texto_r, (ancho_pantalla // 2 - texto_r.get_width() // 2, 270))
        
    pygame.display.flip()
    
    reloj.tick(FPS)
    
pygame.quit()

sys.exit()