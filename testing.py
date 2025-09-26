import pygame
import sys
import webbrowser
import random
from base_de_datos import obtener_pregunta_aleatoria

# ─────────────────────────────────────────────────────────────
# Inicialización
# ─────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.init()

# ─────────────────────────────────────────────────────────────
# Constantes y configuración
# ─────────────────────────────────────────────────────────────
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CELESTE = (135, 206, 255)
ROJO_MAT = (255, 0, 0)
AMARILLO_ES = (255, 255, 0)
VERDE_NAT = (0, 128, 0)
NARANJA_SOC = (255, 165, 0)
MORADO_IN = (128, 0, 128)

COLORES_MATERIAS = {
    "Matematicas": ROJO_MAT,
    "Español": AMARILLO_ES,
    "Naturales": VERDE_NAT,
    "Sociales": NARANJA_SOC,
    "Ingles": MORADO_IN,
}

ALIAS_MATERIAS = {
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

# Mapeo de todas las materias a sus colores
MATERIAS = {}
for clave in COLORES_MATERIAS:
    MATERIAS[clave] = COLORES_MATERIAS[clave]
for alias, original in ALIAS_MATERIAS.items():
    MATERIAS[alias] = COLORES_MATERIAS[original]

# Configuración del juego
TIEMPO_LIMITE = 60000  # 60 segundos
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
pygame.display.set_caption("CranICFES")
reloj = pygame.time.Clock()

# ─────────────────────────────────────────────────────────────
# Carga de recursos
# ─────────────────────────────────────────────────────────────
def cargar_imagen(ruta, tamaño=None):
    """Carga una imagen con manejo de errores."""
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        if tamaño:
            imagen = pygame.transform.scale(imagen, tamaño)
        return imagen
    except pygame.error as error:
        print(f"⚠️ No se pudo cargar la imagen: {ruta} - {error}")
        marcador = pygame.Surface(tamaño or (100, 50))
        marcador.fill((200, 0, 0))
        return marcador

# Imágenes principales
logo_juego = cargar_imagen("img/logo_juego.png")
fondo = cargar_imagen("img/FONDO.png")
tablero = cargar_imagen("img/tablero1.png", (1366, 720))
mago_personaje = cargar_imagen("img/MAGO_MTMC.png", (100, 100))

# Botones
boton_ajustes = cargar_imagen("img/AJUSTES.png", (200, 50))
boton_ajustes_hover = cargar_imagen("img/AJUSTES.png", (220, 55))
boton_jugar = cargar_imagen("img/JUGAR.png", (200, 50))
boton_jugar_hover = cargar_imagen("img/JUGAR.png", (220, 55))
boton_creditos = cargar_imagen("img/CREDITOS.png", (200, 50))
boton_creditos_hover = cargar_imagen("img/CREDITOS.png", (220, 55))
boton_salir = cargar_imagen("img/boton_salir.png", (120, 100))
boton_salir_hover = cargar_imagen("img/boton_salir.png", (140, 120))

# Botones adicionales
URL_YOUTUBE = "https://www.youtube.com/watch?v=yNEpyU3PnDI"
boton_youtube = cargar_imagen("img/LOGO_YT.png", (150, 150))
boton_youtube_hover = cargar_imagen("img/LOGO_YT.png", (200, 200))
personaje_interfaz = cargar_imagen("img/MAGO_MTMC.png", (250, 250))
personaje_interfaz_hover = cargar_imagen("img/MAGO_MTMC.png", (300, 300))

# Botones de audio
boton_mute = cargar_imagen("img/mute.png", (100, 100))
boton_mute_hover = cargar_imagen("img/mute.png", (120, 120))
boton_unmute = cargar_imagen("img/unmute.png", (100, 100))
boton_unmute_hover = cargar_imagen("img/unmute.png", (120, 120))
boton_vol_up = cargar_imagen("img/vol_up.png", (100, 100))
boton_vol_up_hover = cargar_imagen("img/vol_up.png", (120, 120))
boton_vol_down = cargar_imagen("img/vol_down.png", (100, 100))
boton_vol_down_hover = cargar_imagen("img/vol_down.png", (120, 120))

# ─────────────────────────────────────────────────────────────
# Posiciones y elementos del juego
# ─────────────────────────────────────────────────────────────
rect_ajustes = boton_ajustes.get_rect(topleft=(220, 580))
rect_jugar = boton_jugar.get_rect(topleft=(550, 580))
rect_creditos = boton_creditos.get_rect(topleft=(880, 580))
rect_youtube = boton_youtube.get_rect(topleft=(60, 300))
rect_mago = personaje_interfaz.get_rect(topleft=(1100, 220))

# Botones de audio
X_COLUMNA, Y_COLUMNA, ESPACIO = 20, 100, 120
rect_mute = boton_mute.get_rect(topleft=(X_COLUMNA, Y_COLUMNA))
rect_unmute = boton_unmute.get_rect(topleft=(X_COLUMNA, Y_COLUMNA))
rect_vol_up = boton_vol_up.get_rect(topleft=(X_COLUMNA, Y_COLUMNA + ESPACIO))
rect_vol_down = boton_vol_down.get_rect(topleft=(X_COLUMNA, Y_COLUMNA + ESPACIO * 2))

# Círculos del tablero
circulos = [
    {"centro": (510, 90), "radio": 50, "materia": "Matematicas"},
    {"centro": (385, 175), "radio": 40, "materia": "Sociales"},
    {"centro": (460, 565), "radio": 40, "materia": "Ingles"},
    {"centro": (365, 495), "radio": 40, "materia": "Naturales"},
    {"centro": (325, 265), "radio": 40, "materia": "Español"},
    {"centro": (785, 610), "radio": 40, "materia": "Sociales2"},
    {"centro": (890, 560), "radio": 40, "materia": "Matematicas2"},
    {"centro": (1015, 350), "radio": 40, "materia": "Español2"},
    {"centro": (985, 250), "radio": 40, "materia": "Naturales2"},
    {"centro": (905, 170), "radio": 40, "materia": "Ingles2"},
    {"centro": (685, 130), "radio": 40, "materia": "Sociales3"},
    {"centro": (585, 160), "radio": 40, "materia": "Matematicas3"},
    {"centro": (505, 230), "radio": 40, "materia": "Español3"},
    {"centro": (480, 320), "radio": 40, "materia": "Naturales3"},
    {"centro": (535, 410), "radio": 40, "materia": "Ingles3"},
    {"centro": (630, 460), "radio": 40, "materia": "Sociales4"},
]

ORDEN_RECORRIDO = [
    "Matematicas", "Sociales", "Español", "Naturales", "Ingles",
    "Sociales2", "Matematicas2", "Español2", "Naturales2", "Ingles2",
    "Sociales3", "Matematicas3", "Español3", "Naturales3", "Ingles3", "Sociales4"
]

# Equipos
class Equipo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = mago_personaje
        self.rect = self.image.get_rect(topleft=(x, y))

equipo1 = Equipo(510, 20)
equipo2 = Equipo(420, 20)
grupo_equipos = pygame.sprite.Group(equipo1, equipo2)

# ─────────────────────────────────────────────────────────────
# Estado del juego
# ─────────────────────────────────────────────────────────────
pantalla_actual = "menu"
mostrando_pregunta = False
mostrando_retroalimentacion = False
mensaje_retro = ""
color_retro = BLANCO
datos_pregunta = None
botones_opciones = []
temporizador_retro = 0
tiempo_inicio_pregunta = 0
turno_actual = "equipo1"  # "equipo1" o "equipo2"

# Estados especiales
modo_dibujo_activo = False
superficie_dibujo = None
elementos_organizar = []
indices_seleccionados = []
tiempo_inicio_dibujo = 0
tiempo_inicio_organizar = 0
mostrando_validacion_dibujo = False
mostrando_validacion_organizar = False
preguntas_usadas = set()
musica_activa = True
sonido_fondo = None

try:
    sonido_fondo = pygame.mixer.Sound("Sonidos/Fondo.mp3")
    pygame.mixer.Sound.play(sonido_fondo, loops=-1)
    musica_activa = True
except pygame.error:
    print("No se pudo cargar el sonido de fondo")


# Fuentes
fuente_pregunta = pygame.font.SysFont("Arial", 36, bold=True)
fuente_opciones = pygame.font.SysFont("Arial", 30)
fuente_ayuda = pygame.font.SysFont("Arial", 24)
fuente_tiempo = pygame.font.SysFont("Arial", 36, bold=True)

# ─────────────────────────────────────────────────────────────
# Funciones auxiliares
# ─────────────────────────────────────────────────────────────
def envolver_texto(fuente, texto, ancho_maximo):
    """Divide el texto en líneas que caben en el ancho máximo."""
    palabras = texto.split(" ")
    lineas = []
    actual = ""
    for palabra in palabras:
        prueba = actual + (" " if actual else "") + palabra
        if fuente.size(prueba)[0] <= ancho_maximo:
            actual = prueba
        else:
            if actual:
                lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas

def dibujar_caja_texto(superficie, texto, fuente, centro_x, y, ancho_caja,
                      color_fondo=(50, 50, 50), color_texto=BLANCO,
                      relleno_x=30, relleno_y=18, radio_borde=15):
    """Dibuja un recuadro con texto envuelto y devuelve su rectángulo."""
    ancho_texto = ancho_caja - 2 * relleno_x
    lineas = envolver_texto(fuente, texto, ancho_texto)
    altura_linea = fuente.get_height()
    altura_total = len(lineas) * altura_linea + 2 * relleno_y
    rectangulo = pygame.Rect(centro_x - ancho_caja // 2, y, ancho_caja, altura_total)
    pygame.draw.rect(superficie, color_fondo, rectangulo, border_radius=radio_borde)
    for i, linea in enumerate(lineas):
        superficie_texto = fuente.render(linea, True, color_texto)
        rect_texto = superficie_texto.get_rect(
            center=(centro_x, y + relleno_y + i * altura_linea + altura_linea // 2)
        )
        superficie.blit(superficie_texto, rect_texto)
    return rectangulo

def calcular_altura_texto(fuente, texto, ancho_maximo):
    """Devuelve la altura total del texto envuelto."""
    lineas = envolver_texto(fuente, texto, ancho_maximo)
    return len(lineas) * fuente.get_height()

def cambiar_turno():
    global turno_actual
    turno_actual = "equipo2" if turno_actual == "equipo1" else "equipo1"

# ─────────────────────────────────────────────────────────────
# Bucle principal
# ─────────────────────────────────────────────────────────────
ejecutando = True
while ejecutando:
    reloj.tick(60)
    pos_mouse = pygame.mouse.get_pos()

    # Botón de salir (común en pantallas secundarias)
    rect_boton_salir = None
    if pantalla_actual in ["ajustes", "creditos", "jugar", "mago", "dibujar"]:
        rect_boton_salir = pygame.Rect(pantalla.get_width() - 150, 10, 120, 100)

    # ────────────────────────
    # Manejo de eventos
    # ────────────────────────
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                if mostrando_pregunta or mostrando_retroalimentacion:
                    mostrando_pregunta = False
                    mostrando_retroalimentacion = False
                else:
                    ejecutando = False

        elif evento.type == pygame.VIDEORESIZE:
            pantalla = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
            if pantalla_actual == "dibujar":
                superficie_dibujo = None

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Botón de salir
            if rect_boton_salir and rect_boton_salir.collidepoint(pos_mouse):
                pantalla_actual = "menu"
                mostrando_pregunta = False
                mostrando_retroalimentacion = False
                if pantalla_actual != "dibujar":
                    superficie_dibujo = None

            # Menú principal
            elif pantalla_actual == "menu":
                if rect_ajustes.collidepoint(pos_mouse):
                    pantalla_actual = "ajustes"
                elif rect_jugar.collidepoint(pos_mouse):
                    pantalla_actual = "jugar"
                elif rect_creditos.collidepoint(pos_mouse):
                    pantalla_actual = "creditos"
                elif rect_youtube.collidepoint(pos_mouse):
                    webbrowser.open(URL_YOUTUBE)
                elif rect_mago.collidepoint(pos_mouse):
                    pantalla_actual = "mago"

            # Ajustes de audio
            elif pantalla_actual == "ajustes":
                if musica_activa and rect_mute.collidepoint(pos_mouse):
                    # Silenciar
                    if sonido_fondo:
                        pygame.mixer.Sound.stop(sonido_fondo)
                    musica_activa = False
                elif not musica_activa and rect_unmute.collidepoint(pos_mouse):
                    # Reanudar
                    if sonido_fondo:
                        pygame.mixer.Sound.play(sonido_fondo, loops=-1)
                        musica_activa = True
                    else:
                        print("⚠️ No se pudo cargar el sonido de fondo")
                elif rect_vol_up.collidepoint(pos_mouse) and sonido_fondo:
                    sonido_fondo.set_volume(min(1.0, sonido_fondo.get_volume() + 0.1))
                elif rect_vol_down.collidepoint(pos_mouse) and sonido_fondo:
                    sonido_fondo.set_volume(max(0.0, sonido_fondo.get_volume() - 0.1))

            # Jugar: seleccionar círculo
            elif pantalla_actual == "jugar" and not mostrando_pregunta and not mostrando_retroalimentacion:
                for circulo in circulos:
                    cx, cy = circulo["centro"]
                    radio = circulo["radio"]
                    distancia = ((pos_mouse[0] - cx) ** 2 + (pos_mouse[1] - cy) ** 2) ** 0.5
                    if distancia <= radio:
                        materia_original = circulo["materia"]
                        materia_real = ALIAS_MATERIAS.get(materia_original, materia_original)
                        datos_pregunta = None
                        intentos = 0
                        MAX_INTENTOS = 10
                        while intentos < MAX_INTENTOS:
                            pregunta_temp = obtener_pregunta_aleatoria(materia_real)
                            if not pregunta_temp:
                                break
                            clave = pregunta_temp.get("id") or pregunta_temp.get("pregunta")
                            if clave and clave not in preguntas_usadas:
                                datos_pregunta = pregunta_temp
                                preguntas_usadas.add(clave)
                                break
                            intentos += 1

                        if datos_pregunta:
                            if "imagen" not in datos_pregunta:
                                datos_pregunta["imagen"] = ""
                            if not all(k in datos_pregunta for k in ("pregunta",)):
                                print("⚠️ Pregunta mal formada (falta 'pregunta'):", datos_pregunta)
                                break

                            datos_pregunta["materia"] = materia_original
                            if datos_pregunta.get("actividad") == "dibujar":
                                mostrando_pregunta = True
                                botones_opciones = []
                                tiempo_inicio_pregunta = pygame.time.get_ticks()
                            elif datos_pregunta.get("actividad") == "organizar":
                                if "elementos" not in datos_pregunta and "opciones" in datos_pregunta:
                                    datos_pregunta["elementos"] = datos_pregunta["opciones"]
                                if not all(k in datos_pregunta for k in ("elementos", "respuesta")):
                                    print("⚠️ Pregunta 'organizar' mal formada:", datos_pregunta)
                                    break
                                elementos_organizar = datos_pregunta["elementos"][:]
                                random.shuffle(elementos_organizar)
                                indices_seleccionados = []
                                mostrando_pregunta = True
                                tiempo_inicio_organizar = pygame.time.get_ticks()
                            else:
                                if not all(k in datos_pregunta for k in ("opciones", "respuesta")):
                                    print("⚠️ Pregunta mal formada (faltan opciones o respuesta):", datos_pregunta)
                                    break
                                mostrando_pregunta = True
                                botones_opciones = []
                                tiempo_inicio_pregunta = pygame.time.get_ticks()
                        else:
                            print(f"⚠️ No se pudo cargar pregunta para: {materia_real}")
                        break

            # Modo dibujo: entrar al modo
            elif mostrando_pregunta and datos_pregunta and datos_pregunta.get("actividad") == "dibujar":
                pantalla_actual = "dibujar"
                mostrando_pregunta = False
                tiempo_inicio_dibujo = pygame.time.get_ticks()

            # Modo organizar: intercambiar elementos
            elif mostrando_pregunta and datos_pregunta and datos_pregunta.get("actividad") == "organizar":
                centro_x = ANCHO // 2
                ancho_caja = min(1100, int(ANCHO * 0.8))
                rect_temp = dibujar_caja_texto(
                    pygame.Surface((1, 1)), datos_pregunta["pregunta"], fuente_pregunta,
                    centro_x, 100, ancho_caja, color_fondo=(40, 40, 40),
                    color_texto=BLANCO, relleno_x=40, relleno_y=20, radio_borde=18
                )
                extra_y = 0
                if datos_pregunta.get("imagen") and datos_pregunta["imagen"].strip():
                    try:
                        img_temp = pygame.image.load(datos_pregunta["imagen"]).convert_alpha()
                        extra_y = img_temp.get_height() + 40
                    except:
                        pass
                y_elemento = rect_temp.bottom + extra_y + 30
                ALTURA_MINIMA_OPCION, ESPACIO_OPCION = 60, 20
                clic_procesado = False
                for i, elemento in enumerate(elementos_organizar):
                    altura_texto = calcular_altura_texto(fuente_opciones, f"{i+1}. {elemento}", ancho_caja - 60)
                    altura_real = max(ALTURA_MINIMA_OPCION, altura_texto + 20)
                    rect_boton = pygame.Rect(centro_x - ancho_caja // 2, y_elemento, ancho_caja, altura_real)
                    if rect_boton.collidepoint(pos_mouse):
                        if len(indices_seleccionados) == 0:
                            indices_seleccionados.append(i)
                        elif len(indices_seleccionados) == 1:
                            idx1 = indices_seleccionados[0]
                            idx2 = i
                            elementos_organizar[idx1], elementos_organizar[idx2] = elementos_organizar[idx2], elementos_organizar[idx1]
                            indices_seleccionados = []
                        clic_procesado = True
                        break
                    y_elemento += altura_real + ESPACIO_OPCION

                if not clic_procesado:
                    texto_terminar = fuente_pregunta.render("TERMINAR", True, BLANCO)
                    rect_terminar = texto_terminar.get_rect(center=(ANCHO // 2, ALTO - 80))
                    if rect_terminar.collidepoint(pos_mouse):
                        correcto = elementos_organizar == datos_pregunta["respuesta"]
                        mensaje_retro = "¡Correcto!" if correcto else "Incorrecto"
                        color_retro = (0, 255, 0) if correcto else (255, 0, 0)
                        if correcto:
                            try:
                                idx_actual = ORDEN_RECORRIDO.index(datos_pregunta["materia"])
                                siguiente_materia = ORDEN_RECORRIDO[(idx_actual + 1) % len(ORDEN_RECORRIDO)]
                                equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                                for c in circulos:
                                    if c["materia"] == siguiente_materia:
                                        equipo_actual.rect.center = c["centro"]
                                        break
                            except ValueError:
                                pass
                        cambiar_turno()
                        mostrando_pregunta = False
                        mostrando_retroalimentacion = True
                        temporizador_retro = pygame.time.get_ticks()
                        elementos_organizar = []
                        indices_seleccionados = []

            # Modo dibujo: terminar
            elif pantalla_actual == "dibujar" and not mostrando_validacion_dibujo:
                texto_terminar = fuente_pregunta.render("TERMINAR", True, BLANCO)
                rect_terminar = texto_terminar.get_rect(center=(ANCHO // 2, ALTO - 80))
                if rect_terminar.collidepoint(pos_mouse):
                    mostrando_validacion_dibujo = True
                else:
                    modo_dibujo_activo = True
                    if superficie_dibujo:
                        pygame.draw.circle(superficie_dibujo, NEGRO, evento.pos, 2)
                    ultima_pos = evento.pos

            # Validación dibujo
            elif pantalla_actual == "dibujar" and mostrando_validacion_dibujo:
                rect_correcto = fuente_pregunta.render("CORRECTO", True, BLANCO).get_rect(center=(ANCHO // 2 - 200, ALTO // 2 + 200))
                rect_incorrecto = fuente_pregunta.render("INCORRECTO", True, BLANCO).get_rect(center=(ANCHO // 2 + 200, ALTO // 2 + 200))
                if rect_correcto.collidepoint(pos_mouse):
                    try:
                        idx_actual = ORDEN_RECORRIDO.index(datos_pregunta["materia"])
                        siguiente_materia = ORDEN_RECORRIDO[(idx_actual + 1) % len(ORDEN_RECORRIDO)]
                        equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                        for c in circulos:
                            if c["materia"] == siguiente_materia:
                                equipo_actual.rect.center = c["centro"]
                                break
                    except ValueError:
                        pass
                    cambiar_turno()
                    pantalla_actual = "jugar"
                    superficie_dibujo = None
                    mostrando_validacion_dibujo = False
                elif rect_incorrecto.collidepoint(pos_mouse):
                    cambiar_turno()
                    pantalla_actual = "jugar"
                    superficie_dibujo = None
                    mostrando_validacion_dibujo = False

            # Respuesta en modo selección
            elif mostrando_pregunta and datos_pregunta and datos_pregunta.get("actividad") not in ["dibujar", "organizar"]:
                for rect_boton, idx_opcion in botones_opciones:
                    if rect_boton.collidepoint(pos_mouse):
                        try:
                            idx_respuesta = int(datos_pregunta["respuesta"])
                        except (ValueError, TypeError, KeyError):
                            idx_respuesta = None
                        es_correcto = (idx_respuesta == idx_opcion)
                        mensaje_retro = "¡Correcto!" if es_correcto else "Incorrecto"
                        color_retro = (0, 255, 0) if es_correcto else (255, 0, 0)
                        if es_correcto:
                            try:
                                idx_actual = ORDEN_RECORRIDO.index(datos_pregunta["materia"])
                                siguiente_materia = ORDEN_RECORRIDO[(idx_actual + 1) % len(ORDEN_RECORRIDO)]
                                equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                                for c in circulos:
                                    if c["materia"] == siguiente_materia:
                                        equipo_actual.rect.center = c["centro"]
                                        break
                            except ValueError:
                                pass
                        cambiar_turno()
                        mostrando_pregunta = False
                        mostrando_retroalimentacion = True
                        temporizador_retro = pygame.time.get_ticks()
                        break

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if pantalla_actual == "dibujar":
                modo_dibujo_activo = False
                ultima_pos = None

        elif evento.type == pygame.MOUSEMOTION:
            if pantalla_actual == "dibujar" and modo_dibujo_activo and superficie_dibujo:
                if ultima_pos:
                    pygame.draw.line(superficie_dibujo, NEGRO, ultima_pos, evento.pos, 5)
                else:
                    pygame.draw.circle(superficie_dibujo, NEGRO, evento.pos, 2)
                ultima_pos = evento.pos

    # ────────────────────────
    # Temporizadores
    # ────────────────────────
    tiempo_actual = pygame.time.get_ticks()
    if mostrando_pregunta and datos_pregunta:
        if datos_pregunta.get("actividad") not in ["dibujar", "organizar"]:
            if tiempo_actual - tiempo_inicio_pregunta >= TIEMPO_LIMITE:
                mensaje_retro = "¡Tiempo agotado!"
                color_retro = (255, 0, 0)
                mostrando_pregunta = False
                mostrando_retroalimentacion = True
                temporizador_retro = tiempo_actual
                cambiar_turno()
        elif datos_pregunta.get("actividad") == "organizar":
            if tiempo_actual - tiempo_inicio_organizar >= TIEMPO_LIMITE:
                correcto = elementos_organizar == datos_pregunta["respuesta"]
                mensaje_retro = "¡Correcto!" if correcto else "Tiempo agotado - Incorrecto"
                color_retro = (0, 255, 0) if correcto else (255, 0, 0)
                if correcto:
                    try:
                        idx_actual = ORDEN_RECORRIDO.index(datos_pregunta["materia"])
                        siguiente_materia = ORDEN_RECORRIDO[(idx_actual + 1) % len(ORDEN_RECORRIDO)]
                        equipo_actual = equipo1 if turno_actual == "equipo1" else equipo2
                        for c in circulos:
                            if c["materia"] == siguiente_materia:
                                equipo_actual.rect.center = c["centro"]
                                break
                    except ValueError:
                        pass
                cambiar_turno()
                mostrando_pregunta = False
                mostrando_retroalimentacion = True
                temporizador_retro = tiempo_actual
                elementos_organizar = []
                indices_seleccionados = []

    if pantalla_actual == "dibujar" and not mostrando_validacion_dibujo:
        if tiempo_actual - tiempo_inicio_dibujo >= TIEMPO_LIMITE:
            mostrando_validacion_dibujo = True

    # ────────────────────────
    # Renderizado
    # ────────────────────────
    if pantalla_actual == "menu":
        pantalla.blit(fondo, (-50, -150))
        pantalla.blit(boton_ajustes_hover if rect_ajustes.collidepoint(pos_mouse) else boton_ajustes, rect_ajustes.topleft)
        pantalla.blit(boton_jugar_hover if rect_jugar.collidepoint(pos_mouse) else boton_jugar, rect_jugar.topleft)
        pantalla.blit(boton_creditos_hover if rect_creditos.collidepoint(pos_mouse) else boton_creditos, rect_creditos.topleft)
        pantalla.blit(boton_youtube_hover if rect_youtube.collidepoint(pos_mouse) else boton_youtube, rect_youtube.topleft)
        pantalla.blit(personaje_interfaz_hover if rect_mago.collidepoint(pos_mouse) else personaje_interfaz, rect_mago.topleft)
        pantalla.blit(logo_juego, (400, 40))

    elif pantalla_actual == "ajustes":
        pantalla.blit(fondo, (-50, -150))
        titulo = pygame.font.SysFont(None, 60).render("AJUSTES", True, NEGRO)
        pantalla.blit(titulo, (pantalla.get_width() // 2 - titulo.get_width() // 2, 30))
        if rect_boton_salir:
            pantalla.blit(boton_salir_hover if rect_boton_salir.collidepoint(pos_mouse) else boton_salir, rect_boton_salir.topleft)
        if musica_activa:
            pantalla.blit(boton_mute_hover if rect_mute.collidepoint(pos_mouse) else boton_mute, rect_mute.topleft)
        else:
            pantalla.blit(boton_unmute_hover if rect_unmute.collidepoint(pos_mouse) else boton_unmute, rect_unmute.topleft)
        pantalla.blit(boton_vol_up_hover if rect_vol_up.collidepoint(pos_mouse) else boton_vol_up, rect_vol_up.topleft)
        pantalla.blit(boton_vol_down_hover if rect_vol_down.collidepoint(pos_mouse) else boton_vol_down, rect_vol_down.topleft)

    elif pantalla_actual == "jugar":
        pantalla.blit(tablero, (0, 0))
        color_turno = ROJO_MAT if turno_actual == "equipo1" else MORADO_IN
        texto_turno = fuente_pregunta.render(f"Turno: {turno_actual.upper()}", True, color_turno)
        pantalla.blit(texto_turno, (10, 10))

        for circulo in circulos:
            centro = circulo["centro"]
            radio = circulo["radio"]
            materia = circulo["materia"]
            color = MATERIAS.get(materia, (100, 100, 100))
            #pygame.draw.circle(pantalla, color, centro, radio)
            #texto_materia = fuente_ayuda.render(materia, True, NEGRO)
            #pantalla.blit(texto_materia, (centro[0] - texto_materia.get_width() // 2, centro[1] - 8))

        grupo_equipos.draw(pantalla)

        if rect_boton_salir:
            pantalla.blit(boton_salir_hover if rect_boton_salir.collidepoint(pos_mouse) else boton_salir, rect_boton_salir.topleft)

        if mostrando_pregunta and datos_pregunta:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))

            titulo_materia = fuente_pregunta.render(f"{datos_pregunta['materia']}", True, MATERIAS.get(datos_pregunta['materia'], BLANCO))
            pantalla.blit(titulo_materia, (ANCHO // 2 - titulo_materia.get_width() // 2, 40))

            centro_x = ANCHO // 2
            ancho_caja = min(1100, int(ANCHO * 0.8))

            rect_pregunta = dibujar_caja_texto(
                pantalla, datos_pregunta["pregunta"], fuente_pregunta,
                centro_x, 100, ancho_caja,
                color_fondo=(40, 40, 40), color_texto=BLANCO,
                relleno_x=40, relleno_y=20, radio_borde=18
            )

            extra_y = 0
            if datos_pregunta.get("imagen") and datos_pregunta["imagen"].strip():
                try:
                    imagen = pygame.image.load(datos_pregunta["imagen"]).convert_alpha()
                    ancho_max_img = ancho_caja - 40
                    alto_max_img = 400
                    ancho_img, alto_img = imagen.get_size()
                    if ancho_img > ancho_max_img or alto_img > alto_max_img:
                        escala = min(ancho_max_img / ancho_img, alto_max_img / alto_img)
                        nuevo_tam = (int(ancho_img * escala), int(alto_img * escala))
                        imagen = pygame.transform.scale(imagen, nuevo_tam)
                        alto_img = nuevo_tam[1]
                    else:
                        alto_img = imagen.get_height()
                    y_imagen = rect_pregunta.bottom + 20
                    pantalla.blit(imagen, (centro_x - imagen.get_width() // 2, y_imagen))
                    extra_y = alto_img + 40
                except Exception as e:
                    print(f"❌ ERROR al cargar imagen: {datos_pregunta['imagen']} - {e}")

            # Modo dibujo
            if datos_pregunta.get("actividad") == "dibujar":
                mensaje = fuente_ayuda.render("Haz clic en cualquier lugar para entrar al modo dibujo", True, (100, 200, 255))
                pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO - 100))

            # Modo organizar
            elif datos_pregunta.get("actividad") == "organizar":
                y_elemento = rect_pregunta.bottom + extra_y + 30
                ALTURA_MINIMA_OPCION, ESPACIO_OPCION = 60, 20
                for i, elemento in enumerate(elementos_organizar):
                    altura_texto = calcular_altura_texto(fuente_opciones, f"{i+1}. {elemento}", ancho_caja - 60)
                    altura_real = max(ALTURA_MINIMA_OPCION, altura_texto + 20)
                    rect_boton = pygame.Rect(centro_x - ancho_caja // 2, y_elemento, ancho_caja, altura_real)
                    esta_sobre = rect_boton.collidepoint(pos_mouse)
                    esta_seleccionado = (i in indices_seleccionados)
                    color_fondo = (120, 120, 255) if esta_seleccionado else (100, 100, 100) if esta_sobre else (50, 50, 50)
                    pygame.draw.rect(pantalla, color_fondo, rect_boton, border_radius=12)
                    lineas = envolver_texto(fuente_opciones, f"{i+1}. {elemento}", ancho_caja - 60)
                    for j, linea in enumerate(lineas):
                        superficie_texto = fuente_opciones.render(linea, True, BLANCO)
                        rect_texto = superficie_texto.get_rect(
                            centerx=rect_boton.centerx,
                            top=rect_boton.top + 10 + j * fuente_opciones.get_height()
                        )
                        pantalla.blit(superficie_texto, rect_texto)
                    y_elemento += altura_real + ESPACIO_OPCION

                texto_terminar = fuente_pregunta.render("TERMINAR", True, BLANCO)
                rect_terminar = texto_terminar.get_rect(center=(ANCHO // 2, ALTO - 80))
                color_boton = (200, 0, 0) if rect_terminar.collidepoint(pos_mouse) else (255, 0, 0)
                pygame.draw.rect(pantalla, color_boton, rect_terminar.inflate(40, 20), border_radius=15)
                pantalla.blit(texto_terminar, rect_terminar)

                tiempo_restante = max(0, (TIEMPO_LIMITE - (tiempo_actual - tiempo_inicio_organizar)) // 1000)
                texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 0))
                pantalla.blit(texto_tiempo, (1150, 0))

            # Modo selección normal
            else:
                y_base_opciones = rect_pregunta.bottom + extra_y + 30
                tiene_imagen = bool(datos_pregunta.get("imagen") and datos_pregunta["imagen"].strip())

                if tiene_imagen:
                    # Layout 2x2
                    ancho_opcion = (ancho_caja - 60) // 2
                    alto_opcion, espacio = 70, 20
                    botones_opciones.clear()
                    for i, opcion in enumerate(datos_pregunta["opciones"]):
                        columna = i % 2
                        fila = i // 2
                        x_opcion = centro_x - ancho_opcion - espacio // 2 + columna * (ancho_opcion + espacio)
                        y_opcion = y_base_opciones + fila * (alto_opcion + espacio)
                        rect_boton = pygame.Rect(x_opcion, y_opcion, ancho_opcion, alto_opcion)
                        esta_sobre = rect_boton.collidepoint(pos_mouse)
                        color_fondo = (120, 120, 120) if esta_sobre else (60, 60, 60)
                        pygame.draw.rect(pantalla, color_fondo, rect_boton, border_radius=12)
                        texto = fuente_opciones.render(f"{i+1}. {opcion}", True, BLANCO)
                        pantalla.blit(texto, texto.get_rect(center=rect_boton.center))
                        botones_opciones.append((rect_boton, i))
                    y_mensaje = y_base_opciones + 2 * (alto_opcion + espacio) + 10
                else:
                    # Layout vertical
                    y_opcion = y_base_opciones
                    botones_opciones.clear()
                    alto_opcion = 60
                    for i, opcion in enumerate(datos_pregunta["opciones"]):
                        rect_boton = pygame.Rect(centro_x - ancho_caja // 2, y_opcion, ancho_caja, alto_opcion)
                        esta_sobre = rect_boton.collidepoint(pos_mouse)
                        color_fondo = (120, 120, 120) if esta_sobre else (60, 60, 60)
                        pygame.draw.rect(pantalla, color_fondo, rect_boton, border_radius=12)
                        texto = fuente_opciones.render(f"{i+1}. {opcion}", True, BLANCO)
                        pantalla.blit(texto, texto.get_rect(center=rect_boton.center))
                        botones_opciones.append((rect_boton, i))
                        y_opcion += alto_opcion + 20
                    y_mensaje = y_opcion + 10

                mensaje = fuente_ayuda.render("Haz clic en tu opción", True, (100, 200, 255))
                pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, y_mensaje))

                tiempo_restante = max(0, (TIEMPO_LIMITE - (tiempo_actual - tiempo_inicio_pregunta)) // 1000)
                texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 0))
                pantalla.blit(texto_tiempo, (1150, 0))

        if mostrando_retroalimentacion:
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(200)
            overlay.fill(NEGRO)
            pantalla.blit(overlay, (0, 0))
            fuente_grande = pygame.font.SysFont("Arial", 72, bold=True)
            texto = fuente_grande.render(mensaje_retro, True, color_retro)
            rect_texto = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
            pantalla.blit(texto, rect_texto)
            instruccion = fuente_ayuda.render("Cerrando en 1 segundo...", True, BLANCO)
            pantalla.blit(instruccion, (ANCHO // 2 - instruccion.get_width() // 2, ALTO // 2 + 60))

    elif pantalla_actual == "creditos":
        pantalla.blit(fondo, (-50, -150))
        texto = pygame.font.SysFont(None, 60).render("Créditos", True, NEGRO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 30))
        if rect_boton_salir:
            pantalla.blit(boton_salir_hover if rect_boton_salir.collidepoint(pos_mouse) else boton_salir, rect_boton_salir.topleft)

    elif pantalla_actual == "mago":
        pantalla.fill(CELESTE)
        fuente = pygame.font.SysFont(None, 60)
        texto1 = fuente.render("¡Hola, soy el Mago MTMC!", True, NEGRO)
        texto2 = fuente_ayuda.render("Estoy aquí para ayudarte a aprender.", True, NEGRO)
        pantalla.blit(texto1, (ANCHO // 2 - texto1.get_width() // 2, ALTO // 2 - 60))
        pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2))
        if rect_boton_salir:
            pantalla.blit(boton_salir_hover if rect_boton_salir.collidepoint(pos_mouse) else boton_salir, rect_boton_salir.topleft)

    elif pantalla_actual == "dibujar":
        if superficie_dibujo is None:
            superficie_dibujo = pygame.Surface((ANCHO, ALTO))
            superficie_dibujo.fill(BLANCO)
        if not mostrando_validacion_dibujo:
            pantalla.fill(BLANCO)
            pantalla.blit(superficie_dibujo, (0, 0))
            texto = fuente_pregunta.render("Modo Dibujo - Mantén presionado el clic para dibujar", True, NEGRO)
            pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 20))
            tiempo_restante = max(0, (TIEMPO_LIMITE - (tiempo_actual - tiempo_inicio_dibujo)) // 1000)
            texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 0, 0))
            pantalla.blit(texto_tiempo, (1150, 10))
            texto_terminar = fuente_pregunta.render("TERMINAR", True, BLANCO)
            rect_terminar = texto_terminar.get_rect(center=(ANCHO // 2, ALTO - 80))
            color_boton = (200, 0, 0) if rect_terminar.collidepoint(pos_mouse) else (255, 0, 0)
            pygame.draw.rect(pantalla, color_boton, rect_terminar.inflate(40, 20), border_radius=15)
            pantalla.blit(texto_terminar, rect_terminar)
        else:
            texto_titulo = fuente_pregunta.render("Considera que la respuesta es correcta", True, ROJO_MAT)
            pantalla.blit(texto_titulo, texto_titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 80)))
            boton_correcto = fuente_pregunta.render("CORRECTO", True, BLANCO)
            rect_correcto = boton_correcto.get_rect(center=(ANCHO // 2 - 200, ALTO // 2 + 200))
            color_correcto = (0, 200, 0) if rect_correcto.collidepoint(pos_mouse) else (0, 255, 0)
            pygame.draw.rect(pantalla, color_correcto, rect_correcto.inflate(40, 30), border_radius=15)
            pantalla.blit(boton_correcto, rect_correcto)
            boton_incorrecto = fuente_pregunta.render("INCORRECTO", True, BLANCO)
            rect_incorrecto = boton_incorrecto.get_rect(center=(ANCHO // 2 + 200, ALTO // 2 + 200))
            color_incorrecto = (200, 0, 0) if rect_incorrecto.collidepoint(pos_mouse) else (255, 0, 0)
            pygame.draw.rect(pantalla, color_incorrecto, rect_incorrecto.inflate(40, 30), border_radius=15)
            pantalla.blit(boton_incorrecto, rect_incorrecto)

    # Cerrar retroalimentación
    if mostrando_retroalimentacion and tiempo_actual - temporizador_retro > 1000:
        mostrando_retroalimentacion = False

    pygame.display.flip()

pygame.quit()
sys.exit()