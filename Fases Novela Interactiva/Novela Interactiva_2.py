from pathlib import Path
import pygame
import sys

# Inicialización de Pygame
pygame.init()

reloj = pygame.time.Clock()
FPS = 60

# Configuración de la ventana
ancho_pantalla = 1360
alto_pantalla = 820
tamaño_pantalla = (ancho_pantalla, alto_pantalla)

pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Novela Interactiva - Portada y Menú")

# Rutas de archivos
CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

# Fuentes de texto
fuente_grande = pygame.font.Font(None, 80)
fuente_mediana = pygame.font.Font(None, 50)

# ---------------------------------------------------------
# ESTADOS DEL JUEGO
# ---------------------------------------------------------
# "portada" -> Pantalla inicial que pide clic del mouse
# "menu"    -> Menú principal con las opciones
# "jugando" -> La novela interactiva en sí
# "ayuda"   -> Pantalla de ayuda
estado_juego = "portada"

# --- CARGA DE RECURSOS DE PORTADA ---
imagen_portada = pygame.image.load(CARPETA_IMAGENES / "portada.png").convert_alpha()
imagen_portada = pygame.transform.scale(imagen_portada, tamaño_pantalla)
# Cargar la imagen del texto o botón de instrucción
imagen_instruccion = pygame.image.load(CARPETA_IMAGENES / "texto_continuar.png").convert_alpha()

# Opcional: Si necesitas cambiarle el tamaño
imagen_instruccion = pygame.transform.scale_by(imagen_instruccion, 0.2)

# ---------------------------------------------------------
# CREACIÓN DE RECTÁNGULOS PARA LOS BOTONES DEL MENÚ
# ---------------------------------------------------------
# Definimos el tamaño y posición de los botones en la pantalla
ancho_boton = 300
alto_boton = 70
centro_x = ancho_pantalla // 2 - ancho_boton // 2

boton_comenzar = pygame.Rect(centro_x, 320, ancho_boton, alto_boton)
boton_ayuda = pygame.Rect(centro_x, 430, ancho_boton, alto_boton)
boton_salir = pygame.Rect(centro_x, 540, ancho_boton, alto_boton)

# Bucle Principal del Juego
encendido = True

while encendido:
    # -----------------------------------------------------
    # 1. GESTIÓN DE EVENTOS
    # -----------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encendido = False

        # Detección de clics del mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo del mouse
                pos_mouse = pygame.mouse.get_pos()

                if estado_juego == "portada":
                    # Al hacer clic en cualquier parte de la portada, pasamos al menú
                    estado_juego = "menu"

                elif estado_juego == "menu":
                    # Verificamos si se hizo clic en alguno de los botones
                    if boton_comenzar.collidepoint(pos_mouse):
                        print("¡Iniciando juego!")
                        estado_juego = "jugando"  # Aquí puedes cambiar a tu lógica de juego/mapas

                    elif boton_ayuda.collidepoint(pos_mouse):
                        print("Abriendo ayuda...")
                        estado_juego = "ayuda"

                    elif boton_salir.collidepoint(pos_mouse):
                        encendido = False

                elif estado_juego == "ayuda":
                    # Si estamos en ayuda, un clic nos regresa al menú principal
                    estado_juego = "menu"

    # -----------------------------------------------------
    # 2. RENDERIZADO / DIBUJADO SEGÚN EL ESTADO ACTUAL
    # -----------------------------------------------------
    pantalla.fill((20, 20, 30))  # Fondo base oscuro

    if estado_juego == "portada":
        # 1. Dibujar la imagen de portada ocupando toda la pantalla
        pantalla.blit(imagen_portada, (0, 0))

        # 2. Título principal como texto (opcional)
        texto_portada = fuente_grande.render("Bienvenido a la Novela", True, (255, 255, 255))
        rect_portada = texto_portada.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 - 100))
        pantalla.blit(texto_portada, rect_portada)

        # 3. Dibujar la imagen de instrucción ("Haz clic para continuar")
        rect_instruccion = imagen_instruccion.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 + 300))
        pantalla.blit(imagen_instruccion, rect_instruccion)

    elif estado_juego == "menu":
        # Título del Menú
        titulo_menu = fuente_grande.render("MENÚ PRINCIPAL", True, (255, 255, 255))
        rect_titulo = titulo_menu.get_rect(center=(ancho_pantalla // 2, 180))
        pantalla.blit(titulo_menu, rect_titulo)

        # Dibujar Botones (Cambiando de color si el mouse pasa por encima)
        pos_mouse = pygame.mouse.get_pos()

        # Botón Comenzar
        color_comenzar = (70, 130, 180) if boton_comenzar.collidepoint(pos_mouse) else (50, 90, 130)
        pygame.draw.rect(pantalla, color_comenzar, boton_comenzar, border_radius=10)
        texto_c = fuente_mediana.render("Comenzar", True, (255, 255, 255))
        pantalla.blit(texto_c, texto_c.get_rect(center=boton_comenzar.center))

        # Botón Ayuda
        color_ayuda = (70, 130, 180) if boton_ayuda.collidepoint(pos_mouse) else (50, 90, 130)
        pygame.draw.rect(pantalla, color_ayuda, boton_ayuda, border_radius=10)
        texto_a = fuente_mediana.render("Ayuda", True, (255, 255, 255))
        pantalla.blit(texto_a, texto_a.get_rect(center=boton_ayuda.center))

        # Botón Salir
        color_salir = (180, 70, 70) if boton_salir.collidepoint(pos_mouse) else (130, 50, 50)
        pygame.draw.rect(pantalla, color_salir, boton_salir, border_radius=10)
        texto_s = fuente_mediana.render("Salir", True, (255, 255, 255))
        pantalla.blit(texto_s, texto_s.get_rect(center=boton_salir.center))

    elif estado_juego == "ayuda":
        # Pantalla de Ayuda
        texto_ayuda_titulo = fuente_grande.render("AYUDA", True, (255, 255, 255))
        texto_ayuda_desc = fuente_mediana.render("Usa el mouse para hacer click en las opciones.", True, (200, 200, 200))
        texto_volver = fuente_mediana.render("Haz click en cualquier parte para volver", True, (100, 200, 255))

        pantalla.blit(texto_ayuda_titulo, texto_ayuda_titulo.get_rect(center=(ancho_pantalla // 2, 250)))
        pantalla.blit(texto_ayuda_desc, texto_ayuda_desc.get_rect(center=(ancho_pantalla // 2, 380)))
        pantalla.blit(texto_volver, texto_volver.get_rect(center=(ancho_pantalla // 2, 500)))

    elif estado_juego == "jugando":
        # Aquí puedes colocar la lógica de tu novela o mapa cuando el usuario presione "Comenzar"
        texto_jugando = fuente_grande.render("¡El juego ha comenzado!", True, (255, 255, 255))
        pantalla.blit(texto_jugando, texto_jugando.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2)))

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()