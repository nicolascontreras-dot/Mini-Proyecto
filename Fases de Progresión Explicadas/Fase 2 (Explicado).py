# El Jugador y Movimiento Top-Down
#=================================
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
jugador_x = ancho_pantalla//2
jugador_y = alto_pantalla//2
jugador_tamaño = 40
jugador_velocidad = 5
jugador_color = (0, 200, 100)       #Verde

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
    
    # --- Renderizado / Dibujo ---
    pantalla.fill((30,30,30))       #Limpia la pantalla dibujando un fondo gris oscuro (R G B)
    
    # Paso 8. Dibuja al Jugador (Posición X, Posición Y, Ancho, Alto)
    pygame.draw.rect(pantalla,jugador_color,(jugador_x,jugador_y,jugador_tamaño,jugador_tamaño))
    
    # Actualiza lo que se ve en la pantalla
    pygame.display.flip()
    # Controla que el juego corra a 60 FPS
    reloj.tick(FPS)
# Cierra el programa limpiamente
pygame.quit()
sys.exit()