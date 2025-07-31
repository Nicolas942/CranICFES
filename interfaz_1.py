import pygame
import sys

# Inicializar Pygame
pygame.init()

# Colores
negro = (0,0,0)
blanco = (255,255,255)
Celeste	= (135, 206, 250)

# imagenes

boton_ajustes = pygame.image.load("img/AJUSTES.png")
boton_ajustes = pygame.transform.scale(boton_ajustes, (200,50))
boton_jugar = pygame.image.load("img/JUGAR.png")
boton_jugar = pygame.transform.scale(boton_jugar, (200,50))
boton_creditos = pygame.image.load("img/CREDITOS.png")
boton_creditos = pygame.transform.scale(boton_creditos, (200,50))
logo_juego = pygame.image.load("img/logo_juego.png")

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

    ventana.blit(boton_ajustes, (220,580))
    ventana.blit(boton_jugar, (550,580))
    ventana.blit(boton_creditos, (880,580))
    ventana.blit(logo_juego, (400,50))

    # Obtener tamaño actual de ventana
    ancho_actual, alto_actual = ventana.get_size()


    pygame.display.flip()

pygame.quit()
sys.exit()