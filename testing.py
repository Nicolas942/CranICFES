import pygame
import sys
import webbrowser
import random
from base_de_datos import obtener_pregunta_aleatoria

pygame.init()

# === Colores ===
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CELESTE = (135, 206, 250)
ROJO_MAT = (255, 0, 0)
AMARILLO_ES = (255, 255, 0)
VERDE_NAT = (0, 128, 0)
NARANJA_SOC = (255, 165, 0)
MORADO_IN = (128, 0, 128)

# === Colores por materia ===
COLORES_MATERIAS = {
    "Matematicas": ROJO_MAT,
    "Español": AMARILLO_ES,
    "Naturales": VERDE_NAT,
    "Sociales": NARANJA_SOC,
    "Ingles": MORADO_IN,
}

# === Mapa de materias a colores ===
materias = {
    "Matematicas": COLORES_MATERIAS["Matematicas"],
    "Español": COLORES_MATERIAS["Español"],
    "Naturales": COLORES_MATERIAS["Naturales"],
    "Sociales": COLORES_MATERIAS["Sociales"],
    "Ingles": COLORES_MATERIAS["Ingles"],
    "Matematicas2": COLORES_MATERIAS["Matematicas"],
    "Sociales2": COLORES_MATERIAS["Sociales"],
    "Español2": COLORES_MATERIAS["Español"],
    "Naturales2": COLORES_MATERIAS["Naturales"],
    "Ingles2": COLORES_MATERIAS["Ingles"],
    "Sociales3": COLORES_MATERIAS["Sociales"],
    "Matematicas3": COLORES_MATERIAS["Matematicas"],
    "Español3": COLORES_MATERIAS["Español"],
    "Naturales3": COLORES_MATERIAS["Naturales"],
    "Ingles3": COLORES_MATERIAS["Ingles"],
    "Sociales4": COLORES_MATERIAS["Sociales"],
}

# === Alias de materias ===
alias_materias = {
    "Matematicas2": "Matematicas",
    "Sociales2": "Sociales",
    "Español2": "Español",
    "Naturales2": "Naturales",
    "Ingles2": "Ingles",
    "Sociales3": "Sociales",
    "Matematicas3": "Matematicas",
    "Español3": "Español",
    "Naturales3": "Naturales",
    "Ingles3": "Ingles",
    "Sociales4": "Sociales",
}

# === Audio ===
pygame.mixer.init()
musica_activa = False
sonido_fondo = None
try:
    sonido_fondo = pygame.mixer.Sound("Sonidos/Fondo.mp3")
    pygame.mixer.Sound.play(sonido_fondo, loops=-1)
    musica_activa = True
except pygame.error:
    print("  No se pudo cargar el sonido de fondo")

# === Ventana ===
info = pygame.display.Info()
ANCHO = info.current_w
ALTO = info.current_h
ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("CranICFES")

# === Reloj para controlar FPS ===
clock = pygame.time.Clock()

def cargar_img(ruta, tamaño=None):
    try:
        img = pygame.image.load(ruta).convert_alpha()
        if tamaño:
            img = pygame.transform.scale(img, tamaño)
        return img
    except pygame.error as e:
        print(f"  No se pudo cargar la imagen: {ruta}")
        img = pygame.Surface(tamaño or (100, 50))
        img.fill((200, 0, 0))
        return img

# === Cargar imágenes principales ===
logo_juego = cargar_img("img/logo_juego.png")
fondo = cargar_img("img/FONDO.png")
tablero = cargar_img("img/tablero1.png")  # Sin tamaño fijo

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
boton_mute = cargar_img("img/mute.png", (100, 100))
boton_mute_hover = cargar_img("img/mute.png", (120, 120))
boton_unmute = cargar_img("img/unmute.png", (100, 100))
boton_unmute_hover = cargar_img("img/unmute.png", (120, 120))
boton_vol_up = cargar_img("img/vol_up.png", (100, 100))
boton_vol_up_hover = cargar_img("img/vol_up.png", (120, 120))
boton_vol_down = cargar_img("img/vol_down.png", (100, 100))
boton_vol_down_hover = cargar_img("img/vol_down.png", (120, 120))
mago_personaje = cargar_img("img/MAGO_MTMC.png", (100,100))

