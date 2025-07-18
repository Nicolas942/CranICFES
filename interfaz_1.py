import pygame
import sys

# Inicializar Pygame
pygame.init()

# Colores
negro = (0,0,0)
blanco = (255,255,255)
Celeste	= (135, 206, 250)

# tamaño de pantalla
info = pygame.display.Info()
ancho = info.current_w
alto = info.current_h

# ventana maximizada con opción de redimensionar
ventana = pygame.display.set_mode((ancho, alto), pygame.RESIZABLE)
pygame.display.set_caption("CranICFES")


# Bucle principal
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
        elif evento.type == pygame.VIDEORESIZE:
            # Actualizar tamaño si el usuario redimensiona
            pantalla = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
            
    # Dibujar fondo 
    ventana.fill((Celeste))

    # Obtener tamaño actual de ventana
    ancho_actual, alto_actual = ventana.get_size()


    pygame.display.flip()

pygame.quit()
sys.exit()