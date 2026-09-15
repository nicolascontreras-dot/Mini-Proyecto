# Creando la estructura base (El Game Loop)
#==========================================
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

# Paso 5. Bucle Principal del Juego (Game Loop)
encendido = True
while encendido:
    # --- Captura de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:      #Si el usuario hace clic en la "X" de la pantalla
            encendido = False
    
    # --- Actualización de Lógica ---
    # (Aquí irá el movimiento del personaje, acciones, ataques, movimiento del enemigo, IA del enemigo, etc.)
    
    # --- Renderizado / Dibujo ---
    pantalla.fill((30,30,30))       #Limpia la pantalla dibujando un fondo gris oscuro (R G B)
    # Actualiza lo que se ve en la pantalla
    pygame.display.flip()
    # Controla que el juego corra a 60 FPS
    reloj.tick(FPS)
# Cierra el programa limpiamente
pygame.quit()
sys.exit()