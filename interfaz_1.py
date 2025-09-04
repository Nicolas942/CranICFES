import pygame
import sys
import webbrowser 

pygame.init()


negro = (0, 0, 0)
blanco = (255, 255, 255)
Celeste = (135, 206, 250)
rojo = (255, 0, 0)


info = pygame.display.Info()
ancho = info.current_w
alto = info.current_h
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("CranICFES")

url_youtube = "https://www.youtube.com/watch?v=yNEpyU3PnDI"

boton_ajustes_img = pygame.image.load("img/AJUSTES.png")
boton_ajustes = pygame.transform.scale(boton_ajustes_img, (200, 50))
boton_ajustes_hover = pygame.transform.scale(boton_ajustes_img, (220, 55))

boton_jugar_img = pygame.image.load("img/JUGAR.png")
boton_jugar = pygame.transform.scale(boton_jugar_img, (200, 50))
boton_jugar_hover = pygame.transform.scale(boton_jugar_img, (220, 55))

boton_creditos_img = pygame.image.load("img/CREDITOS.png")
boton_creditos = pygame.transform.scale(boton_creditos_img, (200, 50))
boton_creditos_hover = pygame.transform.scale(boton_creditos_img, (220, 55))

boton_youtube = pygame.image.load("img/LOGO_YT.png")
boton_youtube = pygame.transform.scale(boton_youtube, (150,150))
boton_youtube_hover = pygame.transform.scale(boton_youtube, (200,200))

personaje_interfaz_img = pygame.image.load("img/MAGO_MTMC.png")
personaje_interfaz = pygame.transform.scale(personaje_interfaz_img, (250,250))
personaje_interfaz_hover = pygame.transform.scale(personaje_interfaz_img, (300,300))

boton_atras_img = pygame.image.load("img/BOTON_SALIR.png")  # Asegúrate de tener esta imagen
boton_atras = pygame.transform.scale(boton_atras_img, (50, 50))
boton_atras_hover = pygame.transform.scale(boton_atras_img, (60, 60))  # Un poco más grande en hover

circulo = pygame.image.load("img/circulo.jpg")
circulo = pygame.transform.scale(circulo, (50,50))

logo_juego = pygame.image.load("img/logo_juego.png")

fondo = pygame.image.load("img/FONDO.png")


pos_ajustes = (250, 580)
rect_ajustes = boton_ajustes.get_rect(topleft=pos_ajustes)
rect_ajustes_hover = boton_ajustes_hover.get_rect(center=rect_ajustes.center)

pos_jugar = (585, 580)
rect_jugar = boton_jugar.get_rect(topleft=pos_jugar)
rect_jugar_hover = boton_jugar_hover.get_rect(center=rect_jugar.center)

pos_creditos = (920, 580)
rect_creditos = boton_creditos.get_rect(topleft=pos_creditos)
rect_creditos_hover = boton_creditos_hover.get_rect(center=rect_creditos.center)

pos_youtube = (60, 300)
rect_youtube = boton_creditos.get_rect(topleft=pos_youtube)
rect_youtube_hover = boton_youtube_hover.get_rect(center=rect_youtube.center)

pos_mago = (1100, 220)
rect_mago = personaje_interfaz.get_rect(topleft=pos_mago)
rect_mago_hover = personaje_interfaz_hover.get_rect(center=rect_mago.center)

pos_atras = (ventana.get_width() - 70, 10)  # Posición: esquina superior derecha
rect_atras = boton_atras.get_rect(topleft=pos_atras)
rect_atras_hover = boton_atras_hover.get_rect(center=rect_atras.center)

pantalla_actual = "menu"

corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()
    pos_atras = (ventana.get_width() - 70, 10)
    rect_atras = boton_atras.get_rect(topleft=pos_atras)
    rect_atras_hover = boton_atras_hover.get_rect(center=rect_atras.center)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
        elif evento.type == pygame.VIDEORESIZE:
            ventana = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if pantalla_actual in ["ajustes", "creditos"] and rect_atras.collidepoint(mouse_pos):
                pantalla_actual = "menu"

            if pantalla_actual == "menu":
                if rect_ajustes.collidepoint(mouse_pos):
                    pantalla_actual = "ajustes"
                elif rect_jugar.collidepoint(mouse_pos):
                    pantalla_actual = "jugar"
                elif rect_creditos.collidepoint(mouse_pos):
                    pantalla_actual = "creditos"
                elif pantalla_actual == "menu" and rect_youtube.collidepoint(mouse_pos):
                    webbrowser.open(url_youtube)  # Abre el enlace en el navegador
                elif rect_mago.collidepoint(mouse_pos):
                    pantalla_actual = "mago"

    if pantalla_actual == "menu":
        ventana.blit(fondo, (-20,-150))

        if rect_ajustes.collidepoint(mouse_pos):
            ventana.blit(boton_ajustes_hover, rect_ajustes_hover)
        else:
            ventana.blit(boton_ajustes, rect_ajustes)

        if rect_jugar.collidepoint(mouse_pos):
            ventana.blit(boton_jugar_hover, rect_jugar_hover)
        else:
            ventana.blit(boton_jugar, rect_jugar)

        if rect_creditos.collidepoint(mouse_pos):
            ventana.blit(boton_creditos_hover, rect_creditos_hover)
        else:
            ventana.blit(boton_creditos, rect_creditos)

        if rect_youtube.collidepoint(mouse_pos):
            ventana.blit(boton_youtube_hover, rect_youtube_hover)
        else:
            ventana.blit(boton_youtube, rect_youtube)

        if rect_mago.collidepoint(mouse_pos):
            ventana.blit(personaje_interfaz_hover, rect_mago_hover)
        else:
            ventana.blit(personaje_interfaz, rect_mago)

        ventana.blit(logo_juego, (430, 40))

    elif pantalla_actual == "ajustes":
        ventana.fill((200, 200, 255))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("Pantalla de Ajustes", True, negro)
        ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, ventana.get_height() // 2 - 30))

        if rect_atras.collidepoint(mouse_pos):
            ventana.blit(boton_atras_hover, rect_atras_hover)
        else:
            ventana.blit(boton_atras, rect_atras)

    elif pantalla_actual == "jugar":
        ventana.fill((255, 255, 200))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("juego:)", True, negro)
        ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, ventana.get_height() // 2 - 30))
        ventana.blit(circulo, (150,500))

    elif pantalla_actual == "creditos":
        ventana.fill((255, 255, 200))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("Créditos", True, negro)
        ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, ventana.get_height() // 2 - 30))


    pygame.display.flip()

pygame.quit()
sys.exit()