# Migrando nuestro Jugador a una Clase
#=====================================
# --- Breve Explicación ---
# Una Clase funciona como un molde, es una plantilla donde se definen los atributos
# que serían las características y comportamientos de algo. Por ejemplo, el "molde"
# de un Jugador establece que tiene posición, velocidad, vidas, movimiento, etc.

# Un Objeto funciona como una galleta, es el resultado de utilizar la Clase. Se pueden
# crear muchos objetos a partir de la misma Clase (molde) y cada uno tendría su propia
# posición, velocidad, vida, movimiento, etc.

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

# --- CLASE JUGADOR ---
class Jugador:
    def __init__(self, x, y):
        self.tamaño = 40
        # pygame.Rect guarda (X, Y, ancho, alto)
        self.rect = pygame.Rect(x, y, self.tamaño, self.tamaño)
        self.velocidad = 6
        self.color = (0, 200, 100)
    
    def mover(self, teclas):       
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.rect.y += self.velocidad
    
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

# Paso 5. Bucle Principal del Juego (Game Loop)
encendido = True
while encendido:
    # --- Captura de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:      #Si el usuario hace clic en la "X" de la pantalla
            encendido = False
    
    # --- Actualización de Lógica ---
    # (Aquí irá el movimiento del personaje, acciones, ataques, movimiento del enemigo, IA del enemigo, etc.)
    
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
    jugador.mover(teclas)
    
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