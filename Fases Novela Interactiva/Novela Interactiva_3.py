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
pygame.display.set_caption("Novela Interactiva")

# Rutas de archivos
CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

# Fuentes de texto (conservadas para pantallas secundarias como ayuda o juego)
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

# Imagen de fondo para el Menú Principal (puedes cambiar el nombre del archivo según prefieras)
imagen_menu = pygame.image.load(CARPETA_IMAGENES / "menu_fondo.png").convert_alpha()
imagen_menu = pygame.transform.scale(imagen_menu, tamaño_pantalla)

# Transición del Acto I al Fondo de los Hermanos
imagen_transicion_acto1 = pygame.image.load(CARPETA_IMAGENES / "acto1_transicion.png").convert_alpha()
imagen_transicion_acto1 = pygame.transform.scale(imagen_transicion_acto1, tamaño_pantalla)

# Fondo del Acto I (con los dos hermanos) y cuadro de diálogo inferior
imagen_fondo_hermanos = pygame.image.load(CARPETA_IMAGENES / "fondo_hermanos.png").convert_alpha()
imagen_fondo_hermanos = pygame.transform.scale(imagen_fondo_hermanos, tamaño_pantalla)

imagen_caja_dialogo = pygame.image.load(CARPETA_IMAGENES / "caja_dialogo.png").convert_alpha()
# Opcional: Ajusta el tamaño de tu cuadro de texto si lo necesitas
imagen_caja_dialogo = pygame.transform.scale_by(imagen_caja_dialogo, 0.35)
ancho_caja_dialogo = imagen_caja_dialogo.get_width() + 500
alto_caja_dialogo = imagen_caja_dialogo.get_height()
imagen_caja_dialogo = pygame.transform.scale(imagen_caja_dialogo,(ancho_caja_dialogo, alto_caja_dialogo))

# Carga de recursos para la Pantalla de Ayuda
imagen_fondo_ayuda = pygame.image.load(CARPETA_IMAGENES / "fondo_ayuda.png").convert_alpha()
imagen_fondo_ayuda = pygame.transform.scale(imagen_fondo_ayuda, tamaño_pantalla)

imagen_cuadro_texto = pygame.image.load(CARPETA_IMAGENES / "cuadro_texto_ayuda.png").convert_alpha()
# Opcional: Ajusta el tamaño de tu cuadro de texto si lo necesitas
imagen_cuadro_texto = pygame.transform.scale_by(imagen_cuadro_texto, 0.45)

# Configuración común para los botones del menú
ancho_b, alto_b = 300, 70
centro_x = ancho_pantalla // 2 - ancho_b // 2

# Botón Comenzar
boton_comenzar_normal = pygame.image.load(CARPETA_IMAGENES / "boton_comenzar_1.png").convert_alpha()
boton_comenzar_hover = pygame.image.load(CARPETA_IMAGENES / "boton_comenzar_2.png").convert_alpha()
# Opcional: Ajustarles el tamaño si lo necesitas
boton_comenzar_normal = pygame.transform.scale(boton_comenzar_normal, (ancho_b, alto_b))
boton_comenzar_hover = pygame.transform.scale(boton_comenzar_hover, (ancho_b, alto_b))
# Obtener su rectángulo a partir de una de ellas para la posición
rectangulo_comenzar = boton_comenzar_normal.get_rect(topleft=(centro_x, 390))

# Botón Ayuda
boton_ayuda_normal = pygame.image.load(CARPETA_IMAGENES / "boton_ayuda_1.png").convert_alpha()
boton_ayuda_hover = pygame.image.load(CARPETA_IMAGENES / "boton_ayuda_2.png").convert_alpha()
# Opcional: Ajustarles el tamaño si lo necesitas
boton_ayuda_normal = pygame.transform.scale(boton_ayuda_normal, (ancho_b, alto_b))
boton_ayuda_hover = pygame.transform.scale(boton_ayuda_hover, (ancho_b, alto_b))
# Obtener su rectángulo a partir de una de ellas para la posición
rectangulo_ayuda = boton_ayuda_normal.get_rect(topleft=(centro_x, 500))

# Botón Salir
boton_salir_normal = pygame.image.load(CARPETA_IMAGENES / "boton_salir_1.png").convert_alpha()
boton_salir_hover = pygame.image.load(CARPETA_IMAGENES / "boton_salir_2.png").convert_alpha()
# Opcional: Ajustarles el tamaño si lo necesitas
boton_salir_normal = pygame.transform.scale(boton_salir_normal, (ancho_b, alto_b))
boton_salir_hover = pygame.transform.scale(boton_salir_hover, (ancho_b, alto_b))
# Obtener su rectángulo a partir de una de ellas para la posición
rectangulo_salir = boton_salir_normal.get_rect(topleft=(centro_x, 610))

