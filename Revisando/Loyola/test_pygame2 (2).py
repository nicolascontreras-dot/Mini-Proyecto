from pathlib import Path
import pygame
import sys

pygame.init()
reloj = pygame.time.Clock()

ancho = 1080
alto = 810
tamaño_ventana = (ancho, alto)
pantalla = pygame.display.set_mode(tamaño_ventana)
pygame.display.set_caption("CANDERE")

cproyecto = Path(__file__).parent
cimagenes = cproyecto / "images"

# Cargar recursos
fondo_inicio = pygame.image.load(cimagenes / "pantallainicio.png")
fondo_inicio = pygame.transform.scale(fondo_inicio, tamaño_ventana)

señora = pygame.image.load(cimagenes / "señora.png")
señora = pygame.transform.scale_by(señora, 10)
señorax = 40
señoray = 40
señorarec = señora.get_rect()
señorarec.topleft = (señorax, señoray)

ojo = pygame.image.load(cimagenes / "cursor3.png")
ojo = pygame.transform.scale_by(ojo, 10)
ojorec = ojo.get_rect()

# Ocultar el cursor normal del sistema operativo para que solo se vea el ojo (opcional pero recomendado)
pygame.mouse.set_visible(False)

encendido = True
velocidad = 3

while encendido:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            encendido = False
            
        # Ejemplo de cómo podrías detectar clics en el futuro para revisar los 4 lugares
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic izquierdo del mouse
                pos_mouse = event.pos
                print(f"Clic en la posición: {pos_mouse}")
                # Aquí puedes verificar si pos_mouse colisiona con la ventana, cama, escritorio o puerta

    # 1. ACTUALIZAR POSICIÓN DEL CURSOR CON EL MOUSE
    # El centro del rectángulo del ojo ahora sigue exactamente la posición del cursor del mouse
    ojorec.center = pygame.mouse.get_pos()

    # 2. CONTROL DE LA SEÑORA (Movimiento por teclado conservado para pruebas)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_d]:
        señorarec.x += velocidad
    if teclas[pygame.K_a]:
        señorarec.x -= velocidad
    if teclas[pygame.K_w]:
        señorarec.y -= velocidad
    if teclas[pygame.K_s]:
        señorarec.y += velocidad
    # Corrección aplicada aquí (uso de += en lugar de =)
    if teclas[pygame.K_DOWN]:
        señorarec.y += velocidad
    if teclas[pygame.K_UP]:
        señorarec.y -= velocidad
    if teclas[pygame.K_RIGHT]:
        señorarec.x += velocidad
    if teclas[pygame.K_LEFT]:
        señorarec.x -= velocidad

    # 3. DIBUJAR EN PANTALLA
    pantalla.blit(fondo_inicio, (0, 0))
    pantalla.blit(señora, señorarec)
    pantalla.blit(ojo, ojorec)
    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()