# Mapas y Transición por Bordes
#==============================
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
jugador_tamaño = 40
jugador_x = ancho_pantalla//2 - jugador_tamaño//2       #Actualizado
jugador_y = alto_pantalla//2 - jugador_tamaño//2        #Actualizado
jugador_velocidad = 6       #Actualizado
jugador_color = (0, 200, 100)       #Verde

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
    
    if teclas[pygame.K_LEFT]:
        jugador_x -= jugador_velocidad
    if teclas[pygame.K_RIGHT]:
        jugador_x += jugador_velocidad
    if teclas[pygame.K_UP]:
        jugador_y -= jugador_velocidad
    if teclas[pygame.K_DOWN]:
        jugador_y += jugador_velocidad
    
    # Paso 12. Transición de Salas por Borde
    # Borde Derecho -> Ir al Este
    if jugador_x > ancho_pantalla:
        sala_x += 1
        jugador_x = 0
    # Borde Izquierdo -> Ir al Oeste
    elif jugador_x < -jugador_tamaño:
        sala_x -= 1
        jugador_x = ancho_pantalla - jugador_tamaño
    # Borde Inferior -> Ir al Sur
    if jugador_y > alto_pantalla:
        sala_y += 1
        jugador_y = 0
    # Borde Superior -> Ir al Norte
    elif jugador_y < -jugador_tamaño:
        sala_y -= 1
        jugador_y = alto_pantalla - jugador_tamaño
    
    # --- Renderizado / Dibujo ---
    # Paso 13. Actualizar el Renderizado
    # Busca el color según la sala actual; si no existe en la lista, usa fondo negro
    fondo_color = salas_colores.get((sala_x,sala_y),(10,10,10)) 
    #pantalla.fill((30,30,30))       #Limpia la pantalla dibujando un fondo gris oscuro (R G B)
    pantalla.fill(fondo_color)      #Actualizado
    
    # Paso 8. Dibuja al Jugador (Posición X, Posición Y, Ancho, Alto)
    pygame.draw.rect(pantalla,jugador_color,(jugador_x,jugador_y,jugador_tamaño,jugador_tamaño))
    
    # Actualiza lo que se ve en la pantalla
    pygame.display.flip()
    # Controla que el juego corra a 60 FPS
    reloj.tick(FPS)
# Cierra el programa limpiamente
pygame.quit()
sys.exit()