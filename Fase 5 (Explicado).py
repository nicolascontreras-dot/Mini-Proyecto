# Obstáculos y Sistema de Colisiones
#===================================
# --- Breve Explicación ---
# Pygame facilita el sistema de coliciones comprobando automáticamente si dos rectángulo intentan
# superponerse a través del método colliderect()

import pygame
import sys

# Paso 1. Inicialización de Pygame
pygame.init()

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

# Paso 19. Crear obstáculos
# --- CLASE PARED / OBSTÁCULOS ---
class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = (120, 120, 120)        #Gris Piedra
        
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
# --- Breve Explicación ---
# Se utiliza la notación dx, dy para determinar un cambio en las coordenadas x e y
# esto facilita el movimiento fluido y que el personaje no se atasque en las esquinas
# de los obstáculos    
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
    
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color, self.rect)

# Paso 15. Creación del Objeto jugador a partir de la Clase
jugador = Jugador(ancho_pantalla//2 - 20, alto_pantalla//2 - 20)
  
# Paso 10. Sistemas de Mapas / Salas
# Coordenadas del mundo (0,0) es la sala incial
sala_x = 0
sala_y = 0

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

# Paso 5. Bucle Principal del Juego (Game Loop)
encendido = True
while encendido:
    # --- Captura de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:      #Si el usuario hace clic en la "X" de la pantalla
            encendido = False
    
    # --- Actualización de Lógica ---
    # (Aquí irá el movimiento del personaje, acciones, ataques, movimiento del enemigo, IA del enemigo, etc.)
    # Paso 22. Obtener las paredes de la sala actual (o lista vacía si no hay configuradas)
    obstaculos_actuales = salas_paredes.get((sala_x,sala_y),[])
    
    # Paso 7. Captura del Teclado
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
    jugador.mover(teclas, obstaculos_actuales)
    
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
        
    # Paso 8. Dibuja al Jugador (Posición X, Posición Y, Ancho, Alto)
    # Paso 18. Actualiza el Dibujo del Jugador
    #pygame.draw.rect(pantalla,jugador_color,(jugador_x,jugador_y,jugador_tamaño,jugador_tamaño))
    jugador.dibujar(pantalla)
    
    # Actualiza lo que se ve en la pantalla
    pygame.display.flip()
    # Controla que el juego corra a 60 FPS
    reloj.tick(FPS)
# Cierra el programa limpiamente
pygame.quit()
sys.exit()