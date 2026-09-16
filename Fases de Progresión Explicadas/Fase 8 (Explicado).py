# NPCs y diálogos
#================
import pygame
import sys

# Paso 1. Inicialización de Pygame
pygame.init()

# Paso 25. Inicialización del sistema de fuentes/texto
pygame.font.init()

# Paso 2. Configuración de la pantalla
ancho_pantalla = 1280
alto_pantalla = 720
pantalla = pygame.display.set_mode((ancho_pantalla,alto_pantalla))

# Paso 3. Asignación del nombre de la pantalla
pygame.display.set_caption("Mi Juego de Aventura")

# Paso 4. Control de fotogramas por segundo (FPS)
reloj = pygame.time.Clock()
FPS = 60

# Paso 6. Propiedades del Jugador

# Paso 9. Actualizar las propiedades
#jugador_x = ancho_pantalla//2
#jugador_y = alto_pantalla//2

# Paso 14. Migrar las propiedades a la Clase
#jugador_tamaño = 40
#jugador_x = ancho_pantalla//2 - jugador_tamaño//2       #Actualizado
#jugador_y = alto_pantalla//2 - jugador_tamaño//2        #Actualizado
#jugador_velocidad = 6       #Actualizado
#jugador_color = (0, 200, 100)       #Verde

# Paso 26. Configurar fuente para renderizar texto en pantalla
fuente = pygame.font.SysFont("arial", 22, bold=True)

# Paso 35. Crear sistema de diálogos
# --- SISTEMA DE DIÁLOGOS ---
class SistemaDialogo:
    def __init__(self):
        self.activo = False
        self.texto_actual = ""
        self.nombre_hablante = ""
        #Rectángulo para la caja de texto en la parte inferior (X, Y, ancho, alto)
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
        # Dibujar fondo semitransparente oscuro
        # Creamos una superficie (surface) especial para poder aplicarle la transparencia (alpha)
        caja_superficie = pygame.Surface((self.caja_rect.width,self.caja_rect.height))
        caja_superficie.set_alpha(200)      # 0 es transparente, 255 es sólido
        caja_superficie.fill((20, 20, 20))
        superficie.blit(caja_superficie, (self.caja_rect.x, self.caja_rect.y))
        
        # Borde blanco
        pygame.draw.rect(superficie,(255, 255, 255),self.caja_rect, 3)
        
        # Renderizar nombre (Amarillo)
        texto_nombre = fuente.render(self.nombre_hablante + ":", True, (255, 200, 0))
        superficie.blit(texto_nombre, (self.caja_rect.x + 20, self.caja_rect.y +15))
        
        # Renderizar texto principal (Blanco)
        texto_dialogo = fuente.render(self.texto_actual, True, (255, 255, 255))
        superficie.blit(texto_dialogo, (self.caja_rect.x + 20, self.caja_rect.y + 50))
        
        # Indicador de cerrar
        texto_cerrar = fuente.render("[E] para cerrar", True, (150, 150, 150))
        superficie.blit(texto_cerrar, (self.caja_rect.x + self.caja_rect.width - 150, self.caja_rect.y + self.caja_rect.height - 30))

# Paso 36. Crear al Personaje No Jugador (NPC)
class NPC:
    def __init__(self, x, y, nombre, linea_dialogo, color):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.nombre = nombre
        self.dialogo = linea_dialogo
        self.color = color
    
    # Paso 47. Actualizar la interacción del NPC
    def interactuar(self, inventario):
        return self.nombre, self.dialogo
    
    def dibujar(self,superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 50)        

# Paso 19. Crear obstáculos
# --- CLASE PARED / OBSTÁCULOS ---
class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = (120, 120, 120)        #Gris Piedra
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