def dibujar_texto_multilineas(superficie, texto, fuente, color, rect_limite, espaciado=6):
    """
    Divide un texto largo para que encaje automáticamente dentro del ancho 
    de un rectángulo (rect_limite), bajando de línea cuando es necesario.
    """
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    # Márgenes internos para que el texto no toque los bordes de la caja de diálogo
    margen_izquierdo = 150
    margen_derecho = 70
    margen_superior = 55

    ancho_maximo = rect_limite.width - (margen_izquierdo + margen_derecho)

    # 1. Organizar las palabras en líneas que quepan en el ancho disponible de la caja
    for palabra in palabras:
        prueba_linea = linea_actual + palabra + " "
        ancho_prueba, alto_prueba = fuente.size(prueba_linea)
        
        if ancho_prueba <= ancho_maximo:
            linea_actual = prueba_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    lineas.append(linea_actual)

    # 2. Dibujar cada línea respetando el margen superior e izquierdo de la caja
    y_actual = rect_limite.top + margen_superior
    for linea in lineas:
        superficie_texto = fuente.render(linea, True, color)
        superficie.blit(superficie_texto, (rect_limite.left + margen_izquierdo, y_actual))
        y_actual += alto_prueba + espaciado

# ---------------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO
# ---------------------------------------------------------
encendido = True

while encendido:
    # 1. GESTIÓN DE EVENTOS
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
                    if rectangulo_comenzar.collidepoint(pos_mouse):
                        estado_juego = "transicion_acto_1"  # Aquí puedes cambiar a tu lógica de juego/mapas

                    elif rectangulo_ayuda.collidepoint(pos_mouse):
                        estado_juego = "ayuda"

                    elif rectangulo_salir.collidepoint(pos_mouse):
                        encendido = False
                        
                elif estado_juego == "transicion_acto_1":
                    # Como el texto está en la imagen, cualquier clic avanza al Acto I
                    estado_juego = "acto_1"
                    
                elif estado_juego == "ayuda":
                    # Si estamos en ayuda, un clic nos regresa al menú principal
                    estado_juego = "menu"
                    
                elif estado_juego == "acto_1":
                    # Espacio para avanzar los diálogos de los hermanos en el futuro
                    pass
    # 2. RENDERIZADO / DIBUJADO SEGÚN EL ESTADO ACTUAL
    pantalla.fill((20, 20, 30))  # Fondo base oscuro

    if estado_juego == "portada":
        # 1. Dibujar la imagen de portada ocupando toda la pantalla
        pantalla.blit(imagen_portada, (0, 0))

        # 3. Dibujar la imagen de instrucción ("Haz clic para continuar")
        rect_instruccion = imagen_instruccion.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 + 300))
        pantalla.blit(imagen_instruccion, rect_instruccion)

    elif estado_juego == "menu":
        # Se dibuja la imagen de fondo del menú principal (sin texto de título)
        pantalla.blit(imagen_menu, (0, 0))

        posicion_mouse = pygame.mouse.get_pos()

        # Botón Comenzar con efecto visual al pasar el mouse
        if rectangulo_comenzar.collidepoint(posicion_mouse):
            pantalla.blit(boton_comenzar_hover, rectangulo_comenzar.topleft)
        else:
            pantalla.blit(boton_comenzar_normal, rectangulo_comenzar.topleft)

        # Botón Ayuda con efecto visual al pasar el mouse
        if rectangulo_ayuda.collidepoint(posicion_mouse):
            pantalla.blit(boton_ayuda_hover, rectangulo_ayuda.topleft)
        else:
            pantalla.blit(boton_ayuda_normal, rectangulo_ayuda.topleft)

        # Botón Salir con efecto visual al pasar el mouse
        if rectangulo_salir.collidepoint(posicion_mouse):
            pantalla.blit(boton_salir_hover, rectangulo_salir.topleft)
        else:
            pantalla.blit(boton_salir_normal, rectangulo_salir.topleft)

    elif estado_juego == "transicion_acto_1":
        # Se dibuja únicamente la imagen de fondo que ya contiene el texto integrado
        pantalla.blit(imagen_transicion_acto1, (0, 0))

    elif estado_juego == "acto_1":
        # 1. Fondo con los dos hermanos
        pantalla.blit(imagen_fondo_hermanos, (0, 0))

        # 2. Caja de diálogo inferior (ya escalada previamente en tus recursos)
        rect_caja_dialogo = imagen_caja_dialogo.get_rect(center=(ancho_pantalla // 2, alto_pantalla - 130))
        pantalla.blit(imagen_caja_dialogo, rect_caja_dialogo)

        # 3. Texto largo de prueba que se ajustará automáticamente a los límites de la caja
        dialogo_actual = "Hermano, recuerda que no debemos confiar en los guardias del cruce. Si nos atrapan aquí, todo lo que hemos construido se perderá en un instante."
        
        # 4. Dibujar el texto multilínea adaptado al cuadro
        dibujar_texto_multilineas(pantalla, dialogo_actual, fuente_mediana, (0, 0, 0), rect_caja_dialogo)
             
    elif estado_juego == "ayuda":
        # 1. Dibujar el fondo de la pantalla de ayuda
        pantalla.blit(imagen_fondo_ayuda, (0, 0))

        # 2. Dibujar el cuadro de texto con la explicación (centrado en la pantalla)
        rect_cuadro_texto = imagen_cuadro_texto.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2 + 160))
        pantalla.blit(imagen_cuadro_texto, rect_cuadro_texto)

    elif estado_juego == "jugando":
        # Aquí puedes colocar la lógica de tu novela o mapa cuando el usuario presione "Comenzar"
        texto_jugando = fuente_grande.render("¡El juego ha comenzado!", True, (255, 255, 255))
        pantalla.blit(texto_jugando, texto_jugando.get_rect(center=(ancho_pantalla // 2, alto_pantalla // 2)))

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
sys.exit()