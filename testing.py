import pygame
import sys
import webbrowser  
from base_de_datos import obtener_pregunta_aleatoria

pygame.init()

# === Colores ===
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CELESTE = (135, 206, 250)  

# === Mapa de materias a colores ===
materias = {
    "Matematicas": (255, 0, 0),        # Rojo
    "Español": (255, 255, 0),          # Amarillo
    "Naturales": (0, 128, 0),          # Verde
    "Sociales": (255, 165, 0),         # Naranja
    "Ingles": (128, 0, 128),           # Morado
    "Lectura Critica": (0, 0, 255)     # Azul
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
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
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

# === Cargar imágenes principales ===
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
boton_salir = cargar_img("img/boton_salir.png", (120, 100))  
boton_salir_hover = cargar_img("img/boton_salir.png", (140, 120))

# === Botones adicionales ===
url_youtube = "https://www.youtube.com/watch?v=yNEpyU3PnDI"  
boton_youtube = cargar_img("img/LOGO_YT.png", (150, 150))
boton_youtube_hover = cargar_img("img/LOGO_YT.png", (200, 200))
personaje_interfaz = cargar_img("img/MAGO_MTMC.png", (250, 250))
personaje_interfaz_hover = cargar_img("img/MAGO_MTMC.png", (300, 300))

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

# === Botones adicionales ===
rect_youtube = boton_youtube.get_rect(topleft=(60, 300))
rect_mago = personaje_interfaz.get_rect(topleft=(1100, 220))

# === Música botones ===
rect_mute = boton_mute.get_rect(topleft=(50, 200))
rect_unmute = boton_unmute.get_rect(topleft=(50, 200))
rect_vol_up = boton_vol_up.get_rect(topleft=(50,250))
rect_vol_down = boton_vol_down.get_rect(topleft=(50,300))

# === Círculos por materia (posición, radio, materia) ===
circulos = [
    {"centro": (510, 90), "radio": 50, "materia": "Matematicas"},
    {"centro": (385, 175), "radio": 40, "materia": "Sociales"},
    {"centro": (460, 565), "radio": 40, "materia": "Ingles"},
    {"centro": (365, 495), "radio": 40, "materia": "Naturales"},
    {"centro": (325, 265), "radio": 40, "materia": "Español"},
    {"centro": (785, 610), "radio": 40, "materia": "Sociales"},
    {"centro": (890, 560), "radio": 40, "materia": "Matematicas"},
]

# === Orden del recorrido ===
orden_antihorario = [
    "Matematicas",
    "Sociales",
    "Ingles",
    "Naturales",
    "Español",
    "Lectura Critica"
]

# === Sprite del equipo ===
class Equipo1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect(topleft=(x, y))

equipo1 = Equipo1(510, 90)
grupo_equipo_1 = pygame.sprite.Group(equipo1)

# === Estado del juego ===
pantalla_actual = "menu"
mostrando_pregunta = False
mostrando_retroalimentacion = False
mensaje_retro = ""
color_retro = BLANCO
pregunta_data = None
botones_opciones = []  
temporizador_retro = 0  

# === Fuentes ===
fuente_pregunta = pygame.font.SysFont("Arial", 36, bold=True)
fuente_opciones = pygame.font.SysFont("Arial", 30)
fuente_ayuda = pygame.font.SysFont("Arial", 24)

rect_boton_salir = None  

# === Bucle principal ===
corriendo = True
while corriendo:
    mouse_pos = pygame.mouse.get_pos()
    rect_boton_salir = None
    if pantalla_actual in ["ajustes", "creditos", "jugar", "mago"]:
        rect_boton_salir = pygame.Rect(ventana.get_width() - 150, 10, 120, 100)

    # === Eventos ===
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if mostrando_pregunta or mostrando_retroalimentacion:
                    mostrando_pregunta = False
                    mostrando_retroalimentacion = False
                else:
                    corriendo = False
        elif evento.type == pygame.VIDEORESIZE:
            ventana = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Botón de salir (atrás) en pantallas secundarias
            if rect_boton_salir and rect_boton_salir.collidepoint(mouse_pos):
                pantalla_actual = "menu"
                mostrando_pregunta = False
                mostrando_retroalimentacion = False

            # Menú principal
            elif pantalla_actual == "menu":
                if rect_ajustes.collidepoint(mouse_pos):
                    pantalla_actual = "ajustes"
                elif rect_jugar.collidepoint(mouse_pos):
                    pantalla_actual = "jugar"
                elif rect_creditos.collidepoint(mouse_pos):
                    pantalla_actual = "creditos"
                elif rect_youtube.collidepoint(mouse_pos):
                    webbrowser.open(url_youtube)  
                elif rect_mago.collidepoint(mouse_pos):
                    pantalla_actual = "mago"  

            # Ajustes: controles de audio
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

            # Jugar
            elif pantalla_actual == "jugar" and not mostrando_pregunta and not mostrando_retroalimentacion:
                for circ in circulos:
                    centro = circ["centro"]
                    radio = circ["radio"]
                    distancia = ((mouse_pos[0] - centro[0])**2 + (mouse_pos[1] - centro[1])**2)**0.5
                    if distancia <= radio:
                        materia = circ["materia"]
                        pregunta_data = obtener_pregunta_aleatoria(materia)
                        if pregunta_data:
                            mostrando_pregunta = True
                            botones_opciones = []
                        break

            # Responder con clic en opción
            elif mostrando_pregunta:
                for rect_boton, opcion_idx in botones_opciones:
                    if rect_boton.collidepoint(mouse_pos):
                        try:
                            respuesta_raw = pregunta_data["respuesta"]
                            if isinstance(respuesta_raw, str):
                                respuesta_idx = int(respuesta_raw)
                            else:
                                respuesta_idx = respuesta_raw
                        except (ValueError, TypeError, KeyError):
                            respuesta_idx = None

                        if respuesta_idx == opcion_idx:
                            mensaje_retro = "¡Correcto!"
                            color_retro = (0, 255, 0)
                            try:
                                idx_actual = orden_antihorario.index(pregunta_data["materia"])
                            except ValueError:
                                idx_actual = 0
                            siguiente_materia = orden_antihorario[(idx_actual + 1) % len(orden_antihorario)]

                            for c in circulos:
                                if c["materia"] == siguiente_materia:
                                    equipo1.rect.center = c["centro"]
                                    break
                        else:
                            mensaje_retro = "Incorrecto"
                            color_retro = (255, 0, 0)

                        mostrando_pregunta = False
                        mostrando_retroalimentacion = True
                        temporizador_retro = pygame.time.get_ticks()
                        break

    # === Renderizado ===
    if pantalla_actual == "menu":
        ventana.blit(fondo, (-50, -150))

        # Botones principales
        ventana.blit(boton_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else boton_ajustes, rect_ajustes.topleft)
        ventana.blit(boton_jugar_hover if rect_jugar.collidepoint(mouse_pos) else boton_jugar, rect_jugar.topleft)
        ventana.blit(boton_creditos_hover if rect_creditos.collidepoint(mouse_pos) else boton_creditos, rect_creditos.topleft)

        # Botón YouTube 
        if rect_youtube.collidepoint(mouse_pos):
            ventana.blit(boton_youtube_hover, rect_youtube.topleft)
        else:
            ventana.blit(boton_youtube, rect_youtube.topleft)

        # Botón Mago (
        if rect_mago.collidepoint(mouse_pos):
            ventana.blit(personaje_interfaz_hover, rect_mago.topleft)
        else:
            ventana.blit(personaje_interfaz, rect_mago.topleft)

        # Logo
        ventana.blit(logo_juego, (400, 40))

    elif pantalla_actual == "ajustes":
        ventana.blit(fondo, (-50, -150))
        titulo = pygame.font.SysFont(None, 60).render("AJUSTES", True, NEGRO)
        ventana.blit(titulo, (ventana.get_width() // 2 - titulo.get_width() // 2, 30))

        if rect_boton_salir:
            ventana.blit(boton_salir_hover if rect_boton_salir.collidepoint(mouse_pos) else boton_salir, rect_boton_salir.topleft)

        if musica_activa:
            ventana.blit(boton_mute_hover if rect_mute.collidepoint(mouse_pos) else boton_mute, rect_mute.topleft)
        else:
            ventana.blit(boton_unmute_hover if rect_unmute.collidepoint(mouse_pos) else boton_unmute, rect_unmute.topleft)
        ventana.blit(boton_vol_up_hover if rect_vol_up.collidepoint(mouse_pos) else boton_vol_up, rect_vol_up.topleft)
        ventana.blit(boton_vol_down_hover if rect_vol_down.collidepoint(mouse_pos) else boton_vol_down, rect_vol_down.topleft)

    elif pantalla_actual == "jugar":
        ventana.blit(tablero, (0, 0))

        # Dibujar círculos por materia
        for circ in circulos:
            centro = circ["centro"]
            radio = circ["radio"]
            materia = circ["materia"]
            color = materias.get(materia, (100, 100, 100))
            pygame.draw.circle(ventana, color, centro, radio)
            texto_materia = fuente_ayuda.render(materia, True, NEGRO)
            ventana.blit(texto_materia, (centro[0] - texto_materia.get_width() // 2, centro[1] - 8))

        grupo_equipo_1.update()
        grupo_equipo_1.draw(ventana)
        
        if rect_boton_salir:
            ventana.blit(boton_salir_hover if rect_boton_salir.collidepoint(mouse_pos) else boton_salir, rect_boton_salir.topleft)


        # Mostrar pregunta
        if mostrando_pregunta and pregunta_data:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))

            titulo_materia = fuente_pregunta.render(f"{pregunta_data['materia']}", True, materias[pregunta_data['materia']])
            ventana.blit(titulo_materia, (ANCHO // 2 - titulo_materia.get_width() // 2, 80))

            render_pregunta = fuente_pregunta.render(pregunta_data["pregunta"], True, BLANCO)
            ventana.blit(render_pregunta, render_pregunta.get_rect(center=(ANCHO // 2, 150)))

            y_opcion = 220
            botones_opciones.clear()
            for i, opcion in enumerate(pregunta_data["opciones"]):
                texto = fuente_opciones.render(f"{i+1}. {opcion}", True, BLANCO)
                rect_boton = texto.get_rect(center=(ANCHO // 2, y_opcion))
                color_fondo = (100, 100, 100) if rect_boton.collidepoint(mouse_pos) else (50, 50, 50)
                pygame.draw.rect(ventana, color_fondo, rect_boton.inflate(30, 15), border_radius=10)
                ventana.blit(texto, rect_boton)
                botones_opciones.append((rect_boton, i))
                y_opcion += 60

            mensaje = fuente_ayuda.render("Haz clic en tu opción", True, (100, 200, 255))
            ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, y_opcion + 30))

        # Mostrar retroalimentación
        if mostrando_retroalimentacion:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))

            fuente_grande = pygame.font.SysFont("Arial", 72, bold=True)
            texto = fuente_grande.render(mensaje_retro, True, color_retro)
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
            ventana.blit(texto, rect_texto)

            instruccion = fuente_ayuda.render("Cerrando en 2 segundos...", True, BLANCO)
            ventana.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO // 2 + 60))

    elif pantalla_actual == "creditos":
        ventana.blit(fondo, (-50, -150))
        texto = pygame.font.SysFont(None, 60).render("Créditos", True, NEGRO)
        ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 30))
        
        if rect_boton_salir:
            ventana.blit(boton_salir_hover if rect_boton_salir.collidepoint(mouse_pos) else boton_salir, rect_boton_salir.topleft)


    elif pantalla_actual == "mago":  
        ventana.fill(CELESTE)
        font = pygame.font.SysFont(None, 60)
        texto1 = font.render("¡Hola, soy el Mago MTMC!", True, NEGRO)
        texto2 = fuente_ayuda.render("Estoy aquí para ayudarte a aprender.", True, NEGRO)
        ventana.blit(texto1, (ANCHO // 2 - texto1.get_width() // 2, ALTO // 2 - 60))
        ventana.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2))
        
        if rect_boton_salir:
            ventana.blit(boton_salir_hover if rect_boton_salir.collidepoint(mouse_pos) else boton_salir, rect_boton_salir.topleft)


    # === Cerrar retroalimentación después de 2 segundos ===
    if mostrando_retroalimentacion and pygame.time.get_ticks() - temporizador_retro > 2000:
        mostrando_retroalimentacion = False

    pygame.display.flip()

pygame.quit()
sys.exit()