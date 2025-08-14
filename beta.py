import pygame
import sys

pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CELESTE = (135, 206, 250)
ROJO = (255, 0, 0)

# Pantalla
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CranICFES")

# Carga de imágenes con optimización
def cargar_img(ruta, tamaño=None):
    img = pygame.image.load(ruta).convert_alpha()
    if tamaño:
        img = pygame.transform.scale(img, tamaño)
    return img

boton_ajustes = cargar_img("img/AJUSTES.png", (200, 50))
boton_ajustes_hover = cargar_img("img/AJUSTES.png", (220, 55))

boton_jugar = cargar_img("img/JUGAR.png", (200, 50))
boton_jugar_hover = cargar_img("img/JUGAR.png", (220, 55))

boton_creditos = cargar_img("img/CREDITOS.png", (200, 50))
boton_creditos_hover = cargar_img("img/CREDITOS.png", (220, 55))

circulo = cargar_img("img/circulo.jpg", (50, 50))
logo_juego = cargar_img("img/logo_juego.png")
fondo = cargar_img("img/FONDO.png")

# Posiciones de botones
pos_ajustes = (220, 580)
rect_ajustes = boton_ajustes.get_rect(topleft=pos_ajustes)
rect_ajustes_hover = boton_ajustes_hover.get_rect(center=rect_ajustes.center)

pos_jugar = (550, 580)
rect_jugar = boton_jugar.get_rect(topleft=pos_jugar)
rect_jugar_hover = boton_jugar_hover.get_rect(center=rect_jugar.center)

pos_creditos = (880, 580)
rect_creditos = boton_creditos.get_rect(topleft=pos_creditos)
rect_creditos_hover = boton_creditos_hover.get_rect(center=rect_creditos.center)

# Clase de jugador/equipo
class Equipo1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(ROJO)
        self.rect = self.image.get_rect(topleft=(x,y))

equipo1 = Equipo1(170, 520)
grupo_equipo_1 = pygame.sprite.Group(equipo1)

# Pantalla inicial
pantalla_actual = "menu"

corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()
    boton_salir = pygame.Rect(ventana.get_width() - 60, 10, 50, 50) 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
        elif evento.type == pygame.VIDEORESIZE:
            ventana = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if pantalla_actual in ["ajustes", "creditos", "jugar"] and boton_salir.collidepoint(mouse_pos):
                pantalla_actual = "menu"
            elif pantalla_actual == "menu":
                if rect_ajustes.collidepoint(mouse_pos):
                    pantalla_actual = "ajustes"
                elif rect_jugar.collidepoint(mouse_pos):
                    pantalla_actual = "jugar"
                elif rect_creditos.collidepoint(mouse_pos):
                    pantalla_actual = "creditos"

    # Renderizado según la pantalla
    if pantalla_actual == "menu":
        ventana.blit(fondo, (-50, -150))

        # Dibujar botones con hover
        ventana.blit(boton_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else boton_ajustes, rect_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else rect_ajustes)
        ventana.blit(boton_jugar_hover if rect_jugar.collidepoint(mouse_pos) else boton_jugar, rect_jugar_hover if rect_jugar.collidepoint(mouse_pos) else rect_jugar)
        ventana.blit(boton_creditos_hover if rect_creditos.collidepoint(mouse_pos) else boton_creditos, rect_creditos_hover if rect_creditos.collidepoint(mouse_pos) else rect_creditos)

        ventana.blit(logo_juego, (400, 40))

    elif pantalla_actual == "ajustes":
        ventana.fill((200, 200, 255))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("Pantalla de Ajustes", True, NEGRO)
        ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, ventana.get_height() // 2 - 30))
        pygame.draw.rect(ventana, ROJO, boton_salir)

    elif pantalla_actual == "jugar":
        ventana.fill((255, 255, 200))
        ventana.blit(circulo, (150, 500))
        grupo_equipo_1.update()
        grupo_equipo_1.draw(ventana)
        pygame.draw.rect(ventana, ROJO, boton_salir)

    elif pantalla_actual == "creditos":
        ventana.fill((255, 255, 200))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("Créditos", True, NEGRO)
        ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, ventana.get_height() // 2 - 30))
        pygame.draw.rect(ventana, ROJO, boton_salir)

    pygame.display.flip()

pygame.quit()
sys.exit()


