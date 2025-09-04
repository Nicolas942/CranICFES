import pygame
import sys
from base_de_datos import obtener_pregunta_aleatoria

pygame.init()

# === Colores (definidos directamente en el diccionario) ===
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# === Mapa de materias a colores (CORREGIDO según tu indicación) ===
materias = {
    "Matematicas": (255, 0, 0),        # Rojo
    "Español": (255, 255, 0),          # Amarillo
    "Lectura Critica": (255, 165, 0),  # Naranja
    "Naturales": (0, 128, 0),          # Verde
    "Sociales": (0, 0, 255),           # Azul
    "Ingles": (128, 0, 128)            # Morado
}

# === Audio ===
pygame.mixer.init()
try:
    sonido_fondo = pygame.mixer.Sound("Sonidos/Fondo.mp3")
    pygame.mixer.Sound.play(sonido_fondo, loops=-1)
    musica_activa = True
except pygame.error:
    print("⚠️  No se pudo cargar el sonido de fondo")
    musica_activa = False

# === Ventana ===
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CranICFES")

def cargar_img(ruta, tamaño=None):
    try:
        img = pygame.image.load(ruta).convert_alpha()
        if tamaño:
            img = pygame.transform.scale(img, tamaño)
        return img
    except pygame.error as e:
        print(f"⚠️  No se pudo cargar la imagen: {ruta}")
        img = pygame.Surface(tamaño or (100, 50))
        img.fill((200, 0, 0))
        return img

# === Cargar imágenes ===
logo_juego = cargar_img("img/logo_juego.png")
fondo = cargar_img("img/FONDO.png")
tablero = cargar_img("img/tablero1.png", (1366, 720))

# === Botones menú ===
boton_ajustes = cargar_img("img/AJUSTES.png", (200, 50))
boton_ajustes_hover = cargar_img("img/AJUSTES.png", (220, 55))
boton_jugar = cargar_img("img/JUGAR.png", (200, 50))
boton_jugar_hover = cargar_img("img/JUGAR.png", (220, 55))
boton_creditos = cargar_img("img/CREDITOS.png", (200, 50))
boton_creditos_hover = cargar_img("img/CREDITOS.png", (220, 55))

# === Botones música ===
boton_mute = cargar_img("img/mute.png", (200, 50))
boton_mute_hover = cargar_img("img/mute.png", (220, 55))
boton_unmute = cargar_img("img/unmute.png", (200, 50))
boton_unmute_hover = cargar_img("img/unmute.png", (220, 55))
boton_vol_up = cargar_img("img/vol_up.png", (200, 50))
boton_vol_up_hover = cargar_img("img/vol_up.png", (220, 55))
boton_vol_down = cargar_img("img/vol_down.png", (200, 50))
boton_vol_down_hover = cargar_img("img/vol_down.png", (220, 55))

# === Posiciones menú ===
rect_ajustes = boton_ajustes.get_rect(topleft=(220, 580))
rect_jugar = boton_jugar.get_rect(topleft=(550, 580))
rect_creditos = boton_creditos.get_rect(topleft=(880, 580))

# === Música botones ===
x_columna = 50
y_columna = 200
espacio = 70
rect_mute = boton_mute.get_rect(topleft=(x_columna, y_columna))
rect_unmute = boton_unmute.get_rect(topleft=(x_columna, y_columna))
rect_vol_up = boton_vol_up.get_rect(topleft=(x_columna, y_columna + espacio))
rect_vol_down = boton_vol_down.get_rect(topleft=(x_columna, y_columna + espacio * 2))

# === Círculos por materia (posición, radio, materia) ===
circulos = [
    {"centro": (510, 90), "radio": 50, "materia": "Matematicas"},
    {"centro": (385, 175), "radio": 40, "materia": "Sociales"},
    {"centro": (325, 265), "radio": 40, "materia": "Ingles"},
    {"centro": (650, 200), "radio": 40, "materia": "Naturales"},
    {"centro": (720, 300), "radio": 40, "materia": "Español"},
    {"centro": (580, 350), "radio": 40, "materia": "Lectura Critica"}
]

