from pathlib import Path
import pygame, sys
pygame.init()
reloj=pygame.time.Clock()

ancho=1080
alto=810
tamaño_ventana=(ancho,alto)
pantalla=pygame.display.set_mode((tamaño_ventana))
#pantalla.fill((0,0,0))
#pygame.display.flip()
pygame.display.set_caption("CANDERE")

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "images"

fondo_inicio=pygame.image.load(CARPETA_IMAGENES/"pantallainicio.png").convert_alpha()
fondo_inicio=pygame.transform.scale(fondo_inicio,tamaño_ventana)

#pieza=pygame.image.load(cimagenes/"pieza.png").convert()
#pieza=pygame.transform.scale(pieza,tamaño_ventana)

ojo=pygame.image.load(CARPETA_IMAGENES/"cursor3.png")
ojo=pygame.transform.scale_by(ojo,10)

ojox=800
ojoy=200
ojorec=ojo.get_rect()
ojorec.topleft=(ojox,ojoy)

pygame.mouse.set_visible(False)

#puerta=pygame.rect(10,30,100,300)

obst=[]
obst.append(ojorec)
#obst.append(puerta)

encendido=True
velocidad=3
while encendido:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            encendido=False
            
        if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    pos_mouse=event.pos
                    print(f"Clic en la posicion:{pos_mouse}")
                    
    ojorec.center=pygame.mouse.get_pos()
            
    pantalla.blit(fondo_inicio,(0,0))
    pantalla.blit(ojo,ojorec)
    pygame.display.flip()
    reloj.tick(60)
pygame.quit()