# === Posiciones menú (se recalcularán dinámicamente) ===
rect_ajustes = pygame.Rect(0, 0, 200, 50)
rect_jugar = pygame.Rect(0, 0, 200, 50)
rect_creditos = pygame.Rect(0, 0, 200, 50)

# === Botones adicionales ===
rect_youtube = pygame.Rect(0, 0, 150, 150)
rect_mago = pygame.Rect(0, 0, 250, 250)

# === Música botones ===
x_columna = 20
y_columna = 100
espacio = 120
rect_mute = pygame.Rect(x_columna, y_columna, 100, 100)
rect_unmute = pygame.Rect(x_columna, y_columna, 100, 100)
rect_vol_up = pygame.Rect(x_columna, y_columna + espacio, 100, 100)
rect_vol_down = pygame.Rect(x_columna, y_columna + espacio*2, 100, 100)

# === Círculos por materia (definidos como porcentajes) ===
circulos_porcentajes = [
    {"x": 0.37, "y": 0.125, "radio": 50, "materia": "Matematicas"},
    {"x": 0.28, "y": 0.24, "radio": 40, "materia": "Sociales"},
    {"x": 0.34, "y": 0.78, "radio": 40, "materia": "Ingles"},
    {"x": 0.27, "y": 0.69, "radio": 40, "materia": "Naturales"},
    {"x": 0.24, "y": 0.37, "radio": 40, "materia": "Español"},
    {"x": 0.57, "y": 0.84, "radio": 40, "materia": "Sociales2"},
    {"x": 0.65, "y": 0.78, "radio": 40, "materia": "Matematicas2"},
    {"x": 0.74, "y": 0.48, "radio": 40, "materia": "Español2"},
    {"x": 0.73, "y": 0.34, "radio": 40, "materia": "Naturales2"},
    {"x": 0.67, "y": 0.23, "radio": 40, "materia": "Ingles2"},
    {"x": 0.50, "y": 0.18, "radio": 40, "materia": "Sociales3"},
    {"x": 0.43, "y": 0.22, "radio": 40, "materia": "Matematicas3"},
    {"x": 0.37, "y": 0.32, "radio": 40, "materia": "Español3"},
    {"x": 0.35, "y": 0.44, "radio": 40, "materia": "Naturales3"},
    {"x": 0.39, "y": 0.57, "radio": 40, "materia": "Ingles3"},
    {"x": 0.46, "y": 0.64, "radio": 40, "materia": "Sociales4"},
]

# Convertir a píxeles
def actualizar_circulos():
    global circulos
    circulos = [
        {
            "centro": (int(c["x"] * ANCHO), int(c["y"] * ALTO)),
            "radio": c["radio"],
            "materia": c["materia"]
        }
        for c in circulos_porcentajes
    ]

actualizar_circulos()

# === Orden del recorrido ===
orden_antihorario = [
    "Matematicas",
    "Sociales",
    "Español",
    "Naturales",
    "Ingles",
    "Sociales2",
    "Matematicas2",
    "Español2",
    "Naturales2",
    "Ingles2",
    "Sociales3",     
    "Matematicas3",
    "Español3",
    "Naturales3",
    "Ingles3",
    "Sociales4",
]

# === Sprite del equipo ===
class Equipo1(pygame.sprite.Sprite):
    def _init_(self, x, y):
        super()._init_()
        self.image = mago_personaje
        self.rect = self.image.get_rect(topleft=(x, y))

class Equipo2(pygame.sprite.Sprite):
    def _init_(self, x, y):
        super()._init_()
        self.image = mago_personaje
        self.rect = self.image.get_rect(topleft=(x, y))

equipo1 = Equipo1(510, 20)
equipo2 = Equipo2(420, 20)
grupo_equipo = pygame.sprite.Group(equipo1, equipo2)

# === Estado del juego ===
pantalla_actual = "menu"
mostrando_pregunta = False
mostrando_retroalimentacion = False
mensaje_retro = ""
color_retro = BLANCO
pregunta_data = None
botones_opciones = []
temporizador_retro = 0
tiempo_inicio_pregunta = 0
TIEMPO_LIMITE = 60000  # 60 segundos en milisegundos

# Sistema de turnos
turno_actual = "equipo1"  # Empieza el equipo 1