# === Sprite del equipo ===
class Equipo1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 0, 0))  # Rojo brillante
        self.rect = self.image.get_rect(topleft=(x, y))

equipo1 = Equipo1(510, 90)
grupo_equipo_1 = pygame.sprite.Group(equipo1)

# === Estado del juego ===
pantalla_actual = "menu"
mostrando_pregunta = False
pregunta_data = None
botones_opciones = []

# === Fuentes ===
fuente_pregunta = pygame.font.SysFont("Arial", 36, bold=True)
fuente_opciones = pygame.font.SysFont("Arial", 30)
fuente_ayuda = pygame.font.SysFont("Arial", 24)

# === Bucle principal ===
corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()
    boton_salir = pygame.Rect(ventana.get_width() - 70, 20, 40, 40)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if mostrando_pregunta:
                    mostrando_pregunta = False
                else:
                    corriendo = False
        elif evento.type == pygame.VIDEORESIZE:
            ventana = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if pantalla_actual in ["ajustes", "creditos", "jugar"] and boton_salir.collidepoint(mouse_pos):
                pantalla_actual = "menu"
                mostrando_pregunta = False
            elif pantalla_actual == "menu":
                if rect_ajustes.collidepoint(mouse_pos):
                    pantalla_actual = "ajustes"
                elif rect_jugar.collidepoint(mouse_pos):
                    pantalla_actual = "jugar"
                elif rect_creditos.collidepoint(mouse_pos):
                    pantalla_actual = "creditos"
            elif pantalla_actual == "ajustes":
                if musica_activa and rect_mute.collidepoint(mouse_pos):
                    if 'sonido_fondo' in locals():
                        pygame.mixer.Sound.stop(sonido_fondo)
                    musica_activa = False
                elif (not musica_activa) and rect_unmute.collidepoint(mouse_pos):
                    if 'sonido_fondo' in locals():
                        pygame.mixer.Sound.play(sonido_fondo, loops=-1)
                    musica_activa = True
                elif rect_vol_up.collidepoint(mouse_pos):
                    if 'sonido_fondo' in locals():
                        vol = sonido_fondo.get_volume()
                        sonido_fondo.set_volume(min(1.0, vol + 0.1))
                elif rect_vol_down.collidepoint(mouse_pos):
                    if 'sonido_fondo' in locals():
                        vol = sonido_fondo.get_volume()
                        sonido_fondo.set_volume(max(0.0, vol - 0.1))

            # === Jugar: clic en círculo → pregunta de esa materia ===
            elif pantalla_actual == "jugar" and not mostrando_pregunta:
                for circ in circulos:
                    centro = circ["centro"]
                    radio = circ["radio"]
                    distancia = ((mouse_pos[0] - centro[0])**2 + (mouse_pos[1] - centro[1])**2)**0.5
                    if distancia <= radio:
                        materia = circ["materia"]
                        pregunta_data = obtener_pregunta_aleatoria(materia)
                        if pregunta_data:  # ✅ Corregido: ahora es completo
                            mostrando_pregunta = True
                            botones_opciones = []
                        break

            # === Responder pregunta ===
            elif mostrando_pregunta:
                for i, rect_boton in enumerate(botones_opciones):
                    if rect_boton.collidepoint(mouse_pos):
                        if i == pregunta_data["correcta"]:
                            print(f"✅ ¡Correcto! Materia: {pregunta_data['materia']}")
                            # Opcional: mover equipo al círculo
                            equipo1.rect.center = circ["centro"]  # Asigna el circ actual
                        else:
                            print(f"❌ Incorrecto. La correcta era: {pregunta_data['opciones'][pregunta_data['correcta']]}")
                        mostrando_pregunta = False
                        break

    # === Renderizado ===
    if pantalla_actual == "menu":
        ventana.blit(fondo, (-50, -150))
        ventana.blit(boton_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else boton_ajustes, rect_ajustes.topleft)
        ventana.blit(boton_jugar_hover if rect_jugar.collidepoint(mouse_pos) else boton_jugar, rect_jugar.topleft)
        ventana.blit(boton_creditos_hover if rect_creditos.collidepoint(mouse_pos) else boton_creditos, rect_creditos.topleft)
        ventana.blit(logo_juego, (400, 40))

    elif pantalla_actual == "ajustes":
        ventana.blit(fondo, (-50, -150))
        titulo = pygame.font.SysFont(None, 60).render("AJUSTES", True, NEGRO)
        ventana.blit(titulo, (ventana.get_width() // 2 - titulo.get_width() // 2, 30))
        pygame.draw.rect(ventana, (255, 0, 0), boton_salir)
        if musica_activa:
            ventana.blit(boton_mute_hover if rect_mute.collidepoint(mouse_pos) else boton_mute, rect_mute.topleft)
        else:
            ventana.blit(boton_unmute_hover if rect_unmute.collidepoint(mouse_pos) else boton_unmute, rect_unmute.topleft)
        ventana.blit(boton_vol_up_hover if rect_vol_up.collidepoint(mouse_pos) else boton_vol_up, rect_vol_up.topleft)
        ventana.blit(boton_vol_down_hover if rect_vol_down.collidepoint(mouse_pos) else boton_vol_down, rect_vol_down.topleft)

    elif pantalla_actual == "jugar":
        ventana.blit(tablero, (0, 0))

        # Dibujar círculos por materia con colores correctos
        for circ in circulos:
            centro = circ["centro"]
            radio = circ["radio"]
            materia = circ["materia"]
            color = materias[materia]
            pygame.draw.circle(ventana, color, centro, radio)
            # Etiqueta pequeña con el nombre
            texto_materia = fuente_ayuda.render(materia, True, NEGRO)
            ventana.blit(texto_materia, (centro[0] - texto_materia.get_width() // 2, centro[1] - 8))

        grupo_equipo_1.update()
        grupo_equipo_1.draw(ventana)
        pygame.draw.rect(ventana, (255, 0, 0), boton_salir)

        # === Mostrar pregunta ===
        if mostrando_pregunta and pregunta_data:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))

            # Título de materia con color
            titulo_materia = fuente_pregunta.render(f"{pregunta_data['materia']}", True, materias[pregunta_data['materia']])
            ventana.blit(titulo_materia, (ANCHO // 2 - titulo_materia.get_width() // 2, 80))

            # Pregunta
            render_pregunta = fuente_pregunta.render(pregunta_data["pregunta"], True, BLANCO)
            rect_preg = render_pregunta.get_rect(center=(ANCHO // 2, 150))
            ventana.blit(render_pregunta, rect_preg)

            # Opciones
            y_opcion = 220
            botones_opciones.clear()
            for i, opcion in enumerate(pregunta_data["opciones"]):
                texto = fuente_opciones.render(f"{i+1}. {opcion}", True, BLANCO)
                rect_boton = texto.get_rect(center=(ANCHO // 2, y_opcion))
                ventana.blit(texto, rect_boton)
                botones_opciones.append(rect_boton)
                y_opcion += 50

            mensaje = fuente_ayuda.render("Haz clic en tu opción", True, (0, 200, 255))
            ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, y_opcion + 30))

    elif pantalla_actual == "creditos":
        ventana.blit(fondo, (-50, -150))
        texto = pygame.font.SysFont(None, 60).render("Créditos", True, NEGRO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 30))
        pygame.draw.rect(ventana, (255, 0, 0), boton_salir)

    pygame.display.flip()

pygame.quit()
sys.exit()