# Paso 27. Crear interacciones adicionales
# --- CLASE COFRE ---
class Cofre:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.abierto = False
        self.color_cerrado = (150, 90, 30)      #Madera / Marrón
        self.color_abierto = (220, 180, 50)     #Oro / Amarillo
    
    # Paso 46. Actualizamos el método interactuar para el inventario
    def interactuar(self, inventario):
        if not self.abierto:
            self.abierto = True
            inventario.agregar("Moneda de Oro")     # Se guarda el objeto
            return "Sistema", "¡Abriste un cofre y obtuviste una Moneda de Oro!"
        return "Sistema", "El cofre ya está vacío."
    
    def dibujar(self, superficie):
        color = self.color_abierto if self.abierto else self.color_cerrado
        pygame.draw.rect(superficie, color, self.rect)

# --- CLASE CUEVA/PUERTA ---
class Cueva:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.color = (10, 10, 10)      #Entrada oscura
    # Paso 48. Actualizar la interacción de la cueva
    def interactuar(self, inventario):
        return "Sistema", "Entraste a la cueva misteriosa..."
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)
        
# --- CLASE JUGADOR ---
class Jugador:
    def __init__(self, x, y):
        self.tamaño = 40
        # pygame.Rect guarda (X, Y, ancho, alto)
        self.rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        self.velocidad = 6
        self.color = (0, 200, 100)

# Paso 20. Actualizar el Movimiento
    def mover(self, teclas, obstaculos):
        dx = 0      #Define cuánto se quiere desplazar el personaje en la horizontal
        dy = 0      #Define cuánto se quiere desplazar el personaje en la vertical
               
        if teclas[pygame.K_LEFT]:
            dx -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            dx += self.velocidad
        if teclas[pygame.K_UP]:
            dy -= self.velocidad
        if teclas[pygame.K_DOWN]:
            dy += self.velocidad

        # --- Movimiento y colisión en eje X ---
        self.rect.x += dx
        for pared in obstaculos:
            if self.rect.colliderect(pared.rect):
                if dx > 0:      #Moviéndose a la derecha -> pegar al lado izquierd del objeto
                    self.rect.right = pared.rect.left
                if dx < 0:      #Moviéndose a la izquierda -> pegar al lado derecho del objeto
                    self.rect.left = pared.rect.right
        
        # --- Movimiento y colisión en eje Y ---
        self.rect.y += dy
        for pared in obstaculos:
            if self.rect.colliderect(pared.rect):
                if dy > 0:      #Moviéndose hacia abajo -> pegar al borde superior del objeto
                    self.rect.bottom = pared.rect.top
                if dy < 0:      #Moviéndose hacia arriba -> pegar al borde inferior del objeto
                    self.rect.top = pared.rect.bottom
    
    # Paso 28. Implementar el método de interacción
    def obtener_zona_interaccion(self):
        # Crea un área ligeramente más grande alrededor del jugador para detectar cercanía
        return self.rect.inflate(30,30)
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

# Paso 45. Implementación de un inventario
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
            
        # Fondo del inventario
        pygame.draw.rect(superficie, (40, 40, 50), self.rect)
        pygame.draw.rect(superficie, (200, 200, 200), self.rect, 2)
        
        # Título
        texto_titulo = fuente.render("INVENTARIO", True, (255, 255, 255))
        superficie.blit(texto_titulo, (self.rect.x + 10, self.rect.y + 10))
        
        # Dibujar los objetos
        y_offset = 50
        if len(self.objetos) == 0:
            texto_vacio = fuente.render("(Vacío)", True, (150, 150, 150))
            superficie.blit(texto_vacio, (self.rect.x + 10, self.rect.y + y_offset))
        else:
            for item in self.objetos:
                texto_item = fuente.render("- " + item, True, (200, 255, 200))
                superficie.blit(texto_item, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 30
 
# Paso 15. Creación del Objeto jugador a partir de la Clase
jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)

# Paso 37. Creación del Objeto sistema de diálogo
sistema_dialogo = SistemaDialogo()

# Paso 10. Sistemas de Mapas / Salas
# Coordenadas del mundo (0,0) es la sala incial
sala_x = 0
sala_y = 0