# === Estado del modo dibujo ===
dibujando = False
superficie_dibujo = None
color_dibujo = NEGRO
grosor_dibujo = 5
ultima_pos = None
tiempo_inicio_dibujo = 0
mostrando_validacion_dibujo = False

# === Estado del modo organizar ===
elementos_organizar = []
elementos_seleccionados = []  # Guarda índices seleccionados para intercambiar
tiempo_inicio_organizar = 0
mostrando_validacion_organizar = False

# === Fuentes (se recalcularán dinámicamente) ===
def actualizar_fuentes():
    global fuente_pregunta, fuente_opciones, fuente_ayuda, fuente_tiempo
    base_ancho = 1920
    escala = ANCHO / base_ancho
    fuente_pregunta = pygame.font.SysFont("Arial", int(36 * escala), bold=True)
    fuente_opciones = pygame.font.SysFont("Arial", int(30 * escala))
    fuente_ayuda = pygame.font.SysFont("Arial", int(24 * escala))
    fuente_tiempo = pygame.font.SysFont("Arial", int(36 * escala), bold=True)

actualizar_fuentes()

# === Funciones de ayuda para dibujar recuadros uniformes y texto envuelto ===
def wrap_text(font, text, max_width):
    """Devuelve una lista de líneas que caben en max_width (en px) usando font.size()."""
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        test = current + (" " if current else "") + w
        width = font.size(test)[0]
        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines

def draw_wrapped_rect(surface, text, font, center_x, y, bar_width,
                      bg_color=(50,50,50), text_color=BLANCO,
                      padding_x=30, padding_y=18, border_radius=15):
    """Dibuja un rect con texto envuelto y devuelve el rect dibujado."""
    max_text_width = bar_width - 2*padding_x
    lines = wrap_text(font, text, max_text_width)
    line_height = font.get_height()
    height = len(lines)*line_height + 2*padding_y
    rect = pygame.Rect(center_x - bar_width//2, y, bar_width, height)
    pygame.draw.rect(surface, bg_color, rect, border_radius=border_radius)
    for i, line in enumerate(lines):
        txt_surf = font.render(line, True, text_color)
        txt_rect = txt_surf.get_rect(center=(center_x, y + padding_y + i*line_height + line_height//2))
        surface.blit(txt_surf, txt_rect)
    return rect

# === Función para cambiar turno ===
def cambiar_turno():
    global turno_actual
    turno_actual = "equipo2" if turno_actual == "equipo1" else "equipo1"

# === Bucle principal ===
corriendo = True
while corriendo:
    clock.tick(60) 
    mouse_pos = pygame.mouse.get_pos()
    rect_boton_salir = None
    rect_terminar = None
    if pantalla_actual in ["ajustes", "creditos", "jugar", "mago", "dibujar"]:
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
            ANCHO, ALTO = evento.w, evento.h
            ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            
            # Recalcular posiciones
            actualizar_circulos()
            actualizar_fuentes()
            
            # Botones del menú
            boton_y = int(ALTO * 0.8)
            espacio_entre_botones = int(ANCHO * 0.15)
            total_ancho_botones = 3 * 200 + 2 * espacio_entre_botones
            inicio_x = (ANCHO - total_ancho_botones) // 2
            rect_ajustes.topleft = (inicio_x, boton_y)
            rect_jugar.topleft = (inicio_x + 200 + espacio_entre_botones, boton_y)
            rect_creditos.topleft = (inicio_x + 2*200 + 2*espacio_entre_botones, boton_y)
            
            # Botones adicionales
            rect_youtube.topleft = (int(ANCHO * 0.05), int(ALTO * 0.2))
            rect_mago.topleft = (int(ANCHO * 0.8), int(ALTO * 0.2))
            
            if pantalla_actual == "dibujar":
                superficie_dibujo = None

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Botón de salir (atrás) en pantallas secundarias
            if rect_boton_salir and rect_boton_salir.collidepoint(mouse_pos):
                pantalla_actual = "menu"
                mostrando_pregunta = False
                mostrando_retroalimentacion = False
                if pantalla_actual != "dibujar":
                    superficie_dibujo = None

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
                    if sonido_fondo:
                        pygame.mixer.Sound.stop(sonido_fondo)
                    musica_activa = False
                elif (not musica_activa) and rect_unmute.collidepoint(mouse_pos):
                    if sonido_fondo:
                        pygame.mixer.Sound.play(sonido_fondo, loops=-1)
                    musica_activa = True
                elif rect_vol_up.collidepoint(mouse_pos):
                    if sonido_fondo:
                        vol = sonido_fondo.get_volume()
                        sonido_fondo.set_volume(min(1.0, vol + 0.1))
                elif rect_vol_down.collidepoint(mouse_pos):
                    if sonido_fondo:
                        vol = sonido_fondo.get_volume()
                        sonido_fondo.set_volume(max(0.0, vol - 0.1))

            # Jugar: mostrar pregunta al hacer clic en círculo
            elif pantalla_actual == "jugar" and not mostrando_pregunta and not mostrando_retroalimentacion:
                for circ in circulos:
                    cx, cy = circ["centro"]
                    r = circ["radio"]
                    dist_click = ((mouse_pos[0] - cx)*2 + (mouse_pos[1] - cy)2)*0.5
                    if dist_click <= r:
                        materia_original = circ["materia"]
                        materia_real = alias_materias.get(materia_original, materia_original)
                        pregunta_data = obtener_pregunta_aleatoria(materia_real)
                        if pregunta_data:
                            if not all(k in pregunta_data for k in ("pregunta",)):
                                print("  Pregunta mal formada (falta 'pregunta'):", pregunta_data)
                                break

                            # Modo dibujo
                            if pregunta_data.get("actividad") == "dibujar":
                                pregunta_data["materia"] = materia_original
                                mostrando_pregunta = True
                                botones_opciones = []
                                tiempo_inicio_pregunta = pygame.time.get_ticks()

                            # Modo organizar (acepta "opciones" o "elementos")
                            elif pregunta_data.get("actividad") == "organizar":
                                # Si no tiene "elementos" pero tiene "opciones", lo asignamos
                                if "elementos" not in pregunta_data and "opciones" in pregunta_data:
                                    pregunta_data["elementos"] = pregunta_data["opciones"]
                                if not all(k in pregunta_data for k in ("elementos", "respuesta")):
                                    print("  Pregunta 'organizar' mal formada:", pregunta_data)
                                    break
                                pregunta_data["materia"] = materia_original
                                elementos_organizar = pregunta_data["elementos"][:]
                                random.shuffle(elementos_organizar)
                                elementos_seleccionados = []
                                mostrando_pregunta = True
                                botones_opciones = []
                                tiempo_inicio_organizar = pygame.time.get_ticks()


                            # Modo selección normal
                            else:
                                if not all(k in pregunta_data for k in ("opciones", "respuesta")):
                                    print("  Pregunta mal formada (faltan opciones o respuesta):", pregunta_data)
                                    break
                                pregunta_data["materia"] = materia_original
                                mostrando_pregunta = True
                                botones_opciones = []
                                tiempo_inicio_pregunta = pygame.time.get_ticks()
                        else:
                            print(f"  No se pudo cargar pregunta para: {materia_real}")
                        break

            # Entrar al modo dibujo 
            elif mostrando_pregunta and pregunta_data and pregunta_data.get("actividad") == "dibujar":
                pantalla_actual = "dibujar"
                mostrando_pregunta = False
                tiempo_inicio_dibujo = pygame.time.get_ticks()

            # Manejar clics en modo organizar 
            elif mostrando_pregunta and pregunta_data and pregunta_data.get("actividad") == "organizar":
                # usamos el mismo ancho/base que en render para detectar clicks
                center_x = ANCHO // 2
                bar_width = min(1100, int(ANCHO * 0.8))
                option_height = 60
                y_elemento = 220
                for i, elemento in enumerate(elementos_organizar):
                    rect_boton = pygame.Rect(center_x - bar_width//2, y_elemento, bar_width, option_height)
                    if rect_boton.collidepoint(mouse_pos):
                        if len(elementos_seleccionados) == 0:
                            elementos_seleccionados.append(i)
                        elif len(elementos_seleccionados) == 1:
                            idx1 = elementos_seleccionados[0]
                            idx2 = i
                            elementos_organizar[idx1], elementos_organizar[idx2] = elementos_organizar[idx2], elementos_organizar[idx1]
                            elementos_seleccionados = []
                        break
                    y_elemento += option_height + 20

                # Botón "TERMINAR" para validar 
                boton_terminar_org = fuente_pregunta.render("TERMINAR", True, BLANCO)
                rect_terminar_org = boton_terminar_org.get_rect(center=(ANCHO // 2, ALTO - 80))
                if rect_terminar_org.collidepoint(mouse_pos):
                    if elementos_organizar == pregunta_data["respuesta"]:
                        mensaje_retro = "¡Correcto!"
                        color_retro = (0, 255, 0)
                        try:
                            idx_actual = orden_antihorario.index(pregunta_data["materia"])
                        except ValueError:
                            idx_actual = 0
                        siguiente_materia = orden_antihorario[(idx_actual + 1) % len(orden_antihorario)]
                        equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                        for c in circulos:
                            if c["materia"] == siguiente_materia:
                                equipo_actual.rect.center = c["centro"]
                                break
                    else:
                        mensaje_retro = "Incorrecto"
                        color_retro = (255, 0, 0)

                    cambiar_turno()
                    mostrando_pregunta = False
                    mostrando_retroalimentacion = True
                    temporizador_retro = pygame.time.get_ticks()
                    elementos_organizar = []
                    elementos_seleccionados = []

            # Manejar clics en modo dibujo 
            elif pantalla_actual == "dibujar" and not mostrando_validacion_dibujo:
                boton_terminar_texto = fuente_pregunta.render("TERMINAR", True, BLANCO)
                rect_terminar = boton_terminar_texto.get_rect(center=(ANCHO // 2, ALTO - 80))
                if rect_terminar.collidepoint(mouse_pos):
                    mostrando_validacion_dibujo = True
                else:
                    dibujando = True
                    if superficie_dibujo:
                        pygame.draw.circle(superficie_dibujo, color_dibujo, evento.pos, grosor_dibujo // 2)
                    ultima_pos = evento.pos

            # Manejar clics en validación de dibujo
            elif pantalla_actual == "dibujar" and mostrando_validacion_dibujo:
                boton_correcto = fuente_pregunta.render(" CORRECTO", True, BLANCO)
                rect_correcto = boton_correcto.get_rect(center=(ANCHO // 2 - 200, ALTO // 2 + 50))
                boton_incorrecto = fuente_pregunta.render(" INCORRECTO", True, BLANCO)
                rect_incorrecto = boton_incorrecto.get_rect(center=(ANCHO // 2 + 200, ALTO // 2 + 50))

                if rect_correcto.collidepoint(mouse_pos):
                    try:
                        idx_actual = orden_antihorario.index(pregunta_data["materia"])
                    except ValueError:
                        idx_actual = 0
                    siguiente_materia = orden_antihorario[(idx_actual + 1) % len(orden_antihorario)]
                    equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                    for c in circulos:
                        if c["materia"] == siguiente_materia:
                            equipo_actual.rect.center = c["centro"]
                            break
                    cambiar_turno()
                    pantalla_actual = "jugar"
                    superficie_dibujo = None
                    ultima_pos = None
                    mostrando_validacion_dibujo = False
                elif rect_incorrecto.collidepoint(mouse_pos):
                    cambiar_turno()
                    pantalla_actual = "jugar"
                    superficie_dibujo = None
                    ultima_pos = None
                    mostrando_validacion_dibujo = False

            # Responder con clic en opción 
            elif mostrando_pregunta and pregunta_data and pregunta_data.get("actividad") not in ["dibujar", "organizar"]:
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
                            equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                            for c in circulos:
                                if c["materia"] == siguiente_materia:
                                    equipo_actual.rect.center = c["centro"]
                                    break
                        else:
                            mensaje_retro = "Incorrecto"
                            color_retro = (255, 0, 0)
                        mostrando_pregunta = False
                        mostrando_retroalimentacion = True
                        temporizador_retro = pygame.time.get_ticks()
                        cambiar_turno()
                        break

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if pantalla_actual == "dibujar":
                dibujando = False
                ultima_pos = None

        elif evento.type == pygame.MOUSEMOTION:
            if pantalla_actual == "dibujar" and dibujando and superficie_dibujo:
                if ultima_pos:
                    pygame.draw.line(superficie_dibujo, color_dibujo, ultima_pos, evento.pos, grosor_dibujo)
                else:
                    pygame.draw.circle(superficie_dibujo, color_dibujo, evento.pos, grosor_dibujo // 2)
                ultima_pos = evento.pos

    # TEMPORIZADOR: modo respuesta multiple
    if mostrando_pregunta and pregunta_data and pregunta_data.get("actividad") not in ["dibujar", "organizar"]:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio_pregunta
        if tiempo_transcurrido >= TIEMPO_LIMITE:
            mensaje_retro = "¡Tiempo agotado!"
            color_retro = (255, 0, 0)
            mostrando_pregunta = False
            mostrando_retroalimentacion = True
            temporizador_retro = pygame.time.get_ticks()
            cambiar_turno()

    # TEMPORIZADOR: modo dibujo
    if pantalla_actual == "dibujar" and not mostrando_validacion_dibujo:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio_dibujo
        if tiempo_transcurrido >= TIEMPO_LIMITE:
            mostrando_validacion_dibujo = True

    # TEMPORIZADOR:modo organizar
    if mostrando_pregunta and pregunta_data and pregunta_data.get("actividad") == "organizar":
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - tiempo_inicio_organizar
        if tiempo_transcurrido >= TIEMPO_LIMITE:
            if elementos_organizar == pregunta_data["respuesta"]:
                mensaje_retro = "¡Correcto!"
                color_retro = (0, 255, 0)
                try:
                    idx_actual = orden_antihorario.index(pregunta_data["materia"])
                except ValueError:
                    idx_actual = 0
                siguiente_materia = orden_antihorario[(idx_actual + 1) % len(orden_antihorario)]
                equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                for c in circulos:
                    if c["materia"] == siguiente_materia:
                        equipo_actual.rect.center = c["centro"]
                        break
            else:
                mensaje_retro = "Tiempo agotado - Incorrecto"
                color_retro = (255, 0, 0)

            cambiar_turno()
            mostrando_pregunta = False
            mostrando_retroalimentacion = True
            temporizador_retro = pygame.time.get_ticks()
            elementos_organizar = []
            elementos_seleccionados = []

    # === Renderizado ===
    if pantalla_actual == "menu":
        ventana.blit(fondo, (-50, -150))
        
        # Posicionar botones dinámicamente
        boton_y = int(ALTO * 0.8)
        espacio_entre_botones = int(ANCHO * 0.15)
        total_ancho_botones = 3 * 200 + 2 * espacio_entre_botones
        inicio_x = (ANCHO - total_ancho_botones) // 2
        rect_ajustes.topleft = (inicio_x, boton_y)
        rect_jugar.topleft = (inicio_x + 200 + espacio_entre_botones, boton_y)
        rect_creditos.topleft = (inicio_x + 2*200 + 2*espacio_entre_botones, boton_y)
        
        ventana.blit(boton_ajustes_hover if rect_ajustes.collidepoint(mouse_pos) else boton_ajustes, rect_ajustes.topleft)
        ventana.blit(boton_jugar_hover if rect_jugar.collidepoint(mouse_pos) else boton_jugar, rect_jugar.topleft)
        ventana.blit(boton_creditos_hover if rect_creditos.collidepoint(mouse_pos) else boton_creditos, rect_creditos.topleft)
        
        # Botones adicionales
        rect_youtube.topleft = (int(ANCHO * 0.05), int(ALTO * 0.2))
        rect_mago.topleft = (int(ANCHO * 0.8), int(ALTO * 0.2))
        
        if rect_youtube.collidepoint(mouse_pos):
            ventana.blit(boton_youtube_hover, rect_youtube.topleft)
        else:
            ventana.blit(boton_youtube, rect_youtube.topleft)
        if rect_mago.collidepoint(mouse_pos):
            ventana.blit(personaje_interfaz_hover, rect_mago.topleft)
        else:
            ventana.blit(personaje_interfaz, rect_mago.topleft)
        ventana.blit(logo_juego, (ANCHO // 2 - logo_juego.get_width() // 2, 40))

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
        # Escalar tablero al tamaño de la ventana
        tablero_escalado = pygame.transform.scale(tablero, (ANCHO, ALTO))
        ventana.blit(tablero_escalado, (0, 0))
        
        color_turno = ROJO_MAT if turno_actual == "equipo1" else MORADO_IN
        texto_turno = fuente_pregunta.render(f"Turno: {turno_actual.upper()}", True, color_turno)
        ventana.blit(texto_turno, (10, 10))
        
        for circ in circulos:
            centro = circ["centro"]
            radio = circ["radio"]
            materia = circ["materia"]
            color = materias.get(materia, (100, 100, 100))
            pygame.draw.circle(ventana, color, centro, radio)
            texto_materia = fuente_ayuda.render(materia, True, NEGRO)
            ventana.blit(texto_materia, (centro[0] - texto_materia.get_width() // 2, centro[1] - 8))
        
        grupo_equipo.update()
        grupo_equipo.draw(ventana)
        
        if rect_boton_salir:
            ventana.blit(boton_salir_hover if rect_boton_salir.collidepoint(mouse_pos) else boton_salir, rect_boton_salir.topleft)

        if mostrando_pregunta and pregunta_data:
            # overlay semitransparente
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))

            # título de materia
            titulo_materia = fuente_pregunta.render(f"{pregunta_data['materia']}", True, materias.get(pregunta_data['materia'], BLANCO))
            ventana.blit(titulo_materia, (ANCHO // 2 - titulo_materia.get_width() // 2, 40))

            # Parámetros de anchura uniforme para pregunta y opciones
            center_x = ANCHO // 2
            bar_width = min(1100, int(ANCHO * 0.8))  # ancho fijo relativo a la ventana

            # DIBUJAR PREGUNTA
            pregunta_rect = draw_wrapped_rect(
                ventana,
                pregunta_data["pregunta"],
                fuente_pregunta,
                center_x,
                100,
                bar_width,
                bg_color=(40, 40, 40),
                text_color=BLANCO,
                padding_x=40,
                padding_y=20,
                border_radius=18
            )

            # Modo dibujo
            if pregunta_data.get("actividad") == "dibujar":
                mensaje = fuente_ayuda.render("Haz clic en cualquier lugar para entrar al modo dibujo", True, (100, 200, 255))
                ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO - 100))

            # Modo organizar
            elif pregunta_data.get("actividad") == "organizar":
                # Mostrar elementos con rects uniformes y detectar hover/selección
                y_elemento = pregunta_rect.bottom + 30
                option_height = 60
                for i, elemento in enumerate(elementos_organizar):
                    rect_boton = pygame.Rect(center_x - bar_width//2, y_elemento, bar_width, option_height)
                    is_hover = rect_boton.collidepoint(mouse_pos)
                    is_selected = (i in elementos_seleccionados)
                    color_fondo = (120, 120, 255) if is_selected else (100, 100, 100) if is_hover else (50, 50, 50)
                    pygame.draw.rect(ventana, color_fondo, rect_boton, border_radius=12)
                    texto = fuente_opciones.render(f"{i+1}. {elemento}", True, BLANCO)
                    ventana.blit(texto, texto.get_rect(center=rect_boton.center))
                    y_elemento += option_height + 20

                # Botón "TERMINAR"
                boton_terminar_org = fuente_pregunta.render("TERMINAR", True, BLANCO)
                rect_terminar_org = boton_terminar_org.get_rect(center=(ANCHO // 2, ALTO - 80))
                color_boton = (200, 0, 0) if rect_terminar_org.collidepoint(mouse_pos) else (255, 0, 0)
                pygame.draw.rect(ventana, color_boton, rect_terminar_org.inflate(40, 20), border_radius=15)
                ventana.blit(boton_terminar_org, rect_terminar_org)

                # Mostrar tiempo restante
                tiempo_actual = pygame.time.get_ticks()
                tiempo_restante = max(0, (TIEMPO_LIMITE - (tiempo_actual - tiempo_inicio_organizar)) // 1000)
                texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 0))
                ventana.blit(texto_tiempo, (int(ANCHO * 0.9), 10))

            # Modo selección normal
            else:
                y_opcion = pregunta_rect.bottom + 30
                botones_opciones.clear()
                option_height = 60
                for i, opcion in enumerate(pregunta_data["opciones"]):
                    rect_boton = pygame.Rect(center_x - bar_width//2, y_opcion, bar_width, option_height)
                    is_hover = rect_boton.collidepoint(mouse_pos)
                    color_fondo = (120, 120, 120) if is_hover else (60, 60, 60)
                    pygame.draw.rect(ventana, color_fondo, rect_boton, border_radius=12)
                    texto = fuente_opciones.render(f"{i+1}. {opcion}", True, BLANCO)
                    ventana.blit(texto, texto.get_rect(center=rect_boton.center))
                    botones_opciones.append((rect_boton, i))
                    y_opcion += option_height + 20

                mensaje = fuente_ayuda.render("Haz clic en tu opción", True, (100, 200, 255))
                ventana.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, y_opcion + 10))

                # Mostrar tiempo restante
                tiempo_actual = pygame.time.get_ticks()
                tiempo_restante = max(0, (TIEMPO_LIMITE - (tiempo_actual - tiempo_inicio_pregunta)) // 1000)
                texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 0))
                ventana.blit(texto_tiempo, (int(ANCHO * 0.9), 10))

        if mostrando_retroalimentacion:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))
            fuente_grande = pygame.font.SysFont("Arial", 72, bold=True)
            texto = fuente_grande.render(mensaje_retro, True, color_retro)
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
            ventana.blit(texto, rect_texto)
            instruccion = fuente_ayuda.render("Cerrando en 1 segundo...", True, BLANCO)
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

    elif pantalla_actual == "dibujar":
        if superficie_dibujo is None:
            superficie_dibujo = pygame.Surface((ANCHO, ALTO))
            superficie_dibujo.fill(BLANCO)

        if not mostrando_validacion_dibujo:
            ventana.fill(BLANCO)
            ventana.blit(superficie_dibujo, (0, 0))
            texto = fuente_pregunta.render("Modo Dibujo - Mantén presionado el clic para dibujar", True, NEGRO)
            ventana.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 20))
            tiempo_actual = pygame.time.get_ticks()
            tiempo_restante = max(0, (TIEMPO_LIMITE - (tiempo_actual - tiempo_inicio_dibujo)) // 1000)
            texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 0, 0))
            ventana.blit(texto_tiempo, (int(ANCHO * 0.9), 10))
            boton_terminar_texto = fuente_pregunta.render("TERMINAR", True, BLANCO)
            rect_terminar = boton_terminar_texto.get_rect(center=(ANCHO // 2, ALTO - 80))
            color_boton = (200, 0, 0) if rect_terminar.collidepoint(mouse_pos) else (255, 0, 0)
            pygame.draw.rect(ventana, color_boton, rect_terminar.inflate(40, 20), border_radius=15)
            ventana.blit(boton_terminar_texto, rect_terminar)
            if rect_boton_salir:
                ventana.blit(boton_salir_hover if rect_boton_salir.collidepoint(mouse_pos) else boton_salir, rect_boton_salir.topleft)
        else:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))
            texto_titulo = fuente_pregunta.render("Considera que la respuesta es correcta", True, BLANCO)
            ventana.blit(texto_titulo, texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 80)))
            boton_correcto = fuente_pregunta.render(" CORRECTO", True, BLANCO)
            rect_correcto = boton_correcto.get_rect(center=(ANCHO // 2 - 200, ALTO // 2 + 50))
            color_correcto = (0, 200, 0) if rect_correcto.collidepoint(mouse_pos) else (0, 255, 0)
            pygame.draw.rect(ventana, color_correcto, rect_correcto.inflate(40, 30), border_radius=15)
            ventana.blit(boton_correcto, rect_correcto)
            boton_incorrecto = fuente_pregunta.render(" INCORRECTO", True, BLANCO)
            rect_incorrecto = boton_incorrecto.get_rect(center=(ANCHO // 2 + 200, ALTO // 2 + 50))
            color_incorrecto = (200, 0, 0) if rect_incorrecto.collidepoint(mouse_pos) else (255, 0, 0)
            pygame.draw.rect(ventana, color_incorrecto, rect_incorrecto.inflate(40, 30), border_radius=15)
            ventana.blit(boton_incorrecto, rect_incorrecto)

    # === Cerrar retroalimentación después de 1 segundo ===
    if mostrando_retroalimentacion and pygame.time.get_ticks() - temporizador_retro > 1000:
        mostrando_retroalimentacion = False

    # === Actualizar pantalla ===
    pygame.display.flip()

pygame.quit()
sys.exit()