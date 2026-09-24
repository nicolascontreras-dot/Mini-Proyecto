from pathlib import Path
import pygame
import sys

pygame.init()

reloj = pygame.time.Clock()
FPS = 60

ancho_pantalla = 1360
alto_pantalla = 820
tamaño_pantalla = (ancho_pantalla, alto_pantalla)

pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Mi Novela Interactiva")

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

# ---------------------------------------------------------
# ZONA DE CARGA DE RECURSOS (Imágenes, Fuentes, Sonidos)
# ---------------------------------------------------------
# Ejemplo de cómo cargar un fondo (asegúrate de tener la carpeta "images"):
# fondo_inicio = pygame.image.load(CARPETA_IMAGENES / "fondo.png").convert()
# fondo_inicio = pygame.transform.scale(fondo_inicio, tamaño_pantalla)

# ---------------------------------------------------------
# ZONA DE CLASES Y FUNCIONES
# ---------------------------------------------------------
# Clase opcional para manejar los estados del juego (menú, historia, etc.)
class JuegoManager:
    def __init__(self):
        self.estado = "menu"  # Puede ser "menu", "jugando", "opciones", etc. Pero se refiere al estado inicial.

# Instancias principales
manager = JuegoManager()

# ---------------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO (Game Loop)
# ---------------------------------------------------------
encendido = True

while encendido:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encendido = False

        # Si planeas usar el mouse para las opciones de la novela interactiva:
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                pos_mouse = pygame.mouse.get_pos()
                # Aquí puedes verificar si el mouse hizo clic en algún botón
                print(f"Clic en posición: {pos_mouse}")

    # 1. LÓGICA Y ACTUALIZACIÓN DE ESTADOS
    # (Actualizar textos, variables de la historia, posiciones, etc.)

    # 2. RENDERIZADO / DIBUJADO EN PANTALLA
    # Limpiar pantalla con un color base (ej. negro)
    pantalla.fill((30, 30, 30))

    # Dibujar elementos gráficos aquí (fondos, textos, botones)
    # pantalla.blit(fondo_inicio, (0, 0))

    # Actualizar la pantalla completa
    pygame.display.flip()

    # Controlar los fotogramas por segundo (FPS)
    reloj.tick(FPS)

# Cierre seguro de Pygame y el sistema
pygame.quit()
sys.exit()