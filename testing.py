import pygame
import sys

pygame.init()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# === Audio ===
pygame.mixer.init()
sonido_fondo = pygame.mixer.Sound("Sonidos/Fondo.mp3")
pygame.mixer.Sound.play(sonido_fondo, loops=-1)
musica_activa = True 

# === Ventana ===
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CranICFES")

def cargar_img(ruta, tamaño=None):
    img = pygame.image.load(ruta).convert_alpha()
    if tamaño:
        img = pygame.transform.scale(img, tamaño)
    return img

# === Botones menú principal ===
boton_ajustes = cargar_img("img/AJUSTES.png", (200, 50))
boton_ajustes_hover = cargar_img("img/AJUSTES.png", (220, 55))

boton_jugar = cargar_img("img/JUGAR.png", (200, 50))
boton_jugar_hover = cargar_img("img/JUGAR.png", (220, 55))

boton_creditos = cargar_img("img/CREDITOS.png", (200, 50))
boton_creditos_hover = cargar_img("img/CREDITOS.png", (220, 55))

# === Botones de música (mismo estilo que los del menú) ===
boton_mute = cargar_img("img/mute.png", (200, 50))
boton_mute_hover = cargar_img("img/mute.png", (220, 55))

boton_unmute = cargar_img("img/unmute.png", (200, 50))
boton_unmute_hover = cargar_img("img/unmute.png", (220, 55))

boton_vol_up = cargar_img("img/vol_up.png", (200, 50))
boton_vol_up_hover = cargar_img("img/vol_up.png", (220, 55))

boton_vol_down = cargar_img("img/vol_down.png", (200, 50))
boton_vol_down_hover = cargar_img("img/vol_down.png", (220, 55))

circulo = cargar_img("img/circulo.jpg", (50, 50))
logo_juego = cargar_img("img/logo_juego.png")
fondo = cargar_img("img/FONDO.png")

tablero = cargar_img("img/tablero1.png",(1366,720))

# === Posiciones menú principal ===
pos_ajustes = (220, 580)
rect_ajustes = boton_ajustes.get_rect(topleft=pos_ajustes)
rect_ajustes_hover = boton_ajustes_hover.get_rect(center=rect_ajustes.center)

pos_jugar = (550, 580)
rect_jugar = boton_jugar.get_rect(topleft=pos_jugar)
rect_jugar_hover = boton_jugar_hover.get_rect(center=rect_jugar.center)

pos_creditos = (880, 580)
rect_creditos = boton_creditos.get_rect(topleft=pos_creditos)
rect_creditos_hover = boton_creditos_hover.get_rect(center=rect_creditos.center)

# === Posiciones botones música en columna izquierda ===
x_columna = 50
y_columna = 200
espacio = 70

pos_mute = (x_columna, y_columna)
pos_unmute = (x_columna, y_columna)   # misma posición para intercambiar
pos_vol_up = (x_columna, y_columna + espacio)
pos_vol_down = (x_columna, y_columna + espacio*2)

rect_mute = boton_mute.get_rect(topleft=pos_mute)
rect_unmute = boton_unmute.get_rect(topleft=pos_unmute)
rect_vol_up = boton_vol_up.get_rect(topleft=pos_vol_up)
rect_vol_down = boton_vol_down.get_rect(topleft=pos_vol_down)

# === Sprite de ejemplo ===
class Equipo1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

equipo1 = Equipo1(510,90)
grupo_equipo_1 = pygame.sprite.Group(equipo1)

pantalla_actual = "menu"
pregunta_mostrada = False  # ✅ Nueva variable de control

corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()
    boton_salir = pygame.Rect(ventana.get_width() - 70, 20, 40, 40)

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
                pregunta_mostrada = False  # ✅ Se resetea al salir
            elif pantalla_actual == "menu":
                if rect_ajustes.collidepoint(mouse_pos):
                    pantalla_actual = "ajustes"
                elif rect_jugar.collidepoint(mouse_pos):
                    pantalla_actual = "jugar"
                elif rect_creditos.collidepoint(mouse_pos):
                    pantalla_actual = "creditos"
            elif pantalla_actual == "ajustes":
                if musica_activa and rect_mute.collidepoint(mouse_pos):
                    pygame.mixer.Sound.stop(sonido_fondo)
                    musica_activa = False
                elif (not musica_activa) and rect_unmute.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(sonido_fondo, loops=-1)
                    musica_activa = True
                elif rect_vol_up.collidepoint(mouse_pos):
                    vol = sonido_fondo.get_volume()
                    sonido_fondo.set_volume(min(1.0, vol + 0.1))
                elif rect_vol_down.collidepoint(mouse_pos):
                    vol = sonido_fondo.get_volume()
                    sonido_fondo.set_volume(max(0.0, vol - 0.1))

    # === Dibujar pantallas ===
    if pantalla_actual == "menu":
        ventana.blit(fondo, (-50, -150))
        ventana.blit(boton_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else boton_ajustes,
                     rect_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else rect_ajustes)
        ventana.blit(boton_jugar_hover if rect_jugar.collidepoint(mouse_pos) else boton_jugar,
                     rect_jugar_hover if rect_jugar.collidepoint(mouse_pos) else rect_jugar)
        ventana.blit(boton_creditos_hover if rect_creditos.collidepoint(mouse_pos) else boton_creditos,
                     rect_creditos_hover if rect_creditos.collidepoint(mouse_pos) else rect_creditos)
        ventana.blit(logo_juego, (400, 40))

    elif pantalla_actual == "ajustes":
        ventana.blit(fondo, (-50, -150))

        font_titulo = pygame.font.SysFont(None, 60)
        texto_titulo = font_titulo.render("AJUSTES", True, NEGRO)
        ventana.blit(texto_titulo, (ventana.get_width() // 2 - texto_titulo.get_width() // 2, 30))

        pygame.draw.rect(ventana, (255, 0, 0), boton_salir)

        if musica_activa:
            ventana.blit(boton_mute_hover if rect_mute.collidepoint(mouse_pos) else boton_mute, rect_mute.topleft)
        else:
            ventana.blit(boton_unmute_hover if rect_unmute.collidepoint(mouse_pos) else boton_unmute, rect_unmute.topleft)

        ventana.blit(boton_vol_up_hover if rect_vol_up.collidepoint(mouse_pos) else boton_vol_up, rect_vol_up.topleft)
        ventana.blit(boton_vol_down_hover if rect_vol_down.collidepoint(mouse_pos) else boton_vol_down, rect_vol_down.topleft)

    elif pantalla_actual == "jugar":
        from base_de_datos import respuesta_multiple, coleccion
        import random
        circulo= pygame.draw.circle(ventana, NEGRO, (510,90),50)
        ventana.blit(tablero, (0,0))
        grupo_equipo_1.update()
        grupo_equipo_1.draw(ventana)
        pygame.draw.rect(ventana, (255, 0, 0), boton_salir)
        if equipo1.rect.colliderect(circulo) and not pregunta_mostrada:  # ✅ Solo una vez
            documento_aleatorio = random.choice(list(coleccion.find()))
            respuesta_multiple(documento_aleatorio)
            pregunta_mostrada = True  # ✅ Bloquea nuevas preguntas

    elif pantalla_actual == "creditos":
        ventana.blit(fondo, (-50, -150))
        font = pygame.font.SysFont(None, 60)
        texto = font.render("Créditos", True, NEGRO)
        ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2, ventana.get_height() // 2 - 30))
        pygame.draw.rect(ventana, (255, 0, 0), boton_salir)

    pygame.display.flip()

pygame.quit()
sys.exit()