# Paso 29. Crear diccionario de objetos interactivos por sala
salas_interacciones = {
    #Paso 38. Integramos un NPC para probar la interacción
    (-1,0) : [
        NPC(0, alto_pantalla//2 - 50, "Guardián", "No puedes seguir avanzando.",(150, 150, 250))
        ],
    (0,-1) : [
        Cofre(400, 300),
        Cueva(200, 200)
        ],
    (0,1) : [
        Cofre(200, 200)
        ]
}
# Paso 11. Colores solo para diferenciar las salas en la matriz
# usa el formato de diccionario (coordenada) : (color)
salas_colores = {
    (0,0):(30,30,30),   #Centro (Gris)
    (1,0):(50,20,20),   #Este (Rojo)
    (-1,0):(20,50,20),  #Oeste (Verde)
    (0,1):(20,20,50),   #Sur (Azul)
    (0,-1):(50,50,20),  #Norte (Amarillo)
}

# Paso 21. Crear el diccionario de las paredes por sala
salas_paredes = {
    # Sala inicial (0,0) : Dos rocas/estructuras en el centro
    (0,0) : [
        Pared(300, 200, 150, 100),
        Pared(800, 400, 200, 150)
        ],
    # Sala Este (1,0) : Una gran estructura central
    (1,0) : [
        Pared(500, 150, 280, 420)
    ],
    # Sala Oeste (-1,0) : Un pasillo estrecho
    (-1,0) : [
        Pared(0, 0, 1280, 150),     #Pared superior
        Pared(0, 570, 1280, 150)    #Pared inferior
    ]
}

# Paso 30. Controlar los mensaje y el tiempo
# Paso 39. Eliminamos el control de tiempo y mensaje dentro y fuera del bucle
#mensaje_pantalla = ""
#tiempo_mensaje = 0

# Paso 49. Crear el inventario
inventario_jugador = Inventario()

# Paso 5. Bucle Principal del Juego (Game Loop)
encendido = True
while encendido:
    obstaculos_actuales = salas_paredes.get((sala_x, sala_y), [])
    interacciones_actuales = salas_interacciones.get((sala_x,sala_y), [])
    # Paso 40. Crear una lista que combine los NPCs con las paredes
    lista_colisiones = list(obstaculos_actuales)
    for obj in interacciones_actuales:
        if isinstance(obj,NPC):
            class ParedTemporal:
                def __init__(self, rect):
                    self.rect = rect
            lista_colisiones.append(ParedTemporal(obj.rect))
            
    # Paso 31. Implementar mensaje e interacciones
    # Paso 39. Eliminamos el control de tiempo y mensaje dentro y fuera del bucle
    # Restar tiempo al mensaje activo
    #if tiempo_mensaje > 0:
    #    tiempo_mensaje -= 1
    #else:
    #    mensaje_pantalla = ""
    
    # --- Captura de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:      #Si el usuario hace clic en la "X" de la pantalla
            encendido = False
        # Paso 32. Implementar la tecla de interacción
        # Interactuar con la tecla_e
        elif evento.type == pygame.KEYDOWN:
            # Paso 50. Actualizar la revisión de teclas
            if evento.key == pygame.K_i:
                inventario_jugador.alternar()     # Abre y cierra con la "I"
                
            elif evento.key == pygame.K_e:
                # Paso 41. Actualizamos para implementar la caja de diálogo
                if sistema_dialogo.activo:
                    sistema_dialogo.cerrar()        # Si está abierta, la 'E' la cierra
                else:
                    zona_jugador = jugador.obtener_zona_interaccion()
                    for objeto in interacciones_actuales:
                        if zona_jugador.colliderect(objeto.rect):
                            nombre, texto = objeto.interactuar(inventario_jugador)      # Actualizado
                            sistema_dialogo.iniciar(nombre, texto)        #Abrimos el diálogo
                            break
    
    # --- Actualización de Lógica ---
    # (Aquí irá el movimiento del personaje, acciones, ataques, movimiento del enemigo, IA del enemigo, etc.)
    # Paso 22. Obtener las paredes de la sala actual (o lista vacía si no hay configuradas)
    #obstaculos_actuales = salas_paredes.get((sala_x,sala_y),[])
    
    # Paso 7. Captura del Teclado
    # Paso 42. Actualizar el movimiento solo cuando no esté el diálogo
    if not sistema_dialogo.activo:
        teclas = pygame.key.get_pressed()
    
    # Paso 16. Migrar el movimiento a la clase
    #if teclas[pygame.K_LEFT]:
    #    jugador_x -= jugador_velocidad
    #if teclas[pygame.K_RIGHT]:
    #    jugador_x += jugador_velocidad
    #if teclas[pygame.K_UP]:
    #    jugador_y -= jugador_velocidad
    #if teclas[pygame.K_DOWN]:
    #    jugador_y += jugador_velocidad
    
    # Paso 23. Actualizar el Movimiento 
        jugador.mover(teclas, lista_colisiones)      #Actualizado
    
    # Paso 12. Transición de Salas por Borde
    # Paso 17. Actualizar la Transición
    # Borde Derecho -> Ir al Este
    if jugador.rect.x > ancho_pantalla: 
        sala_x += 1
        jugador.rect.x = 0
    # Borde Izquierdo -> Ir al Oeste
    elif jugador.rect.x < -jugador.tamaño:    #Actualizado
        sala_x -= 1
        jugador.rect.x = ancho_pantalla - jugador.tamaño
    # Borde Inferior -> Ir al Sur
    if jugador.rect.y > alto_pantalla:
        sala_y += 1
        jugador.rect.y = 0
    # Borde Superior -> Ir al Norte
    elif jugador.rect.y < -jugador.tamaño:
        sala_y -= 1
        jugador.rect.y = alto_pantalla - jugador.tamaño
    
    # --- Renderizado / Dibujo ---
    # Paso 13. Actualizar el Renderizado
    # Busca el color según la sala actual; si no existe en la lista, usa fondo negro
    fondo_color = salas_colores.get((sala_x,sala_y),(10,10,10)) 
    #pantalla.fill((30,30,30))       #Limpia la pantalla dibujando un fondo gris oscuro (R G B)
    pantalla.fill(fondo_color)      #Actualizado
    
    # Paso 24. Dibujar los obstáculos de las sala
    for pared in obstaculos_actuales:
        pared.dibujar(pantalla)

    # Paso 33. Dibujar Objetos Interactivos
    zona_jugador = jugador.obtener_zona_interaccion()
    for objeto in interacciones_actuales:
        objeto.dibujar(pantalla)
        # Si el jugador está cerca aparecerá el texto "(E)" flotante
        # Paso 43. Actualizar para implementar el Sistema de Diálogo
        if not sistema_dialogo.activo and zona_jugador.colliderect(objeto.rect):        #Actualizado
            texto_e = fuente.render("[E]", True, (255, 255, 255))
            pantalla.blit(texto_e,(objeto.rect.x + 5, objeto.rect.y - 25))
            
    # Paso 8. Dibuja al Jugador (Posición X, Posición Y, Ancho, Alto)
    # Paso 18. Actualiza el Dibujo del Jugador
    #pygame.draw.rect(pantalla,jugador_color,(jugador_x,jugador_y,jugador_tamaño,jugador_tamaño))
    jugador.dibujar(pantalla)
    
    # Paso 34. Dibujar mensaje de Interacció en pantalla si existe
    # Paso 44. Eliminar para implementar el Sistema de Diálogos
    #if mensaje_pantalla:
    #    texto_renderizado = fuente.render(mensaje_pantalla, True, (255, 255, 0))
    #    pantalla.blit(texto_renderizado, (ancho_pantalla//2 - texto_renderizado.get_width()//2, 50))
    sistema_dialogo.dibujar(pantalla)       #Actualizado
    
    # Paso 51. Mostrar el inventario en pantalla
    inventario_jugador.dibujar(pantalla)
    
    # Actualiza lo que se ve en la pantalla
    pygame.display.flip()
    
    # Controla que el juego corra a 60 FPS
    reloj.tick(FPS)
    
# Cierra el programa limpiamente
pygame.quit()
sys.exit()