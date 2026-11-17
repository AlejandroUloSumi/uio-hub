"""
UIO Hub v31 — Hub ajustado: menos aire en los laterales y abajo.

CAMBIOS v31 (los pedidos de esta ronda, sobre la captura de pantalla):
  v31a MENOS AIRE LATERAL: la ventana tenía un ancho mínimo de 110px
    heredado de la época de DOS columnas; con el hub de UNA columna los
    iconos piden ~62px y esos ~48px sobrantes quedaban repartidos a los
    lados (~23px por lado). Ahora el piso es 64px y además se ajustó el
    padding interno: celdas de la grilla 3→2px, cabecera 10→8px y pie
    6→4px. Los iconos quedan a ~7px del borde de la ventana.
  v31b MENOS ESPACIO ABAJO: el aire debajo del botón de Configuración
    baja de 6px a 4px y el que rodea la línea del pie se achica 1px.
  v31c ARRANQUE VISIBLE MÁS ROBUSTO: el refresco de estilo de la ventana
    ya no usa el par withdraw/deiconify (en el arranque de Windows podía
    dejar el dock escondido: "solo el icono de la bandeja") sino
    SetWindowPos con FRAMECHANGED (refresca sin ocultar). Y el
    "asegurar visible" ahora también CLAVA la posición dentro del área
    útil del monitor (si guardó la posición de un monitor desconectado
    la ventana quedaba fuera de pantalla) y fuerza primer plano en 3
    intentos (~1 s, ~3 s, ~5 s), siempre respetando el ✕ del usuario.
  Todo lo demás queda exactamente igual que en v30.

CAMBIOS v30 (ronda anterior):
  v30a BOTONES RETIRADOS: OmniRoute, DeepSeek Harness y el Chat del pie
    ya no existen (el usuario dejó de usarlos). El dock queda con
    Proyectos, Drive, Notion y Tasks + el engranaje de Configuración.
    Con los botones se retira todo su aparato: barra lateral de chat,
    foco de pestaña DSH por CDP, indicadores de servicio, monitoreo de
    procesos y la sección DSH completa de Configuración. Las funciones
    internas quedan dormidas por si el chat vuelve algún día.
  v30b CHROME NORMAL POR DEFECTO: los botones web (Drive / Notion /
    Tasks y cualquier botón web propio) abren en la sesión de Google
    Chrome de SIEMPRE (el perfil de todos los días), no en el Chrome
    dedicado con perfil aparte. La casilla "Usar Chrome dedicado para
    DSH" y sus botones desaparecen de Configuración.
  v30c UNA SOLA COLUMNA: los iconos ya no van en dos columnas; quedan
    apilados en UNA columna centrada y un poco más grandes (46 → 52 px,
    el pie también) para que el dock se vea como un hub vertical.
  v30d Marcadores de versión y logs actualizados a v30.

CAMBIOS v29 (ronda anterior):
  v29a DSH TAMPOCO SE AUTO-INICIA: se elimina la casilla "Auto-iniciar DSH
    Web" y su comportamiento. NINGÚN servicio arranca solo: OmniRoute y
    DeepSeek Harness se levantan ÚNICAMENTE al apretar su botón (clic →
    PowerShell). Motivo: el nuevo DeepSeek Harness tiene app propia y ya
    no hace falta un servidor encendido de fondo todo el día.
  v29b EL DOCK NACE VISIBLE: al abrir el programa (a mano o con el
    arranque de Windows) el dock se ve en pantalla directamente. Si el
    arranque de Windows lo dejaba escondido (Explorer lento al prender la
    PC: el hub "solo estaba" en los iconos ocultos de la bandeja), ahora
    se re-muestra solo a los ~1 s y ~3 s. La bandeja sigue igual: clic
    izquierdo muestra/oculta, ✕ oculta a la bandeja, menú → Salir.
  v29c Marcadores de versión y logs actualizados a v29.

CAMBIOS v28 (los 2 pedidos de esta ronda):
  v28a OMNIROUTE YA NO SE AUTO-INICIA: abrir la aplicación (a mano o con
    el arranque de Windows) NO levanta OmniRoute. El servicio arranca
    ÚNICAMENTE cuando se aprieta su botón (indicador y tooltip siguen
    mostrando su estado real igual que antes).
  v28b DEEPSEEK HARNESS SIEMPRE HABILITADO: se elimina la condición
    "el botón DSH requiere OmniRoute corriendo". El botón DSH nace
    habilitado junto con el programa, funciona siempre y, si la casilla
    "Auto-iniciar DSH Web" está marcada (lo está por defecto), el
    servidor DSH arranca junto con el programa sin depender de Omni.
    - Sin Omni: el botón DSH abre el asistente igual que siempre
      (mismo "foco total": pestaña existente → foco; si no existe →
      nueva pestaña; servidor caído → lo levanta).
    - La casilla "Auto-iniciar OmniRoute" desaparece de Configuración
      (ya no tiene sentido); "Auto-iniciar DSH Web" queda y ya no
      depende del auto-arranque con Windows.
  Todo lo demás queda exactamente igual (bandeja del sistema, navegador
  sin duplicados, chat, iconos personalizados, instalador, etc.).

CAMBIOS v27 (ronda anterior):
  v27a NAVEGADOR SIN DUPLICADOS: el Chrome dedicado tarda 2-5 s en
    arrancar y en ese lapso el puerto de depuración (CDP) todavía no
    responde; antes, cada clic durante el arranque creía que "no había
    nada abierto" y lanzaba OTRO Chrome → ventana nueva en vez de
    pestaña. Y el foco por título de ventana (que solo ve la pestaña
    ACTIVA de cada ventana) abría la pestaña DSH duplicada cuando no
    era la activa. Ahora:
    - cdp_wait_ready() / cdp_tabs_smart(): si el Chrome se lanzó hace
      poco (marca de hora en cada lanzamiento), se ESPERA a que el
      puerto de depuración responda (hasta ~10 s) antes de decidir.
    - Antes de abrir una pestaña DSH "nueva" se reintenta CDP una
      última vez: si el Chrome ya vive, la pestaña se abre por CDP
      (cero duplicados, cero ventanas extra).
    Resultado: 1er clic sin nada abierto → ventana nueva (correcto);
    todos los demás clics → pestañas en ESA ventana y foco directo.
  v27b BANDEJA DEL SISTEMA: el dock deja de aparecer en la barra de
    tareas (WS_EX_TOOLWINDOW sobre el HWND raíz) y pasa a vivir como
    las apps "de segundo plano": icono en la zona de notificaciones.
    - Clic IZQUIERDO en el icono → mostrar / ocultar el dock.
    - Clic DERECHO → menú: "Mostrar / ocultar UIO Hub" y "Salir".
    - El ✕ del dock ahora OCULTA a la bandeja (muestra un globo la
      primera vez); el "Salir" real está en el menú del icono.
    - Hecho 100% con ctypes (Shell_NotifyIconW + ventana oculta propia
      en un hilo aparte): cero dependencias nuevas, mismo .exe.
    - Si Explorer se reinicia, el icono se re-agrega solo
      (mensaje "TaskbarCreated").
    - Config: "tray_enabled": true (por defecto). Nota: la zona de
      "iconos ocultos" (el chevron ^) la controla Windows: el icono se
      puede ARRASTRAR ahí, o configurarlo en Configuración de la barra
      de tareas → "Otros iconos de la bandeja".

CAMBIOS v26 (ronda anterior):
  v26a ICONOS PERSONALIZADOS INTERNALIZADOS: los 9 iconos de fábrica ya
    viajaban dentro del programa (v25c), pero los PNG que el USUARIO
    asigna a los botones (Configuración → Botones → Editar → icono)
    seguían guardando la RUTA del archivo original: si ese archivo se
    movía o borraba, el botón perdía su icono. Ahora, al elegir un
    icono, el programa guarda AUTOMÁTICAMENTE una COPIA en su propia
    carpeta "iconos_guardados" (junto al programa) y la config guarda
    ESA copia: mover o borrar el original ya no afecta a ningún botón.
    - Al arrancar, migrar_iconos_internos() hace lo mismo con los iconos
      YA asignados con versiones anteriores (una sola vez, si el archivo
      original todavía existe; los que ya se perdieron hay que reasig-
      narlos una vez y quedan protegidos para siempre).
    - La copia usa nombre fijo por CONTENIDO (ico_<huella>.png): el
      mismo archivo nunca se duplica y re-guardar un botón no genera
      copias nuevas.
    - Nota para el .exe: la carpeta "iconos_guardados" vive junto al
      programa (igual que uio_hub_config.json). Si movés el programa,
      mové la carpeta entera.

CAMBIOS v25 (ronda anterior):
  v25a BOTÓN DE ENVIAR SÓLIDO: alrededor del círculo de enviar se veía un
    CUADRADO más oscuro que dejaba ver el escritorio (el icono de Windows
    detrás). Causa real: la cara horneada y su overlay usaban el color
    mágico de transparencia del panel (#010101 → -transparentcolor) y en
    Windows esos píxeles se vuelven AGUJEROS al escritorio (en las
    capturas de prueba no se veía porque ahí #010101 ≈ fondo negro).
    Ahora la cara (círculo normal/hover + píldora) se hornea con fondo
    OPACO del color del cuerpo de la barra (PANEL_BG #181818) y el
    overlay usa ese mismo color: el cuadrado se funde con la barra.
  v25b CHAT PEGADO: CHAT_DOCK_GAP 2px → 0px (la barra toca el borde del
    dock; con el cuadrado transparente eliminado, la separación visible
    desaparece por completo).
  v25c ICONOS EMBEBIDOS: los 9 PNG de fábrica viajan DENTRO del propio
    .py en base64 (EMBEDDED_ICONS). Orden de carga: PNG personalizado
    (Configuración) → PNG en disco → EMBEBIDO. Además ensure_builtin_
    icons() restaura a disco los PNG que falten al arrancar
    (auto-reparación) y las previsualizaciones de Configuración también
    caen al embebido. Compilar el .exe ya NO necesita los PNG sueltos:
    todo va dentro del programa.

CAMBIOS v24 (los 3 pedidos de esta ronda):
  v24a SEPARADORES IGUALES Y CON AIRE:
    - MISMO ANCHO: la línea de abajo quedó más corta que la de arriba
      (padx fijos distintos + márgenes que no escalan igual). Ahora el
      ancho de la línea del pie se SINCRONIZA en vivo con la línea de
      arriba (se mide en pantalla la extensión real de sep_frame y se le
      copia): ambas van exactamente de punta a punta de los iconos, a
      cualquier escala / DPI.
    - PEQUEÑA SEPARACIÓN de los botones: las dos líneas estaban pegadas
      a la fila de abajo (la de arriba a Proyectos/Drive, la de abajo a
      Chat/Configuración). Ahora el aire alrededor de cada línea escala
      con ui_scale: pady (3·s arriba, 5·s abajo) en ambas → separación
      chica pero claramente visible, simétrica y prolija.
  v24b ARO EN EL CONTORNO DEL BOTÓN: al abrir el chat se iluminaba el
    borde del ICONO (el aro iba horneado dentro del tile PNG). Ahora el
    aro UIO Blue de 2px es un MARCO EXTERNO (CTkFrame) que rodea el botón
    ENTERO: es el contorno real del botón el que se ilumina, con las
    esquinas concéntricas (radio 12 sobre el radio 10 del botón). El
    icono NO cambia nada (ni imagen, ni tamaño, ni color) al abrir/cerrar.

CAMBIOS v23 (ronda anterior):
  v23a SEPARADORES: la línea sutil que dividía la fila Omni+DeepSeek del
    resto HABÍA DEJADO DE DIBUJARSE (era un CTkFrame de 1px que CustomTk-
    inter 6.x ya no pinta: quedaba del color del fondo, invisible). Ahora
    los separadores son tk.Frame de 1px REALES (píxel exacto, siempre se
    dibuja) y usan un color de la PALETA: #343434, el mismo aro de los
    iconos. Son DOS: uno después de la fila Omni+DSH (el de siempre, otra
    vez visible) y uno NUEVO entre los botones de arriba y el pie (Chat /
    Configuración), igual de pequeño y sutil.
  v23b CHAT PEGADO AL DOCK: el panel del chat se desplegaba a 6px del
    dock; ahora queda a 2px, "casi pegado" pero sin llegar a superponerse
    (también en el lado derecho cuando no hay lugar a la izquierda).
  v23c (reemplazado por v24b: el aro horneado en el icono pasó a la
    historia — ahora es el marco externo del botón).

CAMBIO v22a (paleta unificada del chat): el cuadro de texto y el panel
  del chat usaban una paleta azulada distinta (#202428/#25292D/#33373A)
  que se veía "otra cosa" junto al dock. Ahora el chat usa EXACTAMENTE la
  misma paleta del dock: fondo #181818, campo de texto #2A2A2A (el mismo
  color de los botones del dock) y borde #343434 (el mismo aro de los
  iconos). También los tooltips pasaron al gris neutro. El botón de
  enviar se conserva en UIO Blue #A1B2C3 (color de identidad que YA es
  parte de la paleta: es el mismo del aro del chat abierto).

CAMBIO v22b (tarjetas en Configuración → "Botones"): la lista de puro
  texto se reemplaza por TARJETAS, una por botón, con espaciado prolijo.
  Cada tarjeta muestra apilado: "BOTÓN N", el NOMBRE del botón y su TIPO
  (shell / web / carpeta / pie), con el icono REAL del botón a la
  izquierda. Clic selecciona (aro UIO Blue), doble clic edita. Todo lo
  demás de v21 sigue igual (Agregar/Editar/Eliminar/Restablecer).

CAMBIO v22a (paleta unificada del chat): el cuadro de texto y el panel
  del chat usaban una paleta azulada distinta (#202428/#25292D/#33373A)
  que se veía "otra cosa" junto al dock. Ahora el chat usa EXACTAMENTE la
  misma paleta del dock: fondo #181818, campo de texto #2A2A2A (el mismo
  color de los botones del dock) y borde #343434 (el mismo aro de los
  iconos). También los tooltips pasaron al gris neutro. El botón de
  enviar se conserva en UIO Blue #A1B2C3 (color de identidad que YA es
  parte de la paleta: es el mismo del aro del chat abierto).

CAMBIO v22b (tarjetas en Configuración → "Botones"): la lista de puro
  texto se reemplaza por TARJETAS, una por botón, con espaciado prolijo.
  Cada tarjeta muestra apilado: "BOTÓN N", el NOMBRE del botón y su TIPO
  (shell / web / carpeta / pie), con el icono REAL del botón a la
  izquierda. Clic selecciona (aro UIO Blue), doble clic edita. Todo lo
  demás de v21 sigue igual (Agregar/Editar/Eliminar/Restablecer).

CAMBIO v21a (Configuración unificada): antes había DOS pestañas ("Iconos"
  y "Custom"): la primera solo cambiaba el PNG de los botones fijos y la
  segunda solo listaba los personalizados. Ahora hay UNA pestaña "Botones"
  que lista TODO el dock en orden: los 6 del sistema (OmniRoute, DSH
  Harness, Proyectos, Drive, Notion, Tasks) + los personalizados + los 2
  del pie (Chat y Configuración). Cada uno se EDITA con doble clic o con
  el botón Editar:
  - Botones del sistema: nombre, DESTINO (la URL o carpeta a la que
    saltan — ya no están obligados a la pantalla principal de la
    plataforma) e icono PNG. NO se pueden eliminar (son parte del dock),
    pero "↺ Restablecer" devuelve nombre/destino/icono originales.
  - Botones personalizados: igual que siempre (nombre, tipo, destino,
    icono, Chrome) + se pueden AGREGAR ("➕ Agregar botón nuevo") y
    ELIMINAR ("🗑️ Eliminar").
  - Chat y Configuración (pie): se les puede cargar icono PNG propio
    (ideal para íconos hechos con la paleta del programa).
  Los cambios se aplican al pulsar Guardar.

CAMBIO v21b (persistencia): nuevas claves en uio_hub_config.json —
  "base_labels" {id: nombre} y "base_targets" {id: destino} guardan las
  personalizaciones de los botones del sistema; "custom_icons" sigue
  guardando los PNG (incluidos chat/settings del pie). Retrocompatible:
  sin esas claves todo funciona como v20.

Heredado de v20: chat 470x92 con campo 68 (fijo), flecha ➤ a la derecha,
  píldora "↗ Ir a Harness" flotante que NO cambia la geometría, fila
  "Agregar/Edituar/Eliminar" siempre visible.
Heredado de v19: íconos que siempre cargan (recoloreado con detalle +
  reservas dibujadas burbuja/engranaje), cara del botón horneada con PIL
  (sin depender de fuentes), marcador de versión.
Heredado de v18: sin cuadrado sobre Omni (glifo ◉ integrado), placeholder,
  ✓ Mensaje enviado, slide 180ms.

NOTA: si en pantalla todavía se ve otra cosa, TODAVÍA está corriendo otra
  versión (el auto-arranque de Windows guarda la ruta EXACTA del .py).
  Verificar: pasar el mouse por los tres puntitos "•••" del dock → dice
  "UIO Hub v26". Solución en el paso a paso de la entrega (re-activar el
  auto-arranque desde esta versión).

Requisito:  pip install customtkinter   (y Pillow para los iconos)
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import json
import socket
import threading
import time
import math
import re
from pathlib import Path
import uuid
import urllib.request
import urllib.error
import urllib.parse
import ctypes

# ---------- CUSTOMTKINTER (capa visual) ----------
try:
    import customtkinter as ctk
except ImportError:
    import tkinter as _tk
    from tkinter import messagebox as _mb
    _root_err = _tk.Tk(); _root_err.withdraw()
    _mb.showerror(
        "UIO Hub",
        "Falta la librería CustomTkinter.\n\n"
        "Instalala una sola vez con:\n\n"
        "    pip install customtkinter")
    sys.exit(1)

# El look se calibró 1:1 (botones 48x48, panel 400px). Se fija la escala de
# CTk en 1.0 para que el DPI de Windows no agrande los widgets ni rompa el
# ajuste de tamaño de la ventana (refit_window).
ctk.set_appearance_mode("dark")
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

# ---------- CONSTANTES ----------
TRANSPARENT = "#010101"
BORDER      = "#3a3a3a"
BG_MAIN     = "#181818"
HEADER_BG   = "#222222"
BG_POPUP    = "#121212"
BTN_BG      = "#2a2a2a"
BTN_HOVER   = "#323538"          # v17 guía §9: hover sutil (era #3a3a3a)
BTN_PRESSED = "#242628"          # v17 guía §20: estado presionado
BLINK_BG    = "#6b5a1c"
ICON_LIGHT  = (224, 224, 224)
# Tamaños del dock — v30: UNA columna con iconos un poco más grandes
# (46 → 52 px, pedido del usuario: "que parezca un hub").
BTN_SIZE   = 52
ICON_SIZE  = 52            # el icono ocupa el botón COMPLETO (v14)
FOOT_SIZE  = 52
FOOT_ICON  = 52            # v17: icono a botón completo; el aro va DENTRO del tile
CORNER_R   = 16            # radio del dock (guía §44: 15-17)
BTN_RADIUS = 10            # radio de botón e icono (guía §44: 10-11)
TILE_RING  = "#343434"     # anillo exterior sutil de cada icono (guía §7)
UIO_BLUE   = "#a1b2c3"     # color de identidad UIO (guía §10): foco/selección
# v23a: separadores = MISMO color de paleta que el aro de los iconos
# (#343434). El viejo #303030 era "otra" capa gris fuera de la paleta.
SEP_COLOR  = TILE_RING      # separadores sutiles (guía §13, color de paleta)
IND_OFF    = "#666666"     # indicador de estado apagado (guía §14)
DSH_DIM_FACE = "#232323"   # cara del botón D atenuado (guía §15)
# Barra de chat lateral — v20: el usuario pidió VOLVER al cuadro de texto
# anterior (el de 470x92 con campo de 68px, fijo). Se conservan el
# placeholder, el "✓ Mensaje enviado", el slide suave y la letra 13 INTACTA
# (aprobada por el usuario — no tocar).
CHAT_BAR_W     = 470       # ancho anterior (v15-v17), pedido expreso del usuario
CHAT_BAR_H     = 92        # alto anterior (v15-v17): caben 2+ líneas visibles
CHAT_BAR_H_MAX = 92        # = CHAT_BAR_H → el crecimiento multilínea queda APAGADO
CHAT_LINE_H    = 20        # (sin uso con el crecimiento apagado; se conserva)
CHAT_BAR_R     = 12        # radio coherente con los botones (guía §44)
CHAT_TXT_H     = 68        # alto del campo de escritura anterior (≈3 líneas)
CHAT_FONT      = 13        # INTACTO: tamaño aprobado por el usuario (no tocar)
SEND_BTN       = 46        # botón de enviar circular (aprobado v15)
CHAT_SLIDE_MS  = 180       # deslizamiento lateral al abrir/cerrar
CHAT_SLIDE_PX  = 28        # recorrido lateral del slide (sale del dock)
CHAT_DOCK_GAP  = 0         # v25: PEGADO al dock (2px de v23b aún se notaba)
# v24b: grosor del aro EXTERNO del chat abierto. Ya no se hornea dentro
# del tile del icono: es un marco que rodea el CONTORNO REAL del botón
# (2px = el "un poquito más gruesa, pero muy levemente" de v23c).
CHAT_RING_PX   = 2

ACCENT       = "#4ade80"   # verde SOLO de estado (v17: servicios/captura)
ACCENT_HOVER = "#22c55e"
ACCENT_TEXT  = "#07130a"
# v22a: el chat usa EXACTAMENTE la misma paleta del dock (pedido del
# usuario: "que utilice la misma paleta, parecía otra cosa").
PANEL_BG     = BG_MAIN      # fondo de la barra de chat = fondo del dock (#181818)
CHAT_BORDER  = TILE_RING    # borde del chat = mismo aro de los iconos (#343434)
PANEL_BG_RGBA = (24, 24, 24, 255)  # v25: PANEL_BG en RGBA — fondo OPACO de las
                                   # caras horneadas (enviar + píldora): antes
                                   # eran transparentes y Windows las volvía
                                   # agujeros al escritorio (-transparentcolor)
INPUT_BG     = BTN_BG       # campo de texto = mismo color de los botones (#2a2a2a)
SEND_BG      = UIO_BLUE    # guía §29: acción con el color de identidad (v22: se
                          # conserva — YA es parte de la paleta, es el aro
                          # del chat abierto en el pie)
SEND_HOVER   = "#b7c5d3"
SEND_TEXT    = "#10141a"   # texto oscuro sobre UIO Blue (fondo claro)
SEND_TEXT_RGBA = (16, 20, 26, 255)   # v19: mismo color para las flechas PIL
SEND_BG_RGBA   = (161, 178, 195, 255)  # v19: UIO Blue en RGBA (caras horneadas)
SEND_HOVER_RGBA = (183, 197, 211, 255)  # v19: hover de la cara horneada

# ---------- v21: definición ÚNICA de los botones del sistema ----------
# La usan el dock (build_grid) y la Configuración (pestaña "Botones") para
# que ambas vean SIEMPRE los mismos nombres/destinos y sus overrides.
BASE_BUTTONS_DEF = [
    # v30: OmniRoute y DeepSeek Harness retirados (el usuario dejó de
    # usarlos). Quedan los 4 botones de uso diario.
    {"id": "folder", "label": "Proyectos",   "type": "folder", "target_key": "projects_path"},
    {"id": "drive",  "label": "Drive",       "type": "web",    "target_key": "drive_url"},
    {"id": "notion", "label": "Notion",      "type": "web",    "target_key": "notion_url"},
    {"id": "tasks",  "label": "Tasks",       "type": "web",    "target_key": "tasks_url"},
]
# ids del sistema con destino editable por el usuario
BASE_EDITABLE_TARGET = {"folder", "drive", "notion", "tasks"}
# botones del pie que solo aceptan icono propio (v21: con la paleta pueden
# hacerse íconos a juego con el resto del dock)
FOOTER_SPECIALS = [("settings", "Configuración (pie del dock)")]
# v30: el botón Chat del pie fue retirado junto con la barra de chat.
# v22b: para la vista previa del icono en las tarjetas de Configuración.
# Archivo PNG de fábrica de cada botón del sistema (drive/tasks apuntan a
# los archivos con la clave interna gdrive/gtasks) y alias bajo los que
# pudo guardar el PNG personalizado (mismos que load_all_icons).
BUILTIN_ICON_FILES = {"folder": "folder_icon.png", "drive": "gdrive_icon.png",
                      "notion": "notion_icon.png", "tasks": "gtasks_icon.png"}
# v30: omni/dsh fuera de la lista (sus botones ya no existen).
ICON_LOOKUP_ALIAS = {"drive": ("gdrive", "drive"), "tasks": ("gtasks", "tasks")}
# tipo interno → texto amable para la tarjeta (v22b)
TIPO_CARD = {"web": "web", "shell": "shell", "folder": "carpeta"}

APP_TITLE   = "UIO Hub"
AUTOSTART_KEY = "UIOHub"
AUTOSTART_KEY_LEGACY = "BotoneraWitte"
DSH_URL     = "http://127.0.0.1:3080/"
DSH_KEYWORDS = ["127.0.0.1:3080", "localhost:3080", "DeepSeek Harness", "dsh", "deepseek", "harness"]
CLIENT_TZ   = "America/Buenos_Aires"

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# ---------- FIX RAÍZ: WIN32 64 BITS CORRECTO ----------
def _setup_win32():
    """Declara tipos para que los HWND de 64 bits NO se truncen."""
    try:
        u = ctypes.windll.user32
        g = ctypes.windll.gdi32
        u.EnumWindows.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        u.IsWindowVisible.argtypes = [ctypes.c_void_p]
        u.GetWindowTextLengthW.argtypes = [ctypes.c_void_p]
        u.GetWindowTextW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
        u.GetClassNameW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
        u.ShowWindow.argtypes = [ctypes.c_void_p, ctypes.c_int]
        u.SetForegroundWindow.argtypes = [ctypes.c_void_p]
        u.SetForegroundWindow.restype = ctypes.c_bool
        u.SetActiveWindow.argtypes = [ctypes.c_void_p]
        u.BringWindowToTop.argtypes = [ctypes.c_void_p]
        u.GetForegroundWindow.restype = ctypes.c_void_p
        u.IsIconic.argtypes = [ctypes.c_void_p]
        u.GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        u.GetWindowThreadProcessId.restype = ctypes.c_uint
        u.AttachThreadInput.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int]
        u.AttachThreadInput.restype = ctypes.c_bool
        u.keybd_event.argtypes = [ctypes.c_ubyte, ctypes.c_ubyte, ctypes.c_uint, ctypes.c_size_t]
        u.SwitchToThisWindow.argtypes = [ctypes.c_void_p, ctypes.c_int]
        u.SetWindowRgn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
        u.SetWindowPos.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int,
                                   ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
        u.GetAncestor.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        u.GetAncestor.restype = ctypes.c_void_p
        g.CreateRoundRectRgn.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                         ctypes.c_int, ctypes.c_int, ctypes.c_int]
        g.CreateRoundRectRgn.restype = ctypes.c_void_p
    except Exception as e:
        print(f"win32 setup: {e}")

_setup_win32()

def resource_path(rel):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, rel)

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

APP_DIR = get_app_dir()
CONFIG_FILE = APP_DIR / "uio_hub_config.json"
LEGACY_CONFIG_FILE = APP_DIR / "botonera_config.json"

# ================== v25: ICONOS DE FÁBRICA EMBEBIDOS ==================
# Los 9 PNG de fábrica viajan DENTRO del programa (base64). Si los
# archivos se mueven o borran, los botones SEGUEN teniendo icono y al
# arrancar se restauran solos a disco (ensure_builtin_icons). Los PNG
# personalizados del usuario (Configuración) tienen prioridad, como
# siempre. Formato: PNG 96x96 RGBA (alfa → esquinas redondeadas limpias).
EMBEDDED_ICONS = {
    "chat_icon.png": (
        "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"
    ),
    "dsh_icon.png": (
        "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"
        "AAAAAElFTkSuQmCC"
    ),
    "folder_icon.png": (
        "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"
    ),
    "gdrive_icon.png": (
        "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAASWklEQVR4nO2de3BcV33HP79z7t3V"
        "rt6WrTxMmDRy4sh2LCcBt5TAAm1IgeEPWjxTaIfplAlQaBMozBRmOhNDgUJfDBQCjqHQlEI7CQWX"
        "aZqQOKA0nUBC69hYlm3sFOJHYtmKbb1W2nvP+fWPe1eRbcnSanclJdF3Zi1rtXvu3d/ze36/s+cI"
        "c4MUCgXb29sbp7/bDRs2bPbevxZ4A7BSVTeKSDDH8V7QUNVYRPYAp4CHjTGP7N2793HAARQKhaC3"
        "t9cBOttYMofr2fLAGzdu7Izj+H0i8nZV3WCMkfSGUJ31Wi8qiAgiifi89yoie1X13iAIvrJnz56B"
        "9GWTsptxnIv9MdVkfNVVV7XmcrkPqeofWWs7VRXvPeng5TFMVZ/ohQef/lTAGmMQEZxzAyLy5WKx"
        "+LmnnnrqbFmGMw0ykwIkffj169ffAnzBGHON9x7vfSwihpeewGeDV1VvjAmMMXjvDwK39fX1PUAi"
        "K2WakDSdECeFv27dujtE5H7gmjiOY1XVNM4vC/9CGBEJVFXjOI6Ba0Tk/nXr1t1B4i1luZ6D85+Y"
        "avl3WWtvjeO4HGaWhV4ZPKBBEFjn3Pa+vr73MI0nnCPULVu2GMB3d3ffZYy5NYqiKH3NsvArhwFM"
        "FEWRMebW7u7uuwCfyngSkx5QThbd3d1bwzC8I4qiSETChb7rFyNUNQrDMIyi6OP9/f1bpybmsgIs"
        "4Lq7u3/DWvug996lz82Fpi5jdijgjDHWOXdzf3//TlKZGxIha09PT5uIbANEVcvPL6M2mJSpiGzr"
        "6elpI1GKmEKhYAFfKpU+aK3tcs6VaeYyaggRMc652FrbVSqVPgj4QqFgBZBrr712hTHmgIi0q+q0"
        "dGkZNYGKiKrqae/92v379z9nADXGvN9a2+G9V5aFX0+I916ttR3GmPcDKmvWrMlmMpknRWRtWtNY"
        "Dj91RDpbFlU9UCqVNplcLnc9cLWqsiz8+kNETFq4vDqXy11voigqGGOsqvrZ3ryM2iD1AhtFUcEA"
        "N0PCjxb5vl4ymCLrmwMRWbWod3MRTE5S5vn+8nuXqmuLyKoAWJfW9pdO/DegHooKE6qEApWTMyVW"
        "yIiQkSVH7Uwq83XBkmsjCpiiohlhTWi4qcHyyoyl0gCpCk+UHI+OO47Gft5eVE+ISCDr1q1bOvdm"
        "QMc8dlMj24eFq53QaAWvlYchAYzAiFcORZ4/fW6c57wSiGEp8Y0lY/1qIBjxnH51M0fftYrH/nOY"
        "VzxR5NkchPM0kVihwwhHnOcZpzSJ4uMxCHKJiywBLIm4rwZsURn89WaO/e5KZNSxdXOOQ+2GJvd8"
        "N6iShwA54ITz/N3ZEiGKmgzauRlciaWSFRZfAQImhrjZcuKt7Wis2AiGWgx3vCpPU0mTmm2F8EBO"
        "hO3DEceckItH8J034t64DXKrwEcsBSUsugJUwIx7Bm5uxTVbpKTENvGIe9c3cN9VIe3jiqtAVh7I"
        "i9AfOb4zGtEsHhc04Tf+CTS14DZ9CKIRMLZun2uuWFQFqAE7oYx2NXD6VU0w7tEpd+QNfGZznthU"
        "bqsW5QtDJcax2NJZXNfb0NWbYLiErnkretmroDQEsrhKWFQFCICHE29qQ0ODlNcOAE7AjiuP/UrI"
        "1zc00FFU4jncrQOaROgdd/SOO5q0hGtcjd90O0QeUAiy+Bv+LBX+4ibjRVOAGrCjnjM3NDK6tgEp"
        "nmv95ddISfnkr+U50mJoiGcXlwWKqnx+qIQ1FqIR/Lo/hNZOiGMwAUyU0Cteia7ZAuPPJc8tEhZH"
        "AQLiIGq2DNzSdu76uinwJAl6oN3wyV/N0TJLQnZAixH+aSRiX6Tk41Fcx3X49X8AEzGY9M0iEHvc"
        "de+FfOeisqJFUYAasGOewde0UFodIhOKzvD5vUlC0d0bG/jRFQGtE9MnZAWywJHY8+2RiEZj8Orx"
        "PbdBJpvUNspCFgNRDB1X4je8D0rDi5aQF1wBKkniHV+d4bnXNMPYhaHnnNen/8SB8OevbsTPUNfx"
        "QN4IXx4q8awK2dJZ/OoC2vUmmIguTLbGwESceMfK66A0kihmgbHwVxTAwYlb2hLaOUP4mYpyQv7x"
        "DAnZA80iPDoes2MsphVPHDTir/9wOuOdLnNI4hWZLK7nNtB49hupAxZUAeXQM7y2gaEb8jB6ces/"
        "/73lhPz0NAnZoXx1OMKJRUpn8V1vQy+7DkrTWH8ZYmEiQrvehL78jYtCSxdUAeLBZw0Dv9UGvjJ7"
        "m5qQ//76BprThOyANiP8+1jMoxOO5vNpp5nDVVRxN340rRFddDl/zbFgCkjqPQntLK5pSBJvhVf3"
        "Bsy4cucNOX56aUBTCazAoPN8fTgiZyx6Pu2c7SOKSbxkZRd+7e/BxNkFpaULowABEytRa0o7x/2M"
        "rOdiUEAUShnhYzflEa80GuEfRyIOxEpuJto5G4yB2ON7PgAtV0I8zkLlgwVRgAqYCWXg5jbijgCp"
        "It+5lEX9qCvD97qznBiK+cZYRKsxOD8D7ZwVAnEETe246z+8oHWiuiugXO8Ze1kmqfcU52f954wJ"
        "iFM+dVOez4hjIjaY6Cz+ZRehnbPBWJiI0a43L2idqO4KkLQrfuIt7RfUe+YLD6gIByc8D47GNIvD"
        "29wstHPWO028ZoHrRHVVwNTEO7Ihj4zPnXZeDKJAKFz2wyFaRsD5Ufw170QvnYV2zjqwXfA6UV0V"
        "IB5c1jBwcyu4eTR2pxtTQbNC9miJ1idHiXIGcR7yl6SeVeVFzqkTXVr3OlHdFFCudp4qtFBanZkX"
        "7Zx+YCAQOh4ZwhY9ajyEjZi922DwFxCGaQKeJ8RAFMHKKxM6O3Gmrl5QFwWogCkpxdUZBl/XAuMz"
        "F9sqwVTrb9s1issZxCnYLIydwP5sGwSm+oZ7mpD9ut9P6kTRaN3qRPUZNVXAyTe04lpsIqRaePEF"
        "1p8+72NoWIEcugc58gRkM1XOaAWcg3wr7rr3Q1x84SignHiHu3MMvbKxonrPxTCt9Z9j6ALqMP/7"
        "WYgnUoFV4QkmgPEoaV9e8fokFNWBltZcAaKgRhj4zVbUyHlCqgLTWf/UsdVBpgV55jHk8H2QDcBX"
        "W9dREJvQ0iBflzpRTRVQrnae3tzE2LW5aduM88Hs1p/COwibsLv+FkZOQxBSlReIhVIJvWwD2vXb"
        "dakT1U4B6fqeUluQ1HtKtUm8wOzWP/WFQQMM/QKz+0tJQvZVLkM0ApHHbbodmlbXvE5UMwWU1/cM"
        "3tRMvDJAotok3jlbfxk+hmwr5sA/w6nDkKmSlmKSqmprZ0JL49Ga1olqooByvad4RUo7x6qv9zw/"
        "OHO0/ikQC3ER+z+foeJl1dNhavuyo7bty5qMUq73PPuWdjRTm3pPedyKrL+MckJ++gfI4fshG1aZ"
        "kM9rX1KjD0gNFKAmCT1D63OMrM9dsLqtusGp3PqnvtmESUIungVbJS2d2r5cXagZLa1OVJK2GTOG"
        "E29pT9qMNaKd87b+MtRD2ASDfZh936wdLVVNqq5hU01oaVUKUElo56nXtTBxRQ3rPVCl9acoJ+R9"
        "X4PBpyHMVFknslCK0MuuQ7veVhNaOn9xCZhImegMGbypuWb1HqiB9U9CwWageBK763O1yXhlWnr9"
        "7dB0edW0tLpbUvCh4EMBX8PmRS2svwwfQ7YdOfxd5OjjSUKuKnSktLSlE99ze1InmmvvefrR5gkF"
        "DYXsyZiGYw7CAPEWdD4PM/lTvKJZIXMstf58av1S5cMYzJN/g7gIY8DgMOIrf+AxFkypBGvfnq6q"
        "m3+1tKoApgJhcZyWg6cobmhNZp3zVqkmt+MaIYTOh4YIhz1xY0prq4ID04QceYyhJ+/BbXonTFCd"
        "/3sgC/kbP0rw4LvmPcy8vyUpKN4EHO/6CBOXNDB+9TFwdh7hMO3hagaC49D8AyQOyR0YRmoU1gRQ"
        "NVwSjvONtYMEnRsRrW5jGE32NmTrka9zaMdfkz+2A59ZUXF4m7cHeAkISkNYd5Lx8FZk71l03lN0"
        "B74VVv4ljJ1EfQtjl0Mtay4inqfiPAOdz/A7HT+EapeCCpwcX81RfyX21XfgdzyatC8rbObPWwGi"
        "Hm8b6PzltxnqfD1xrnkeyS1dqatN0PAwrLgXtBWMQun5rQaqVYOSRBvnlY8evpw3Nx0mTG14PnBq"
        "sVnHI8d7GDzwBB3Niq7chBz/LwgbK+rIVZEDFG8yhOMDtB//D0523YqUzqAVzw4NEEHrN5KkUl6P"
        "Ls/bUS0CkUOwgePQWI57Bpt516WncZFg58FvBYcRuO/7P6Nh1zuwuRhn8+na0soSVlU0VNTjgzwr"
        "jn+foHgcNRkqE5cD3wSNO6FhN2gj9dxaQxVElE8fX8VELIhoxcp1XjB5+Om+Rh7e20pzSw4XNDNf"
        "P61yapJ4Qab4DK0ndkKQR+ZsAQpkIBiAtrvB56n3viYewVjHgZE8/3qqDROAr2D2mGxzqJTGhc/u"
        "uCQttPqqZtfVzw3TXNB24iEkGq4gBHnwOWjeAcExoFLvmR+q8QLvBNMI9/+khf/e30hzg6u+31Pd"
        "21M6anPkh/bTOvAwBE3IrMnYg+YgcxBa7gHfzCzb7NcMk14w/LwXuDl4gSpIoAyfsXzpgVU0Zn1N"
        "Jv+1KZ1psg9Dx5HvIPHIHL3AQvvXwBRrdhtzhSqI8fzF0U6GS3ZOXuB8Yv3f3LmCPb/Mkc/6isLX"
        "TKhNQwaPsznywwfm4AU+Sby5H0PuseT/C7ynVeIFnkOjOT729CXYWXKBV8Fklad/mWH7zg7aGh3O"
        "L5GGzCTm7AUmsfr2r5J8rXpx4DWhpdueXcmuszlsoDOGIlUwWdj2wEpOnAnJBFqz3W5qpoCpXtAy"
        "8EMIm6fxApfE+5Z7k/ivORZrRzcFVJRYhXf/32oiJzBNKPI+sf59+3N89ydttDU64kp2DpkFtQ2+"
        "6vEmy6qn/wU7MYhKwLnTqUzCeJq/lzCgRd5Oz6sQWMeus018+ljntKFIBSSEv9rRyei4wZraMrWa"
        "KiBhRA3khg+y4ui/Qdg4xQt8wvXb7k64/wLRztng0lD0qaOdHBzJYq1OKiF2gs0r9zzUziP7mmlp"
        "9DWL/WXUYWmixwfNrDj+/cQLTBYhSma5DbuTWa9vYqFo52xQAFEiZ/jALy5PnhMldkLQqvx4TyMf"
        "uXs1uYyvbnnRDKgD/1O8CQknTnHpoS+DzaGSTTyh9R8QGUc0abIslYfzSSh66FQrdx7vwAoEDcre"
        "Azn+ePsV5DKKkfr4a12+eSDq8EEjK47fh3GjHL96K27Vw9DyOKptLBXrn4oYgcDzsWcu5R1XnCY7"
        "DO/+4ss5PRrQmK0d7Twf9fvqh3risJn2Zx8kmDjLwI1FGCuv21/82D8djChRHPCh4mqCxw3PnAlp"
        "zzniOgkfquiIzRUqFuPGkn4xVa5WXgCIKKOxBQP5TG3KDRdDkB5MWTdPEHWoyaE2bT0ueQj5IMm2"
        "9Ra+qsYG2GeSZRV1JOU+mU6WdbDEH17rLnyfynyfUdWTdb3UMmaEqp40wIPpLy+E+PCiwBRZP2jC"
        "MOz13rvl40sWDiJivPcuDMNeUywWdwE/FxGWjzGpP1TVpwdo/LxYLO4yhw4dmgC+lZ6OvRyG6g9N"
        "Zf2tQ4cOTRhAvPd3OucGl5VQd6gxRpxzg977OyE9ynD//v2DqvpFY4xRXeBN015CUFWXyviL+/fv"
        "H5w8yhCQnp6eliiKfmqM6XLO+eWkXFuoqrfWGu/94TAMX7F79+4heH7lvezevfuMqr4XUBFJd7le"
        "Ro0wKVNVfe/u3bvPkK68LFu5KxQKQX9//07n3CeCIAhUNV60232RQVXjIAgC59wn+vv7dxYKhYC0"
        "JDwZZnp7e+MtW7bY/v7+rVEUbQ+CIFTViGVPqAaqqlEQBGEURdv7+/u3btmyxZZP04YLFzSWc4Jf"
        "v379XdbaW+M4Lm8uvJwTKoMHNAgC65zb3tfX9x4SGZ5TlTxfqOU/mr6+vvfEcbzVGGPTAyhjlr1h"
        "LtC0wmyMMTaO460zCR9mXtI71RNuAb5gjLnGe4/3vnzi9rJHnAufHtIZGGPw3h8Ebuvr63uAGYQP"
        "MwtRSY7cDvr6+h4oFoubvfcfV9WBIAgCYya/FuhIXO2lWMIof+4kmRpjUvIy4L3/eLFY3NzX1/dA"
        "mnBnZJVz6bXZ8kU2btzYGcfx+0Tk7aq6IZ05o6q81IqpIkL5UNT0IOy9qnpvEARf2bNnz0D6sknZ"
        "zTjOXK9XKBSmZm+7YcOGzd771wJvAFaq6sYldy5lnZDG+D3AKeBhY8wje/fufZxU2IVCIejt7Z1T"
        "8/v/AXHPc+uNsgdHAAAAAElFTkSuQmCC"
    ),
    "go_icon.png": (
        "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"
    ),
    "gtasks_icon.png": (
        "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAU1UlEQVR4nO2de5BdRZ3HP78+596Z"
        "SSYzmbx4SXDzgEzerDEiWs7iAxZkfUHcWkFQFhCplUJXt1hLFnyU6667tciWoliiosFawVeJSvBV"
        "YREhoJBshiQaIOGxJEMYyM1k5s495/Rv/+g+MzeTuY+5985kZtxv1a153HP69Pn+un/9+/36191C"
        "dZCurq5g8+bNsf87WLly5Xpr7RuANwLzVHW1iIRVljeloaqxiGwDDgC/Msbct3379i1AAtDV1RVu"
        "3rw5AbRSWVLF84K04NWrVy+I4/gqEblQVVcaY8RXCNWKz5pWEBFEHH3WWhWR7ap6VxiGX962bVuP"
        "v2yIu5LllPvSSzJetGhRe0tLy4dV9YNBECxQVay1+MLTMkxdbzT1YP1PBQJjDCJCkiQ9InLLwMDA"
        "fzz55JMHUw5LFVJKAOI/dsWKFecANxtjTrXWYq2NRcTwp0d4JVhVtcaY0BiDtfYPwDXd3d2bcFwp"
        "o6ik0UgcIn/58uU3iMg9wKlxHMeqql7P/z/5R8OISKiqGsdxDJwqIvcsX778BlxvSXk9AiP/Udzy"
        "bw2C4Io4jlM1M4lIL9VxJ9U4ZAENwzBIkuSr3d3dVzJKTziC1A0bNhjAdnZ23mqMuSKKoshfc2zI"
        "FwEJwITupxj30RhsdPQH8deMuOfYwAAmiqLIGHNFZ2fnrYD1HA9hqCmlg0VnZ+eNmUzmhiiKIhHJ"
        "TGydZZgwtWAHISmAjd3/Teh+Ns/z16l/Bf8z3+vuUXX3mBBMBoImJ4y03AnuKaoaZTKZTBRFn9yx"
        "Y8eNxQNzKoAASDo7O98UBMHPrbWJ/181Zmr9EOMeZSOI+8EmkJkBra9A2xejHZ3QMg/tWAoYtH0J"
        "mMARPVSGILm9kBxG+vZB39NI7il4+Y/u/4Wcuy5scQJBQMtaiI2EAokxJkiS5C07duz4JZ7zVOfL"
        "mjVr2qIoesQYszhJEustnfGFBICFQp8jY8Zx6HGvRo9/DTp/Ldq+FJpmuqoWa87UxSluHspwkxka"
        "yYCogOSeQg5sg57fYZ7/LeT2up6QbXW9xI5/r1BVGwSBsdY+kclk1m3dujUHaJh6uIVC4dowDBfH"
        "cRyPu0crgdPjgy9DkEVfcRa66HzsCa+FWSc67ZkAiUIUQVRMjrixAY7mLCqSkqofD0K04zR03mmw"
        "bAO2P4f0bEH2bMLsvQcGeiEzE8Jm1/PGSRAiYpIkicMwXFwoFK4Fbuzq6goFkGXLls0xxuwSkQ5V"
        "HdVcakwtAtfSCznItmEXvR1deiG64M9d642BJPLkpUTXWxX1qsoTa7IQumKl9wnkqZ9gdn0HDj0D"
        "mVYIsuOpmlREVFVfstaetnPnzt4QUGPM1UEQzI3jOBkX1ZMSWchBZiZ22UXo8svQead6NRFDbIet"
        "nIaKv6jHgOt5BefEavtidN012NPeg9l1hxNE33OQnTXcWBoLsdbaMAznAlcDn5YlS5Y0ZbPZx0Tk"
        "NB/TaKwAJIAkD0kBXfhm7Kv+wRGfAHGBIyyfiYZa1zvCLGSAvgOYrbdgdm4EW3CCsCWjCLU90nnL"
        "oqq7CoXCWlm1atUZSZLcj9O8jVU9JnR6fuZJJOs/ji4+f2hgdCpmsvh26gbi0Kkn2b8V8+CnkP1b"
        "oGm2v8SWLWHsD8QGQfB6E0VRlzEmUG3gE1JVMnAAPflNxH/1Q3TJ+VCIII6cCTlpyAcQVycbQ76A"
        "zl9D8tb/wq76IBQOOfM49SMaAN8LgiiKugzwFgARaUzrl8A5T9Fh7LrrSM6+DVoWQL4wLJhJCy+I"
        "KAIL9syPk7zxFghnOEGYxhiHRVy/xYjI/IaUCo78eAAyrSRnfRG77kPuZRLf6qcK0kYyMIguOZfk"
        "3I3o3BVOnTZICAAiMl86Ozujhtj9KfnZWSRnfxM9YRX0510oYCrDxtDUBPkcwab3Iz0PQ/McH3uq"
        "D6oam3Eh/7hpQj54Q6IA2TaSc25Dj3u1izk14N1EJKxfIY9Gfn5wepCfwgTOZM62k5xdLIT62259"
        "AhADyeAo5E/DuXkZIYQF65xjWad1VH8PsAWSM//Z6fx8fnqSn0IC58M0tZP8xRdcWDwZrMuyq+PO"
        "EPK92NM/ii45Z/ro/EowARQGYfbJJF1f8J5y7QG82gQgzsPVU/4Se/rVzsafzi1/JEwI+UF04ZnY"
        "0z8C+Zdqfv+xC0AMJAMuvPC6z/nkjPELoE5amADyEfb0q9GF5zgfoQaDsoYeIJAMkqy/Htrmu4Fp"
        "Unu344XhOYnkjBu8b1BgrA1xbMxJAIWD6MKz0cXnQj7601I9IyHGDcpzTsGuvMqHK8ZmFY1NAJq4"
        "MMOrrjtyPnYaQEZMG1QNE8BgjF3xPpi/BqK+MWmEMVwZQiGHLno7zFvsIpvTQPUYcZ84gShxCiQY"
        "02uJm8rMNpEsv9wFIhsvAJ+xkG0jWf63YLXG5jK5EBjoL0DfIMxugTkzILJwcGCMQjABFBJ00Xkw"
        "b7VLMqhSCNUpcAlgMIcue69r/fnC1IpujoLQwEv9sG6hcG2XsOYVQiCwp1e57UHlu48pHS2urVWG"
        "OH+guYlkxeUE911LtYNxlSNoAkEGu/TdR6eDTEGEBnr74TWnCLdfbGhrHv5u7UnCzRcIbc2Wrz+k"
        "tDe75IyKMAFEFl14Nsw6BQ7vcxP8FZy0yv1EAij0oSd2oQtWQiFu6OzQRCM0kMvDGa8cJj+2w2lH"
        "iXWfz7zVcNZSITcIQVUNTty8R8tM7NINzleqQktUIQBAE+yit0E4LpkCE4bQOH1/fBvc9jeO/ETd"
        "/1NXMjDDwvjr04UkzWuuBsa4mbRXng/Z9qrmDCoIQNyoPuM49PjXQsSU1f2BgcMFN9h+/T2Gjhmu"
        "pY/WukUc5ye2QSYYi8VtXIrN7FPQeashGqioLcoLQAxEA+hx66HtONfFpuAAEAgMFKC9GTZeYlh5"
        "gpBoaUtHcYPvwUEnpDG9sSYQGvTkN/vJ/PJ3VxCAS2DV48/wme0NTc2YEBiBQgJtReTHJVp+CrXu"
        "vnt26NgtbjGQ4CZtMjN9umOZ+pX91mcp6/y1fjXY1HK8jDj1cbgAn3+HIz+yTueXglWndr77qHLn"
        "o84KisfS7kQgUbT9z6D1JDdfUKYPlamKn+1qPRltX+xGqynkfIk4Mg8Nws0XGM4+zbX8TBm1E3t1"
        "842HlI/+yJKpKUHfO63NrejcVRUnbEp/I64gbV/sUsRtXEttjglSi6a/ADe9y7BhrSO/XMuPnerm"
        "i/crH/6BpTXrjJqaQl6qYEDnrHD6rEzDrSyAjmU+P3/q6P/AQE+fs+U3rK2sdmLr1M6djyn/+kvL"
        "8W1+gVet8UYRsKAdp7kYWhnuynjCPr++ZV6NtRgdgW+e6cuJOEujUQg9+Ve/Xrh0fRUt339/52PK"
        "td+3tDZ5P6CuYK+4Qpo73LqDmgSgCiaDdvgU8gbo/0AgN+h0c2hcPmyizjyE+pdGpC3/A2cKnz7P"
        "YL2pWarmKfl3FZFvpNr4TxmkPaB1ITR1FOURHV1w+VhQQxZIOBiBg3k4a6nwztXCCW3OK713l/K9"
        "rUrGOLJqffk0uPaBM4XPvNWQaPl075T8rf+rfOxHlpnZBpE/EhUsxxIC8B5w83xvAVUuqBwCgd4B"
        "uPwMR04xzl4mrF+ofOQHlpk1tsBMAD2H4LzlI8gvwX7iyd/+vHLJty2mTuEfjTQu1I62L0b6nnML"
        "A0cJ41TuAXVmLgbGxdffvXaYHNVhG90qvPt0QcTUpAYyAbx4GF63SLjpXU7tCOXJDzz5F91uOZiH"
        "GdnGjkNDqIK/Ktitr1lYC00hXPU6GSppaFAUvzTMwoa1bjH+WIQQGkf+a04RvnmRC65ZL9zRkIYf"
        "nnsZLvrWOJM/hHrD0XVAxM0wzW+Fkzuk5H4HoRkWwk3vMvQNlicyvSeXh/VFMf1y91j1RkAerr7L"
        "0nsYZo47+ZUxIbGFNMZezrQbixDSyOacmfClC4fDyuXIN578S75t2bJXh+YBjjUqh6PrGHxVIRvA"
        "vhx0P69pmKQkqhFCOo/b3gwb32s4aXbpsDIMq7GXB+DSjZaH9ipzZ04g+RX4Kx0ZMSEM9rrl/nVG"
        "QoMAPvdLJZf39n8NQhCfvTAYQ3tLUVjZlgkrq9PARuDa71t+86QjPxr3OSXPX/4QktvjfIAS/JUJ"
        "RfhgXDJYlytg1ena3z3tTL5cvvIAO5oQxJdlLdx+cVFYuQz5FtczPvETy707lfmtE0G+h4gjPe6v"
        "MRiHL6Dv2bp9scRCxwx4aG/tQjiYd5HNz7/DsObE8iGGdEoxJf8rDyizZ0yg2lFnC0t/D0SHy86K"
        "lTZDfTBO+p5DZbjQWhFbmDtzWAjVWC7FQhiMHdsXrpEhR2o0pBProYHrf+rIX9A60QOu9wQHely6"
        "Yra1BhWkChI6HdagWFCUHCmEanuCVbh4nXDxOhmK75RC2jO+uUX50v3HgnyGe0Buj9saoaZwtA/G"
        "yct/8CvbG5OEW4sQ0u8r+QbphMudjymf+IllQeuxsvN9JXu7j/x7FJSbnIOwCXJ7IPeM7/ONeZta"
        "hVCJ/OKw8oxsiW0KJwImhEIBc2ArmCa/H1GJSysXdNAXRNmCxopahFCyLE/+vbuUa75nmdU0HGua"
        "eHjTLPeM2xgqzFKu4VZ2xMAtTi76u1FohBBStbP9eeVjP3RhZalRkA2BtRCAOfAYFA5WXD9ROSsi"
        "bEGefwD6cxCMPqlQD+oRQprVlkY2c3nneR8z8sHZ/AryzC9wE8PlL6/QAxSCZsjtRXp+DxkZl7nh"
        "WoSQhh+Kw8ot2SoTaccNCkEIh3qQ/Q9DpqUiX1UEelxyltnzs6FnjAdKCWE0KyYNP7zUD++/w/Ly"
        "wOSIbDqNIZjnNkP//gZlR2sC2VnI3p9C7x7IZGiUNTQSowkh8M5Y4s3QNPyQy8Nl37Hsy0Fr0+SI"
        "bGJCiCLMzm+ByVZlBVTRA5w/QP4lzFN3QygNtYZGolgIl260/PEFp+cDb4amWQ+XbrQ8uGfyhJXd"
        "+rkA2fcIvNjt9j2tQl3L8uXLq1AqabbXHOK33e3SLexY8rbHjsDA4UFozsAFa4TzlguBgd89Dd/Y"
        "Yunpg1mTpeWDIzsTEmy6DHn2Vy49vYpU/ioFgOteAwew6/4Ru+7vYGD8N+VIx4C+wnA+UZy4acRj"
        "bu0UQxPIZpFnHyTY9B6XlFulsVL9bIt1S1TNro3Q9xKEjTdJj3qkDz3MbnF6vjXroqqZyUQ+kGoC"
        "s/0rnvjqNcMYpru8Sdr3LGbrl5z3M45jQdFTSexwLKjS1OaEwybQlEGeuAd59teQbRvTKqKxzTdq"
        "Atk2zM7bkX3dkB3XXWanAHxoNt9H8Oi/eZU8ttYxxglfdZMLtoB58J/8ChAz5odOG9gEsiHm9zdB"
        "784x6f4UY59x971A9j2EefjfXdJPhVUg0xJ+XbDs3oTp/pq3DMe+y25tKQ82huYOzPZbkN33QktT"
        "w7f4ndRQtzUBLz9D8MDHvcdbG+rLCwpbCB64Dnlhl9va8U+hJ6h1K0XjfoLN18Jgr8/7rM0gqSPp"
        "x7rJhnwv5r6/h/xByEzzQTmdF88EBL/9FLLvwTFbPSNRXw/QGJrakRf/h2DTZS7+HU5TIaiCKGQy"
        "mP++Htn5Lbd4pU7VW39qoo2haTbS8zDBvUVCmE7qSO0w+fdfj3n8aw0hH8Coav2l2Bia5yD7i4SQ"
        "zU6PgTnV+dli8uc35N1UNTbA48YYqDfG7IN1sv9ht8dybi80T3HryMYu/K4DmM3XYR7/eqPIt57z"
        "x42qvlB/TdNiI2juQF54lODuC5Fn7ncmKnZKrbJ0Bzp4Oz+3l+Bnl7gYf8vchjYoVX3BAD/3fzTG"
        "nbWxO/qjkCPYdCnmkf90gbswMzV6g0386tAm5ImfEfz4AuSF3zdM58MRXP/cZDKZzdbaxh7eo4lz"
        "TsIWzCP/4lXSU743MDkHaPW9tDkLyWHMbz5F8OurIToEmcaeJSMixlqbZDKZzeN/iE96jkzTXOyq"
        "y7ErLncDdMH6tL1yaxknAKlqzLptl+WJuzGP3oT07nThheJrGvG4EYf4mN27dw8Cd/jTsRsfVbOx"
        "mx1KBjBbPkvw43didt4FxNCUZei4qAkdI3TYV8lmIJNBnr2f4J73Efz6Qy6ns2XucK9o8MM913fs"
        "3r17UGCiDnITt/lC1A/JIDpvFbriMuzCc6Bllj/WKob06N0GrlHmiMPcxOU3hUAUI/t+i9n+NeS5"
        "+xzZ2Vn+lnFpEEcd5CbFp6iGYXjDuB9lmKqc+LDrHbMWYpduQF95Ljp7qVs2afFpEHFRWnwqFP/7"
        "6O/nf4zICpXQxe3TMykPPY95bjOycyPy4uNDmR9pCs54QVXjMAzDOI6HTlVNm9nEH+aZCiLJ+xM4"
        "2lyvOPnN7kDP9iXQPNPnpOKnxvy9pfZiM/6MQsORy+QLBSS3BzmwDXnmF8j+R6C/x2V7ZGYw3sQD"
        "JQ/zTKt47I6zFb94VRN/lG3kjo2aeRI6byU6Z4U7zra5A511sru2uX30muUPgxaQ/gMwsB/JPQm9"
        "jzvi0yNtxbjy070bJmbsUcocZwtMkgOd016h1u1EHud9KCB0u440zQYJ3PYJRyz7cav4JPc0xH1u"
        "s7xCbrhVB03H9FDnag50BmDDhg3BnXfemXR2dt4ahuEVcRynR1xNvJ2Y9gxgqKWmx80mg6PfE2Td"
        "PcZ4suXI+yce6vV+Jo7jr+7YsePKlOP0gpHEpmOCXbFixa1BEFwRx3Hi/zchi7rLw1f3KAvJWzfY"
        "ooZ9zOepLaBhGAZJkny1u7v7SvyCX4oqN5LU9EvT3d19ZRzHNxpjAhFJo6bH+K189dR63yH9pH8r"
        "I97vmFRSVWMRMcaYII7jG0uRD6VVS3FPOAe42RhzqrUWa23sLaRJ0CMmFaz3ckNjDNbaPwDXdHd3"
        "b6IE+VCaRAVsV1dX2N3dvWlgYGC9tfaTqtoThmFofCwVZxhaxitdenIjfe8EwBhjwjAMVbXHWvvJ"
        "gYGB9d3d3Zu6urpChg3po1DN4BqkD1m9evWCOI6vEpELVXWld6lRVRoVTJ0qEBHSQ1F9DG27qt4V"
        "huGXt23b1uMvG+KuZDnVPq+rqytITScgWLly5Xpr7RuANwLzVHX1uHrQkwhex28DDgC/Msbct337"
        "9i14sr2Z6U228vg/mB9Vj6apdEgAAAAASUVORK5CYII="
    ),
    "notion_icon.png": (
        "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"
    ),
    "omni_icon.png": (
        "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAA60lEQVR4nO3RMQ0AIADAMEANEnEP"
        "MnqwKliyec++I8zSAb9rANYArAFYA7AGYA3AGoA1AGsA1gCsAVgDsAZgDcAagDUAawDWAKwBWAOw"
        "BmANwBqANQBrANYArAFYA7AGYA3AGoA1AGsA1gCsAVgDsAZgDcAagDUAawDWAKwBWAOwBmANwBqA"
        "NQBrANYArAFYA7AGYA3AGoA1AGsA1gCsAVgDsAZgDcAagDUAawDWAKwBWAOwBmANwBqANQBrANYA"
        "rAFYA7AGYA3AGoA1AGsA1gCsAVgDsAZgDcAagDUAawDWAKwBWAOwBmANwB6ijQNe9qAxaQAAAABJ"
        "RU5ErkJggg=="
    ),
    "settings_icon.png": (
        "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAbbklEQVR4nO2de3RdVb3vP3POtZ9J"
        "dnZKkvLoy5KGpCmt0vYM4SqhPAaKyFWxx6NYUKSl4uOq6JWrolXQy/XAxaseHoWL8vBZHV7FgzLE"
        "llQPOA4tmrRpShNKaSq0TWiyd5L9WmvNef9Ye23S0JTsRxpUvmOswWhYe661fr85f/P3noKpQbS3"
        "t6uOjg4n/2+1ZMmSf9JanwucD9QbY5YKIawpjvc3DWOMI4ToAgaBzVLKrTt37vxPwAVob2+3Ojo6"
        "XMC82lhiCs9T/sBLly5tdBxnvRDivcaYJVJKkX8hjHnVZ/1dQQiBEB75tNZGCLHTGPMzy7Lu6urq"
        "Opy/rUC7Scc53v/Mc9JZuHBhbSQS+bQx5qNKqUZjDFpr8oP7Y8iyvuhYLycEUpY3rNZ6uiaHzv/X"
        "AEpKiRAC13UPCyHuTKfTt+/duzfh03CyQSZjgMhfuq2t7WLg21LKZq01WmtHCCGZBoIf9QJCkMtl"
        "yWSyCKawlif+Pv+bcDhEMBg6EStUG2O0lNKSUqK13gN8sru7+1E8WhmO8RnHYkCB+IsXL/6KlHJD"
        "fsY7Qgg1yW8qCo/4OZrPOINly5ZhOw5SFMdvbTQBy6Kzs5M9zzxDMBg8UWLSGGNcKaUlhEBrvWHX"
        "rl1fZRImTNw0x8/8jUqptY7juIA4kRuslJJsNsv8+Qv4+s03k7INShXHd9c1RAOCj338E+zo6iIc"
        "DuO6xxXHlYIQQljGGG2MMZZlbWhrazutu7t7HS9LjQITjppWq1evloBubW3dKKVca9u2nb9nWsXN"
        "RGitCQaDPLO7hxcOH2FsbIzh4WRR19jYGC8cPsIzu3sIBoP+nnUiIQFp27YtpVzb2tq6EdB5Gh91"
        "E+BtuJs2bXJbW1s3BAKBtY7j2EKIACdA5EyEMYZAIMDAwACDgwOEQiGkECilpnRJIQiFQgwODjAw"
        "MEAgEJgpLU0IIQKO49iBQGBta2vrhk2bNrnt7e0FaeIzQHV0dDitra0XKKW+7DiOM9M6vVKKkZEk"
        "z+/bRyAYQBdBQG0MgWCA5/ftY2QkiVJqGt/01SGEsBzHcZRSX25tbb0grxUp8BggALNs2bK4EOJu"
        "QBhj/L+X89CyVEghBI7t0Ne3B1XCMEpCX98eHNsp6OulwFcvy0SBpkKIu5ctWxbH2weEbG9vV4DO"
        "5XKfUkqd7rqur2aW9dKO45BKpcpjgpT07emllL3TdaFvTy+ijOdLKUmlUjiOU7Y9IoSQrus6SqnT"
        "c7ncpwDd3t6uZEdHh9vS0nKSEOLjWmudVzVLhlKKVCpF4+zZtJ+3irGxsZJeXuf3gX379jI2NlaU"
        "GFFKMTY2xr59ewkEihNfPqSUjI2N0X7eKhpnzyaVSpUtyoQQKk/jj7e0tJzU0dHhSsBIKa9TSp2k"
        "tTaUIXqUUmQyGWpqavjmbbdz6+3fZv78+WQymaKYIIRACkE4HObQwYMMDBya8kb68gZ+iEMHDxIO"
        "h5Hj3AZTgZSSTCbD/PnzufX2b/PN226npqaGTCZTLhOE1toopU6SUl4HGNnU1BQCPlAp4ldVVXHH"
        "3fewdNmbCIXD3PDFG6fsDpBSopTCdV1GRkYYSY5w6NBB9j//fNEM2P/88xw6dJCR5AgjIyO4rutp"
        "SFOYCL6r5YYv3kgoHGbpsjdxx933UFVVVTEmAB9oamoKiTPPPPPNruv+kZc35KIxnvj/dtdGlq9c"
        "ydBQAiEE8boYN2/4Kt+/715mzZqF40xwiwiBkhLXdUmlUriuS319PYvblrB8xUoWty2hdXEb1TXV"
        "uK5+1ZlsjEEpyejIKD27utnVvZPt255iV/dOBgcHUUoRjUY9RmsNE5hqWRZHjhzhQ1dfw5c2fIXh"
        "oSTGGOrqatn+1FN8bP06xsbGyjXsDKCVUm8RLS0tn7cs6xbXdd1S5P9kxLcsK08MhZ3Lsub9/8ze"
        "vXuJRCIFo0gpheM4jI6OEo1GWb58BRde/DbefPY5zJk7j1DIwnEhk04XbUhJKQlHIlgKslmHA/37"
        "+dOTT/DYo79l+/ZtpFIpqqursSyrQEgpJel0moULF/Lgj35KIBjCdV1PI3OcijHBGOMqpZTjODeI"
        "lpaWxyzLukB7X1jUbnk84vtwXZdYrIYn/uOPfPSaqwmGQggpMVqTTCaJx+O87ZJ38O7L38uSM5cR"
        "DFpkMjmy2RzG6LLUWV/0CSEJhYKEw0FyOYedOzr5xc9/xm8f+XeGh4eJxWKFd8pls9x5732c81/e"
        "QjI5cpS4qSATtJRSOo7ze9Ha2tqplFpaLAOmQvzxLz7rpFpuufkb3HP3nYTDYZSUvPO/vosPXvUh"
        "WlpbsW1PBBljKqV7HwVfrgshiEajBAKK3T09PHT/93n4l/8PV2symQxrr/0oN3zpCxx5afJvqQAT"
        "tJRSuq7bJVpbW+1ird5iiO9/vOeidbnqA+/DCgS44Ys3snzlCrJZh3QqVRHf/1Thr4xINEooZLH9"
        "qW3c8vWbcGyb+3/4E6RUBWYdC5VaCcYYRyxevLgoJblY4o97GMFgkBdffIF4bZzaujjJRPKEEn4i"
        "fEbEamMkhoYZTgxzyimnksvlXnUFVooJRTGgVOL78FVE13VxHGfGfTQ+XNfFsixPYbDtKYu/SjBh"
        "ylNPSslYXlsphfjgGVi2baO1fs0QH7yJpbUuivjgqaxDQwmWr1zJv921kWg0ytjoaFErekp3+oSb"
        "M3cud917H288a3nRxB8/VqU32Eqg1PfymfDGs5Zz1733MWfu3KIYWRQDmhYtYlFzM8Z4f/tHy4Q4"
        "Fjw1V2AMLGpupmnRosozQGtNNBply+bNvPvSd7C1Ywt1dbGC2+AfFb57o64uxtaOLbz70newZfNm"
        "otHolA3HojZh30mlteZfPnAFH/9vnyYeryOZTE6L7v5ahW9TxGIxhoeH+O7/uZ0f//AHnvUdDhdl"
        "tRethkopMUBieJiW1lZu+MKXeGv7uYyMpI6rO/+9wLdpamqi/KFjK7d842Z29/RQG4972QxFukyK"
        "ZoAPy7JIjY1hgDVXfZjrPvFJgsHQlHTov1X4tkwul+WO73ybB+//HgKIVlW90sk4RZTMAMivBmNI"
        "JhK0trXxre/cwSmnzsG2//6Y4NkwQV584QCf+sR19HR3E6utJZ/7U/K4ZZmgWmuElITCYUKhEPG6"
        "Oly3vBjsaxVe2qFDvK6OUChEKBxGeBlwZY1btg/AaI1Skhu+cCN1dXW4JS7FKT8vvwG6rnvUNY05"
        "oAW4jkNdXR03fOFGlPK8p+WiLAYopUgmk1x62btYvnIFiUQSOQ0WrjGmQGjLsqiqqiIej1FX513x"
        "eIyqqqqCb9913WlhhlSKRCLJ8pUruPSyd5FMlp/yUlbuj+M41NbW8sErP0w2V5wZP1W4rksgEKC2"
        "thqt4dChw/Tv38+LB18kmUgAEKut5ZSTT2HuvHnMnt2IlDA6msa27Yq7PIQQZHM2H7zywzz6m0dw"
        "nPJEbskMUEoxPDzM+97/floXtzA8XNkEKK01UkrqZsUYHDjCrx/+Fb955Dd0dXYyMDBAJp32QoqA"
        "yke/GhoaWLpsGW+/5O1ceNFF1DfMIpkYK4xVCUgpSafStC5u4W2XXMJPfvQj4vF4yQZpWVqQ67rc"
        "98APWLrsjWXnAE0c17MmHR584EHu3XgPfb29CCEIRyIEAoGjfDd+gYht22TSaYwxNC1axDXr1rLm"
        "yjVIaVUkrcSH7xno6vwLV195RVnjlkQxP2HprOUrOHPpUlKpdMWI74m1GM/tfZbVl7+Xz13/Wfr7"
        "+4nX1RGrrS3Emo91WZZFrLaWeF0d/f39fO76z7L68vfy3N5nqa2NlayrT4T3/WnOXLqUs5avKGvy"
        "lfSrfCUIF138NoKhAMZUJvPYcVxmzaqlY8sWLrv0nTz5xJPUN9QTCoVwXBcpBdFIiFh1hNqa6FFX"
        "rDpCNBJCSoHjuoRCIeob6nnyiSe57NJ30rFlC7Nm1eJl25cPYzTBUICLLn5bIXBfCl7BACEEUqlJ"
        "B/Q9o/X19bz57HPIpHMVmf2u4xKvi7F58+NcueZKRkdHicfj5HI2Skpi1RFiNREi4SCBgIWUAiFA"
        "CJBSEAhYRMJBYjURYtURlJTkcjbxeJzR0VGuXHMlmzc/TrwuhlsBJkgpyaRzvPnsc6ivrz+uB/R4"
        "NJUTb8zlcowkk+RyuYLfQylVGMB3yC1ua2PO3Hlks9mytR+tNdGqCHt272H92nW4rks4HMa2baJ5"
        "ogYDFpjJCwILfzcQDFjEaiJEw0Fs2y5EqdavXcee3XuIVkXKNqCEEGSzWebMncfitrZC9p9PbD8J"
        "zBhzFE0n0kqOHzCXy9HUtIiLLr6YU087DaUUo6MjDA0NMZJMkM1mC4bQWctXEgpZFdG3/YD9Z6+/"
        "npdeeolIJILjOFRFw1RFwwBFPce/1/+94zhEIhFeeuklPnv99WjtVmTVGmMIhSzOWr6yYAhms1lG"
        "kgmGhoYYHfXSWk497TQuuvhimpoWvYIJLxcK5JOSlq9YwU1f+yr9BwcYPHyYffv20tfbR1/vHvbt"
        "e46Bw4dxHYe2JWfiuqbs6g3XdZk1K8bdd93LH7ZuLSznSDhEJFxeXZcxhkg4iNaGdCZLPB7nD1u3"
        "8uADD3Ht+ms4cqQ81VnglUK1LTkT13EIBAKcetppLFjwBpoWNdO0qIkFCxZS39jI3JMbuPHLX2HH"
        "jqPLpY6yA/xVkHY04XCEpuYzaG1rQ0pwHMPo6AiHDx1k//P7aV3cRjqTLSv9G/xE2iPcu3EjVVVV"
        "BWs3GqlMUZ0xhmgkiO14FnJVVRX3btzIey5/D+FwBK3HV9oWByEl6UyW1sVtbLzvfubNn0fj7JOp"
        "rq7BsgRag207ZDIZ0o4+pgh6hSHmy3nXdUmn06RSpvB3pSzmzX8Dpzc1k06n0WU63lxXE4tV8+uH"
        "H6avt5d4XR2O61IdCVY05CmEIBoJkhxNEw6H6evt5bHfPca/vP+fGRoqfRUIIdCuQ3VNDasuuBDb"
        "trFtm9HR0cK7+97SyQJWk05fnxFqwoaSzWYZGUmWNXPGPQVXG37zyCMI4Y0fsBQBS1XUlzNxXCEk"
        "v3nkEdzyEsLzEGjtMjKSLOyRE+l2vElatPzwGFN+ubAX3Ahw+NAAXZ2dhCNeKC8YsKbFpySEIBiw"
        "0FoTjoTp6uzk8KEBgsFKFPB5NCnlvWcmJY2Xo0v9/fsZGDiMZQUAsJSi+Lr4KT0xPzZYVoCBgcP0"
        "9+8/kQXcx8SMMkBZkoMvHiSTyeYNK4FSYmLKfoWeB0qJ/AoWZDJZDr54EGXJGWXAjJaiSgGJ4aEJ"
        "pvx0RtNEwYnnui6J4SHkDAfvZmwFvA4PM7oCtIHaeB1KqXEuhkpoJpPhZTeGUoraeB16hpP7ZmwF"
        "CCFwHc3Jp5xMOBxCa5MPPRqmI6YvhGe1eq4UQzgc4uRTTsZ1ZjaXaUYZkMvlmDt3Hg0NjTiODYDj"
        "VsK+OOYT82OD49g0NDQyd+68Gc9jKpoB3gyaUju048JjgE3jbC+MmEl73sSc7UyLVmKMIWc7eTdy"
        "hqXLltE4u4FcRWLZHk1Kee9JGTAx/cNPOwyFQtTUxPLGWLmEMigpePsllxQK8mzHxXZKD3AcCxPH"
        "NUbz9ksuQclSenFNhEFKRU1NjFAoVHA9TDVd5hWbsE94pRThcDgf/HjZGffiCwfY//x+lpy5lOpY"
        "DLeMrAClJKOjaS686EKaFi3iwIEDBINBUukcAatyAX5jDKl0DikEmUyGpkWLuPCiCxkdTaNK6QQy"
        "blxlWYwmk/zpif84rjNuMkZYEwcMBoNELMlgJs2B/c8f0x19+NAh/u/9D3HueecxkswhSnbpetG1"
        "hoZZXLNuHZ+7/noikQi2bZNK56iKlt/rTQjBWCqLk3cXj42Ncc26dTQ0zCrbHW20JhIO8dSfull3"
        "9VU0zp5NQ2PjMd3RDfHqY1rdBQZorYlEImzfto21115L7549vDQ4yOjoCI7jopQkEAh6JaaWRffO"
        "Hay6YFXZC1gpRSIxxporP8ivfvlLnnziCeLxOOm8dVxOTEAIQTqTI53JEggEGB4e5q3nnsuaKz9I"
        "IlFcA5BjweBZ1907d6AsC9u22fvsszyzu4dH/v3XWJaiurqGk+rrWdTczF/7DxxVqA7jGODP/r6+"
        "Xnbt6iYYDGJZFtXVNZ7cxOO47yV9evtTZLOVyQP13LVBbr3tNi679FJGR0cJh8OMpbylG42EinJP"
        "+/eOpTKkMzksyyKdTnPSSSdx62235ctQ7Uq0oCGbdXh6+1MFr2coFCIciXhNmPIZfS/89a/se+45"
        "gsHgK1bBUW/gM6EmFiMYDB61oeh8up/WmnA4zK7ubg707ycUKl9MSClJjaVpbmnmrns2FqoxA4EA"
        "qUyO5EianO2AmLyWq/B3ATnbITmSJpXJEQgECg027rpnI80tzaTGyk+j8cKRIQ7072dXd3ehMMMY"
        "g56guIyn6URaveIt/AEmI6pfajo4OMifnnyCcKQyDfGUpRgeSnL++efxwIMPUF1dzfDwMMFgAFdr"
        "kqNpkiNp0pkctu3kDTfPyaa1wbYd0nlmJUe9rLlg0BM71dXVPPDgA5x//nkMDyVRFdjgPbd2kD89"
        "+QSDg4PH7eZyPJqWNA38Jhy/e/S35LI2ZTbYKsCyFEeOJGhftYpf/fphzj7nbAYHBslms1hKobUh"
        "lc6SHE2TGEkddSVH06TSWbT23M7ZbJbBgUHOPudsfvXrh2lftYojRxJYFdKuhJDksja/e/S3BVdK"
        "KSiJcn5q3tPbt7Gjq4totPw0Dx+WZZFIJHnDwtPZ9POf8a+33crcuXMZHhoimUgUkmGPdTmOQzKR"
        "YHhoiLlz5/Kvt93Kpp//jDcsPJ1EIllSWe2x4H1/hB1dXTy9fVtRRXmv+N5SX8LrajjCL37+U5av"
        "WF5R61UpRTrtyel169fynssv57Hf/e5Vk3MbGxsnSc6tbJa0J4YVv/j5T0mlUjOXnOuLogd/tImF"
        "TacX3AmVhJ+eXl0deU2kp/shzb19z7Lm/avLSkuEMt3RlmUxPDzMQw98j6/f8r9Ip9LlDHdM+LXI"
        "Q0NJAGKxGG866yxWWrLgNTUGnHzaRyLh3ecHxisNYwyhYICHHvgeiUSirNkPZa4AyPf3dGzuu/8H"
        "nLViBclpqpLxMT4beuJ7THcbBO26xGpjPL1tG1dfdQWWVX5Av2x5IaTEdTW3fOMmhoaGUBXa6CZ9"
        "3oR0mammf1QCyrIYGhrilm/c5PWvq4C4LbtBq9GabCZDNptleGgIpSqTL/pag7ffWQwPDZHNZslm"
        "MpgKVN6U/GvLssik02QyGT6ybj0P/XgTp57291kjDH5afo5TT5vDQz/exEfWrSeTyZBJp8tSb19v"
        "VVAkZrRVwevNOjzMSLMOv5fynDlz+R83fpkLLrxg2nTtvxWMt1F+/9jv+Z83fY0DB/qpqqqqbLsa"
        "vyjvvFWr+Ob//hbhcJTRfGuuf5RZPxn81VBdXU0mk+K/f+ZTPL5ly5TdE1PahH0PaF9vL7179iDE"
        "y52i/tHhxx6EgN49e+jr7S3qxI6iGHCgv5/111zNX57eTl1dbUlln5PVeM00Sn0vv3PiX57ezvpr"
        "ruZAf3/lGQDe7l5VXU0qleJj69ex/amnimaCz0i/AOS1Atf1asaKPWtmYtvKVCpFVXV1UZtwUXaA"
        "X704NjZWNBP8aNvBgy9i53LEamOFqNFMwY/2xWpj2LkcBw++OOV09Uo1bpXGmKLkSClM8HXnXC7L"
        "Zz5xHes+chV/3r6NeF2McCRywhnhEz4ciRCvi/Hn7dtY95Gr+MwnriOXyxaqgSZDJVsXS2BX3pye"
        "MgWKZYLrutTEotz53e+wY8cOenbt4uo1V/Clz3+e557tJR6PFbSG6Wo14wfI/WBSPB7juWd7+dLn"
        "P8/Va66gZ9cuduzYwZ3f/Q41seikxKxg826AXa+3r5/p9vWvH+Awwwc4vH6EyQwfYdLU1BQKBoN/"
        "EUKckT+YuKT1PpEJbzxrBcYY/rj1ca67di2RSORVZbtvWdu27fmcXI02Lvd+/0Heeu55Bev7ePCt"
        "0j9sfZxrPrQGKRRSyXyea6BguR4PQgjS6TR33H0Pbzn3PIQQ/OXpbRUhvvGOvBXGmGdyudwbZV9f"
        "Xxb4Yf507LKaN/kb83XXrqWr889kMxlu+fpNU3ZZ+JuwUoqamhpqYjXMnn0y8+bPn3I/Zp+B8+bP"
        "Z/bsk6mJ1VBTU1MIbU5FlPn7zi1fv4lsJkNX55+57tq1lZj54B0bJoAf9vX1ZQUgWlpaZkkpnxFC"
        "1Blj/CNtS4J/iNppc+bQ1LSIx7dsLso55UNISSad5oyWFu7/wU9Keperrngfz+zeTTgSKbrDoe98"
        "PG/V+fT19fLXAwcKrRTKgBFCGGPMkNb6jN27dx+R7e3tavfu3S8ZY74rpZTGmLKe4LcbO3zoEB2P"
        "bymJ+AAyP5MXLFhY9If7PSEWLFiIbdvIEnxWWmuqqqroeHwLhw8dIhqdXDWdKox30LM0xnx39+7d"
        "LxWOMgRkMBj8luu6zyqlLFNmCyyttddwo4yEJfCSgZuaF1GKt1spaGpeVFZvT99msCyrbEPRGKOV"
        "Upbrus8Gg8FvAbJwlCEgOjs7h40x1+ItE02ZpSNT2exe7fdWwKKpqRm3hGFcDU1NzViB8mLUFWoI"
        "W6CpMebazs7OYfKn2Poqhdve3m719PT83nXdr1mWZRXroqg0XNelpibG/AULsHPFiREpBHbOZv6C"
        "BdTUxGbc8WeMcSzLslzX/VpPT8/v8wc6uzDO8u3o6HBWr16tenp6Nti2fY9lWQFjjM30NG44LnxN"
        "pqGhgfr6BrLZLHpc99xXu3S+q0t9fQMNDQ1Fnw1TQRhjjG1ZVsC27Xt6eno2rF69WuUPdAYmZMZt"
        "2rRJA7Knp2ddW1sb+aPN/brRE1bS6jnucpzR0sqpjbNI2QaliiOg6xqi8WrOaGmlt7eXSN7pdwKh"
        "ARMIBAKu697T09OzDpB5GhdwrK/y1VC9ePHir0gpN+TluZN3VUz7VPJriJvPOINly5ZhOw6ySPtQ"
        "G03Asujs7GTPM8+cyK4oJq/tWPkClw27du36Kt4E9lsBFDAZMQtMaGtruxj4tpSyWWvtM0IyzSvC"
        "Y0KWTCZLKRai/5twOEQwWH4VzxSg81au5TUh1HuAT3Z3dz/KJMT333NStLe3Wx0dHc7ChQtrI5HI"
        "p40xH1VKNY7TcMaXtVecIeV4Qn1MY1t7X5QYQPnWvuu6h4UQd6bT6dv37t2b8Gk42SBTESeK/I69"
        "dOnSRsdx1gsh3muMWZI3qV+zcd7pxPhE4LwPbacx5meWZd3V1dV1OH9bgXaTjjPV57W3t4/fvdWS"
        "JUv+SWt9LnA+UG+MWSqKPBT0bxXGGEcI0QUMApullFt37tz5n+SJnZ/1U+rn8P8BOPQCB0uVFZgA"
        "AAAASUVORK5CYII="
    ),
}


def _embedded_icon_img(fname):
    """v25: decodifica un PNG embebido a imagen PIL (o None si no está)."""
    try:
        import base64 as _b64, io as _io
        data = EMBEDDED_ICONS.get(fname)
        if data and HAS_PIL:
            return Image.open(_io.BytesIO(_b64.b64decode(data))).convert("RGBA")
    except Exception as e:
        print(f"icono embebido {fname}: {e}")
    return None

def ensure_builtin_icons():
    """v25: restaura a disco los PNG de fábrica que falten junto al
    programa (APP_DIR). Así: 1) los iconos nunca se pierden aunque se
    muevan los archivos, 2) Configuración vuelve a tener archivo real que
    previsualizar, 3) el .exe no necesita PNG sueltos: los suyos los crea
    al primer arranque."""
    try:
        wanted = set(BUILTIN_ICON_FILES.values()) | {"settings_icon.png"}
        for fn in sorted(wanted):
            p = APP_DIR / fn
            if p.exists():
                continue
            img = _embedded_icon_img(fn)
            if img is not None:
                try:
                    img.save(p)
                    print(f"[UIO Hub v31] PNG de fábrica restaurado "
                          f"desde el programa: {fn}")
                except Exception as e:
                    print(f"[UIO Hub v31] no pude restaurar {fn}: {e}")
    except Exception as e:
        print(f"ensure_builtin_icons: {e}")


# ================== v26: ICONOS PERSONALIZADOS DENTRO DEL PROGRAMA ======
# Los PNG que el usuario asigna a los botones se COPIAN a la carpeta
# "iconos_guardados" (junto al programa, igual que la config). La config
# guarda la ruta de ESA copia: mover o borrar el archivo original ya no
# afecta a ningún botón. Nombre por contenido (ico_<huella>.png): el
# mismo archivo nunca se duplica.
ICON_STORE_DIR = APP_DIR / "iconos_guardados"

def internalizar_icono(ruta):
    """v26: guarda una COPIA del icono dentro de la carpeta del programa
    y devuelve la ruta de esa copia (la original queda intacta).
    - Ruta vacía o archivo inexistente → se devuelve igual (el botón cae
      a su icono de reserva, como siempre).
    - Ruta que YA vive en iconos_guardados → se devuelve igual (no
      duplica).
    - Si la carpeta no se puede crear (ej. exe en carpeta sin permiso de
      escritura) → se devuelve la original (comportamiento de antes)."""
    try:
        if not ruta:
            return ruta
        src = os.path.abspath(str(ruta))
        if not os.path.isfile(src):
            return ruta
        try:
            store = os.path.abspath(str(ICON_STORE_DIR))
            os.makedirs(store, exist_ok=True)
        except Exception:
            return ruta
        if os.path.dirname(src) == store:
            return ruta
        import hashlib as _h
        with open(src, "rb") as fh:
            data = fh.read()
        nombre = "ico_" + _h.md5(data).hexdigest()[:12] \
                 + os.path.splitext(src)[1].lower()
        dest = os.path.join(store, nombre)
        if not os.path.isfile(dest):
            import shutil as _sh
            _sh.copy2(src, dest)
            print(f"[UIO Hub v31] icono guardado dentro del programa: "
                  f"{nombre}")
        return dest
    except Exception as e:
        print(f"internalizar_icono: {e}")
        return ruta

def migrar_iconos_internos(cfg):
    """v26: protege también los iconos ya asignados con versiones
    anteriores: recorre la config (custom_icons + iconos de los botones
    personalizados) y reemplaza cada ruta por su copia interna. Se corre
    UNA VEZ al arrancar; devuelve True si cambió algo (para guardar).
    Los iconos cuyo archivo original YA se movió/perdió antes de esta
    versión no se pueden recuperar: hay que reasignarlos una vez."""
    cambiado = False
    try:
        ci = cfg.get("custom_icons")
        if isinstance(ci, dict):
            for bid, ruta in list(ci.items()):
                nueva = internalizar_icono(ruta)
                if nueva and nueva != ruta:
                    ci[bid] = nueva
                    cambiado = True
        for btn in cfg.get("custom_buttons") or []:
            if not isinstance(btn, dict):
                continue
            ruta = btn.get("icon_path") or ""
            nueva = internalizar_icono(ruta)
            if nueva and nueva != ruta:
                btn["icon_path"] = nueva
                cambiado = True
    except Exception as e:
        print(f"migrar_iconos_internos: {e}")
    return cambiado

def reparar_rutas_iconos(cfg):
    """v26: auto-reparación para cuando la carpeta del programa se MUDA
    (reinstalación con el instalador, mover la carpeta a mano, etc.).
    La config guarda rutas ABSOLUTAS (ej. C:\\Vieja\\iconos_guardados\\
    ico_ab12cd34ef56.png). Si esa ruta ya no existe pero un archivo con
    EL MISMO NOMBRE vive en la carpeta iconos_guardados ACTUAL, se
    re-apunta hacia acá: como el nombre interno se calcula por contenido
    (md5), mismo nombre = mismo icono. Devuelve True si cambió algo."""
    cambiado = False
    try:
        store = str(ICON_STORE_DIR)

        def _fix(ruta):
            nonlocal cambiado
            if not ruta:
                return ruta
            p = os.path.abspath(str(ruta))
            if os.path.isfile(p):
                return ruta                      # vive: nada que hacer
            candidato = os.path.join(store, os.path.basename(p))
            if os.path.isfile(candidato):
                cambiado = True
                print(f"[UIO Hub v31] ruta de icono reparada: "
                      f"{os.path.basename(p)}")
                return candidato
            return ruta                          # perdido: queda igual

        ci = cfg.get("custom_icons")
        if isinstance(ci, dict):
            for bid, ruta in list(ci.items()):
                nueva = _fix(ruta)
                if nueva != ruta:
                    ci[bid] = nueva
        for btn in cfg.get("custom_buttons") or []:
            if not isinstance(btn, dict):
                continue
            ruta = btn.get("icon_path") or ""
            nueva = _fix(ruta)
            if nueva != ruta:
                btn["icon_path"] = nueva
    except Exception as e:
        print(f"reparar_rutas_iconos: {e}")
    return cambiado

DEFAULT_CONFIG = {
    "projects_path": str(Path.home() / "Documents" / "DSH_Projects"),
    # v30: claves de OmniRoute/DSH y del Chrome dedicado retiradas de la
    # config (cmd_omniroute, cmd_dsh, dsh_*, chrome_cdp_port, omni_port).
    "tray_enabled": True,        # v27: icono en la bandeja del sistema
    "opacity_idle": 0.80,
    "opacity_hover": 1.0,
    "window_x": 100,
    "window_y": 100,
    "drive_url": "https://drive.google.com/drive/my-drive",
    "notion_url": "https://www.notion.so",
    "tasks_url": "https://tasks.google.com",
    "chrome_path": "",
    "prefer_chrome": True,
    "custom_buttons": [],
    "custom_icons": {},
    "base_labels": {},          # v21: nombre personalizado de botones del sistema
    "base_targets": {},         # v21: destino personalizado (URL/carpeta)
    "ui_scale": 1.0,
    "autostart_enabled": False,
    "autostart_delay": 3         # v29: autostart_dsh eliminado — DSH SOLO con su botón
}

def load_config():
    src = None
    if CONFIG_FILE.exists(): src = CONFIG_FILE
    elif LEGACY_CONFIG_FILE.exists(): src = LEGACY_CONFIG_FILE
    if src:
        try:
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "custom_buttons" not in data: data["custom_buttons"] = []
            if "custom_icons" not in data: data["custom_icons"] = {}
            if "base_labels" not in data: data["base_labels"] = {}
            if "base_targets" not in data: data["base_targets"] = {}
            return {**DEFAULT_CONFIG, **data}
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando config: {e}")

CONFIG = load_config()

try:
    from PIL import Image, ImageTk, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

def force_light_icon(img, color=ICON_LIGHT):
    """v19 FIX: antes los PNG oscuros se APLANABAN a un solo color claro
    (el ícono del chat quedaba como un cuadrado gris vacío, sin glifo).
    Ahora se preserva el DETALLE: cada pixel se recolorea dentro de un
    rango claro según su luminancia original (oscuro → casi blanco,
    semiclaro → gris claro). Un glifo oscuro sigue viéndose como glifo,
    solo que en tonos claros para el fondo oscuro del dock."""
    try:
        img = img.convert("RGBA")
        px = img.load()
        w, h = img.size
        total = 0.0; count = 0
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a > 40:
                    total += 0.2126 * r + 0.7152 * g + 0.0722 * b
                    count += 1
        if count == 0 or (total / count) >= 120:
            return img
        lo, hi = 150, 248   # rango claro de salida (detalle preservado)
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a <= 0:
                    continue
                L = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
                v = int(lo + (hi - lo) * (1.0 - L))
                px[x, y] = (v, v, v, a)
        return img
    except Exception:
        return img

def image_is_featureless(img, max_std=8.0):
    """v19: True si la imagen visible es prácticamente UN color uniforme
    (sin glifo distinguible). Se usa para descartar PNG del pie que son
    una mancha lisa (no aportan nada visual) y sustituirlos por el ícono
    de reserva dibujado. Solo se aplica a chat/settings del pie."""
    try:
        g = img.convert("RGBA").split()[3]
        w, h = g.size
        px = img.convert("RGBA").load()
        vals = []
        for y in range(0, h, max(1, h // 48)):
            for x in range(0, w, max(1, w // 48)):
                r, gg, b, a = px[x, y]
                if a > 60:
                    vals.append(0.2126 * r + 0.7152 * gg + 0.0722 * b)
        if len(vals) < 8:
            return True   # casi vacía → tratarla como sin detalle
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        return (var ** 0.5) < max_std
    except Exception:
        return False

def draw_chat_glyph(size=96, color=(235, 240, 244, 255)):
    """v19: burbuja de chat dibujada con PIL (ícono de reserva del pie).
    Nada de glifos de fuente: se ve igual en cualquier Windows."""
    S = size * 4
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([S*0.10, S*0.14, S*0.90, S*0.70],
                        radius=int(S*0.16), fill=color)
    d.polygon([(S*0.20, S*0.66), (S*0.20, S*0.90), (S*0.44, S*0.66)], fill=color)
    dot = (24, 26, 30, 255)
    for i, fx in enumerate((0.32, 0.50, 0.68)):
        r = S*0.045
        yy = S*0.42
        d.ellipse([S*fx - r, yy - r, S*fx + r, yy + r], fill=dot)
    return c.resize((size, size), Image.LANCZOS)

def draw_gear_glyph(size=96, color=(235, 240, 244, 255)):
    """v19: engranaje dibujado con PIL (ícono de reserva del pie)."""
    S = size * 4
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    cx = cy = S / 2
    r_out = S * 0.46
    r_in = S * 0.36
    import math as _m
    for k in range(8):
        a0 = _m.radians(k * 45 - 11)
        a1 = _m.radians(k * 45 + 11)
        pts = []
        for a in (a0, a1):
            pts.append((cx + r_out * _m.cos(a), cy + r_out * _m.sin(a)))
        for a in (a1, a0):
            pts.append((cx + r_in * _m.cos(a), cy + r_in * _m.sin(a)))
        d.polygon(pts, fill=color)
    d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], fill=color)
    hole = S * 0.16
    # agujero central: se recorta con máscara (-transparente)
    m = Image.new("L", (S, S), 255)
    dm = ImageDraw.Draw(m)
    dm.ellipse([cx - hole, cy - hole, cx + hole, cy + hole], fill=0)
    r, g, b, a = c.split()
    from PIL import ImageChops
    a = ImageChops.multiply(a, m)
    c = Image.merge("RGBA", (r, g, b, a))
    d2 = ImageDraw.Draw(c)
    # v19: anillo oscuro alrededor del agujero → contraste interno (el
    # engranaje monocromo se vería como una mancha lisa igual que el PNG
    # plano del usuario y el detector lo descartaría)
    dark = (24, 26, 30, 255)
    d2.ellipse([cx - hole, cy - hole, cx + hole, cy + hole],
               outline=dark, width=int(S * 0.035))
    return c.resize((size, size), Image.LANCZOS)

def draw_send_arrow(size=22, color=(16, 20, 26, 255)):
    """v20: flecha ➤ dibujada con PIL para el botón de enviar. FIX de
    dirección: el polígono de v19 apuntaba hacia la IZQUIERDA; ahora la
    punta mira hacia la DERECHA (hacia el dock, como un enviar clásico).
    Cero dependencia de fuentes: polígono sólido antialiased."""
    S = size * 4
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    # punta a la DERECHA, muesca a la izquierda (estilo ➤ clásico)
    d.polygon([(S*0.92, S*0.50), (S*0.08, S*0.10), (S*0.40, S*0.50),
               (S*0.08, S*0.90)], fill=color)
    return c.resize((size, size), Image.LANCZOS)

def draw_harness_arrow(size=18, color=(16, 20, 26, 255)):
    """v19: flecha ↗ dibujada con PIL (modo "Ir a Harness")."""
    S = size * 4
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    w = int(S * 0.14)
    # diagonal de abajo-izquierda a arriba-derecha
    d.line([(S*0.16, S*0.84), (S*0.78, S*0.22)], fill=color, width=w)
    # punta
    d.polygon([(S*0.30, S*0.10), (S*0.90, S*0.10), (S*0.90, S*0.70)], fill=color)
    return c.resize((size, size), Image.LANCZOS)

def _pill_font(px):
    """v19: fuente propia de PIL para hornear el texto de la píldora
    (NO depende de Tk ni del fallback de fuentes de Windows)."""
    try:
        from PIL import ImageFont
        for cand in ("segoeuib.ttf", "arialbd.ttf",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
            try:
                return ImageFont.truetype(cand, px)
            except Exception:
                continue
        return ImageFont.load_default()
    except Exception:
        return None

def draw_send_face(size=46, bg=SEND_BG_RGBA, hover=False, arrow=SEND_TEXT_RGBA):
    """v19: cara COMPLETA del botón de enviar horneada en RGBA: círculo
    UIO Blue + flecha ➤, esquinas transparentes. Se superpone como overlay
    sobre el botón con fondo = clave de transparencia del panel → se ve
    idéntica en CUALQUIER versión de customtkinter (el canvas interno de
    CTkButton dejó de pintarse en 6.x) y sin depender de fuentes.
    v20: flecha corregida — ahora apunta hacia la DERECHA.
    v25 FIX: fondo OPACO PANEL_BG. Antes las esquinas eran transparentes
    y el overlay (bg = clave -transparentcolor) las volvía agujeros al
    escritorio: se veía el CUADRADO del botón sobre el fondo de pantalla."""
    S = size * 4
    c = Image.new("RGBA", (S, S), PANEL_BG_RGBA)   # v25: opaco = color de la barra
    d = ImageDraw.Draw(c)
    d.ellipse([0, 0, S - 1, S - 1], fill=SEND_HOVER_RGBA if hover else bg)
    a = S * 0.52
    ox = oy = (S - a) / 2
    # v20: punta a la DERECHA (antes el polígono quedaba espejado → ◀)
    d.polygon([(ox + a*0.90, oy + a*0.50), (ox + a*0.08, oy + a*0.08),
               (ox + a*0.42, oy + a*0.50), (ox + a*0.08, oy + a*0.92)],
              fill=arrow)
    return c.resize((size, size), Image.LANCZOS)

def draw_pill_face(text="Ir a Harness", h=46, bg=SEND_BG_RGBA, hover=False,
                   arrow=SEND_TEXT_RGBA, tcol=SEND_TEXT_RGBA):
    """v19: píldora COMPLETA horneada en RGBA: cápsula UIO Blue + flecha ↗
    + texto con fuente propia de PIL. Devuelve (imagen, ancho_lógico).
    El texto horneado garantiza que 'Ir a Harness' se VEA siempre: antes
    solo cambiaba un glifo en el círculo y el usuario no lo notaba."""
    S = 4
    H = h * S
    fpx = int(13 * S)
    f = _pill_font(fpx)
    try:
        tw = int(f.getlength(text)) if f is not None else int(len(text) * fpx * 0.58)
    except Exception:
        tw = int(len(text) * fpx * 0.58)
    aw = int(H * 0.32)      # lado de la flecha ↗
    pad_l = int(H * 0.26)
    gap = int(H * 0.18)
    pad_r = int(H * 0.34)
    W = pad_l + aw + gap + tw + pad_r
    c = Image.new("RGBA", (W, H), PANEL_BG_RGBA)   # v25: fondo opaco (sin agujeros)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=H // 2,
                        fill=SEND_HOVER_RGBA if hover else bg)
    ax = pad_l
    ay = (H - aw) // 2
    d.line([(ax + aw*0.08, H - ay - aw*0.08), (ax + aw*0.68, ay + aw*0.32)],
           fill=arrow, width=max(S, int(aw * 0.17)))
    d.polygon([(ax + aw*0.32, ay), (ax + aw*0.98, ay),
               (ax + aw*0.98, ay + aw*0.66)], fill=arrow)
    if f is not None:
        try:
            d.text((ax + aw + gap, H // 2), text, font=f, fill=tcol, anchor="lm")
        except Exception:
            d.text((ax + aw + gap, (H - fpx) // 2), text, font=f, fill=tcol)
    wl = max(46, round(W / S))
    return c.resize((wl, h), Image.LANCZOS), wl

def fit_icon_image(img, size):
    """Escalado que NO recorta: la imagen entra COMPLETA en un lienzo de
    (size x size) con fondo transparente. Si ya es cuadrada queda exactamente
    del tamaño del botón; si no, se centra sin deformar ni cortar lados."""
    try:
        img = img.convert("RGBA")
        w, h = img.size
        if w == size and h == size:
            return img
        scale = min(size / max(1, w), size / max(1, h))
        nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
        img = img.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.paste(img, ((size - nw) // 2, (size - nh) // 2), img)
        return canvas
    except Exception:
        return img

def rounded_tile(img, size, radius, ring=TILE_RING, ring_color=None, ring_px=1):
    """v17 Ronda A (guía §7): icono estilo dock macOS. La imagen entra
    completa en (size x size), se RECORTA con esquinas redondeadas (máscara
    antialiased 4x) y se le dibuja un anillo exterior de 1px ultra sutil.
    El icono ES el botón: sin placa visible alrededor.
    v23c: ring_px permite hornear el aro MÁS GRUESO (2px) — el aro del
    chat abierto pasa de 1px difuminado a 2px nítidos en el borde exterior
    del botón ("un poquito más gruesa, pero muy levemente")."""
    try:
        base = fit_icon_image(img, size)
        ss = 4
        S = size * ss
        R = max(2 * ss, radius * ss)
        big = base.resize((S, S), Image.LANCZOS)
        mask = Image.new("L", (S, S), 0)
        d = ImageDraw.Draw(mask)
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=R, fill=255)
        tile = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        tile.paste(big, (0, 0), mask)
        dd = ImageDraw.Draw(tile)
        dd.rounded_rectangle([0, 0, S - 1, S - 1], radius=R,
                             outline=(ring_color or ring),
                             width=max(ss, int(round(ss * ring_px))))
        return tile.resize((size, size), Image.LANCZOS)
    except Exception:
        return fit_icon_image(img, size)

def dim_tile(tile, factor=0.55):
    """v17 guía §15: atenúa un tile (45-60% de intensidad) multiplicando su
    alfa. Se usa para el botón DeepSeek cuando OmniRoute está apagado."""
    try:
        t = tile.copy()
        r, g, b, a = t.split()
        a = a.point(lambda v: int(v * factor))
        t.putalpha(a)
        return t
    except Exception:
        return tile

# ---------- TOOLTIPS (v17 guía §21: aparecen a los ~450ms) ----------
class Tooltip:
    """Tooltip oscuro de UIO Hub: título + descripción, estilo sobrio.
    Tk no trae tooltips nativos: Toplevel sin decoración + delay propio."""
    def __init__(self, widget, get_text, delay=450):
        self.widget = widget
        self.get_text = get_text
        self.delay = delay
        self._job = None
        self.tip = None
        try:
            widget.bind("<Enter>", self._enter, add="+")
            widget.bind("<Leave>", self._leave, add="+")
            widget.bind("<ButtonPress-1>", self._leave, add="+")
        except Exception:
            pass

    def _cancel(self):
        if self._job:
            try: self.widget.after_cancel(self._job)
            except Exception: pass
            self._job = None

    def _enter(self, _e=None):
        self._cancel()
        try: self._job = self.widget.after(self.delay, self._show)
        except Exception: pass

    def _leave(self, _e=None):
        self._cancel()
        self._hide()

    def _hide(self):
        if self.tip is not None:
            try: self.tip.destroy()
            except Exception: pass
            self.tip = None

    def _show(self):
        self._job = None
        if self.tip is not None:
            return
        try:
            if not self.widget.winfo_exists(): return
        except Exception:
            return
        try: text = self.get_text()
        except Exception: text = None
        if not text: return
        lines = text.split("\n", 1)
        try:
            tw = tk.Toplevel(self.widget)
            tw.overrideredirect(True)
            tw.attributes("-topmost", True)
            tw.withdraw()
            tw.configure(bg="#1e1e1e", highlightthickness=1,
                         highlightbackground="#343434")
            tk.Label(tw, text=lines[0], bg="#1e1e1e", fg="#e8eaed",
                     font=("Segoe UI", 10, "bold"), justify="left"
                     ).pack(anchor="w", padx=10, pady=(5, 1))
            if len(lines) > 1 and lines[1].strip():
                tk.Label(tw, text=lines[1], bg="#1e1e1e", fg="#9a9a9a",
                         font=("Segoe UI", 9), justify="left"
                         ).pack(anchor="w", padx=10, pady=(0, 5))
            tw.update_idletasks()
            wx, wy = self.widget.winfo_rootx(), self.widget.winfo_rooty()
            ww, wh = self.widget.winfo_width(), self.widget.winfo_height()
            tw_w, tw_h = tw.winfo_reqwidth(), tw.winfo_reqheight()
            sw, sh = self.widget.winfo_screenwidth(), self.widget.winfo_screenheight()
            x = wx + ww + 6                     # a la derecha del botón
            if x + tw_w > sw - 8: x = wx - tw_w - 6   # sin lugar → izquierda
            y = wy + max(0, (wh - tw_h) // 2)
            x = max(8, min(sw - tw_w - 8, x))
            y = max(8, min(sh - tw_h - 8, y))
            tw.geometry(f"+{x}+{y}")
            tw.deiconify()
            self.tip = tw
        except Exception:
            self.tip = None

# ---------- API DE DSH ----------
def _api_url(base, method):
    b = str(base or "").rstrip("/")
    if not b: b = "http://127.0.0.1:3080"
    if b.endswith("/api"): return f"{b}/{method}"
    return f"{b}/api/{method}"

def dsh_rpc(base, method, payload):
    url = _api_url(base, method)
    body = {
        "type": "client-request",
        "rpcId": str(uuid.uuid4()),
        "method": method,
        "payload": payload
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=8) as resp:
        raw = resp.read().decode("utf-8")
    try: return json.loads(raw)
    except Exception: return {"raw": raw}

def _find_session_id(obj):
    if isinstance(obj, str):
        if re.match(r"^session-[0-9a-zA-Z\-]{6,}$", obj):
            return obj
    elif isinstance(obj, dict):
        for k in ("sessionId", "session_id", "id"):
            v = obj.get(k)
            if isinstance(v, str) and v.startswith("session-"):
                return v
        for v in obj.values():
            r = _find_session_id(v)
            if r: return r
    elif isinstance(obj, list):
        for v in obj:
            r = _find_session_id(v)
            if r: return r
    return None

SESSION_DISCOVERY_CANDIDATES = [
    ("session/list", {}),
    ("session/list", {"args": {"request": {}}}),
    ("session.list", {}),
    ("session.list", {"args": {"request": {}}}),
    ("sessions/list", {}),
    ("session/getActive", {}),
    ("session/get", {}),
    ("app/state", {}),
]

def dsh_scrape_session_from_html(base):
    try:
        req = urllib.request.Request(base.rstrip("/") + "/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r"session-[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", html)
        if m: return m.group(0)
        m = re.search(r"(session-[0-9a-zA-Z\-]{8,})", html)
        if m: return m.group(1)
    except Exception:
        pass
    return None

def dsh_discover_session(base):
    for method, payload in SESSION_DISCOVERY_CANDIDATES:
        try:
            resp = dsh_rpc(base, method, payload)
            sid = _find_session_id(resp)
            if sid: return sid
        except Exception:
            continue
    return dsh_scrape_session_from_html(base)

def dsh_send_message(base, session_id, text):
    payload = {
        "sessionId": session_id,
        "mode": "queue",
        "content": [{"type": "text", "text": text}],
        "clientTimeZone": CLIENT_TZ
    }
    return dsh_rpc(base, "session.prompt", payload)

def dsh_page_title():
    try:
        req = urllib.request.Request(dsh_base_url() + "/",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=2) as r:
            html = r.read().decode("utf-8", errors="ignore")
        m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
        if m:
            t = m.group(1).strip()
            if t: return t
    except Exception:
        pass
    return None

def dsh_base_url():
    """URL base de DSH desde config (nunca hardcodeada)."""
    for key in ("dsh_url", "dsh_api_base"):
        v = str(CONFIG.get(key) or "").strip()
        if v:
            return v.rstrip("/")
    return "http://127.0.0.1:3080"

def _dsh_hostport():
    """Devuelve 'host:puerto' de la URL de DSH (ej: '127.0.0.1:3080')."""
    try:
        b = dsh_base_url()
        p = urllib.parse.urlparse(b if "://" in b else "http://" + b)
        if p.netloc:
            return p.netloc.lower()
    except Exception:
        pass
    return "127.0.0.1:3080"

def cdp_base_url():
    return f"http://127.0.0.1:{CONFIG.get('chrome_cdp_port', 9222)}"

def cdp_list_tabs(timeout=0.9):
    """Lista de pestañas (type=page) vía CDP, o None si el puerto no responde."""
    try:
        with urllib.request.urlopen(f"{cdp_base_url()}/json", timeout=timeout) as r:
            tabs = json.loads(r.read().decode("utf-8"))
        if isinstance(tabs, list):
            return [t for t in tabs if t.get("type") == "page"]
    except Exception:
        pass
    return None

def cdp_find_dsh_tab(tabs=None):
    """Busca la pestaña de DSH por URL (activa o inactiva)."""
    if tabs is None:
        tabs = cdp_list_tabs()
    if not tabs:
        return None
    hp = _dsh_hostport()
    try:
        port = hp.split(":")[-1]
    except Exception:
        port = "3080"
    for t in tabs:
        url = str(t.get("url", "")).lower()
        for h in ("127.0.0.1", "localhost"):
            if f"{h}:{port}" in url:
                return t
    return None

def cdp_activate_tab(tab_id, timeout=1.5):
    """Activa la pestaña dentro de su ventana de Chrome (GET con fallback PUT)."""
    if not tab_id:
        return False
    for method in ("GET", "PUT"):
        try:
            req = urllib.request.Request(
                f"{cdp_base_url()}/json/activate/{tab_id}", method=method)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                r.read()
            return True
        except Exception:
            continue
    return False

def cdp_open_tab(url, timeout=2.0):
    """Abre url como PESTAÑA NUEVA en el Chrome con depuración (ventana DSH).
    Chrome 111+ exige PUT en /json/new; se reintenta con GET por compatibilidad.
    Devuelve el id de la pestaña o None si no pudo."""
    try:
        q = urllib.parse.quote(url, safe="")
        for method in ("PUT", "GET"):
            try:
                req = urllib.request.Request(
                    f"{cdp_base_url()}/json/new?{q}", method=method)
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    data = json.loads(r.read().decode("utf-8", "replace"))
                if isinstance(data, dict) and data.get("id"):
                    return data["id"]
                return True
            except Exception:
                continue
    except Exception as e:
        print(f"cdp_open_tab: {e}")
    return None


# ---------- v27: ARRANQUE DE CHROME SIN CARRERAS ----------
# El Chrome dedicado tarda 2-5 s en arrancar y mientras tanto el puerto de
# depuración (CDP) no responde. Antes, cada consulta hecha en ese lapso
# devolvía None y la app lanzaba OTRO comando de Chrome → ventana nueva en
# vez de pestaña. Ahora TODO lanzamiento marca la hora y las consultas hechas
# durante el arranque ESPERAN a que el puerto responda.
CHROME_LAST_LAUNCH = 0.0    # time.time() del último lanzamiento del Chrome dedicado
CDP_MARKED_DEAD = False     # CDP no respondió ni esperando: no penalizar cada clic

def mark_chrome_launched():
    """v27: registra que acabamos de lanzar el Chrome dedicado."""
    global CHROME_LAST_LAUNCH
    CHROME_LAST_LAUNCH = time.time()

def cdp_wait_ready(max_wait=8.0, interval=0.4):
    """v27: sondea el puerto de depuración hasta que responda o se agote el
    tiempo. Devuelve la lista de pestañas o None si nunca respondió."""
    fin = time.time() + max(0.0, float(max_wait))
    while True:
        tabs = cdp_list_tabs()
        if tabs is not None:
            return tabs
        if time.time() >= fin:
            return None
        time.sleep(interval)

def cdp_tabs_smart():
    """v27: lista de pestañas con espera inteligente al arranque de Chrome.
    - Si CDP responde → lista.
    - Si no responde pero el Chrome se lanzó hace poco (<15 s) → ESPERA
      (hasta ~10 s): el Chrome está arrancando, no lanzar otro.
    - Si ya esperó y nunca respondió → None sin volver a esperar (para no
      penalizar cada clic cuando el puerto está realmente caído).
      El flag se limpia solo en cuanto CDP vuelve a responder."""
    global CDP_MARKED_DEAD
    tabs = cdp_list_tabs()
    if tabs is not None:
        CDP_MARKED_DEAD = False
        return tabs
    if CDP_MARKED_DEAD:
        return None
    desde = time.time() - CHROME_LAST_LAUNCH
    if desde > 15:
        return None
    restante = min(15 - desde, 10)
    print(f"[UIO Hub v31] Chrome arrancando: espero el puerto de depuración "
          f"(hasta {restante:.0f}s)...")
    tabs = cdp_wait_ready(restante)
    if tabs is not None:
        CDP_MARKED_DEAD = False
        return tabs
    CDP_MARKED_DEAD = True
    return None

def _ps_quote(s):
    return str(s).replace("'", "''")

def get_dsh_profile_dir():
    """Perfil dedicado de Chrome para DSH. Chrome 136+ exige --user-data-dir
    propio para permitir el puerto de depuración (por eso nunca anduvo)."""
    return Path(os.path.expandvars(r"%LocalAppData%")) / "UIOHub" / "ChromeProfile"

def launch_dsh_chrome_debug():
    """Abre el Chrome DEDICADO de DSH con puerto de depuración.
    Si ya está corriendo, Chrome reenvía el comando y abre la pestaña ahí mismo."""
    chrome = get_chrome_exe()
    if not chrome:
        return False, "✗ Chrome no encontrado"
    profile = get_dsh_profile_dir()
    try:
        profile.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    try:
        mark_chrome_launched()   # v27: el puerto tarda unos segundos en vivir
        subprocess.Popen([
            chrome,
            f"--user-data-dir={profile}",
            f"--remote-debugging-port={CONFIG.get('chrome_cdp_port', 9222)}",
            "--no-first-run",
            "--no-default-browser-check",
            dsh_base_url() + "/",
        ])
        return True, "✓ Chrome DSH (perfil dedicado) abierto"
    except Exception as e:
        return False, f"✗ {str(e)[:40]}"

def create_chrome_debug_shortcut():
    chrome = get_chrome_exe()
    if not chrome:
        return False, "✗ Chrome no encontrado"
    lnk = Path.home() / "Desktop" / "Chrome DSH (dedicado).lnk"
    profile = get_dsh_profile_dir()
    port = CONFIG.get("chrome_cdp_port", 9222)
    ps = (f"$ws = New-Object -ComObject WScript.Shell; "
          f"$sc = $ws.CreateShortcut('{_ps_quote(lnk)}'); "
          f"$sc.TargetPath = '{_ps_quote(chrome)}'; "
          f"$sc.Arguments = '--user-data-dir=\"{_ps_quote(profile)}\" "
          f"--remote-debugging-port={port} --no-first-run --no-default-browser-check'; "
          "$sc.Save()")
    try:
        subprocess.run(["powershell.exe", "-Command", ps],
                       creationflags=0x08000000, capture_output=True)
        return True, "✓ Acceso directo creado en el Escritorio"
    except Exception as e:
        return False, f"✗ {str(e)[:40]}"

def _is_valid_dsh_title(title):
    if not title:
        return False
    t = title.lower()
    dsh_markers = ["deepseek", "dsh", "harness", "127.0.0.1:3080", "localhost:3080"]
    return any(m in t for m in dsh_markers)

# ---------- VENTANAS / CHROME (AHORA CON HANDLES CORRECTOS) ----------
def set_dark_titlebar(win):
    try:
        try: win.update_idletasks()
        except: pass
        u = ctypes.windll.user32
        hwnds = [win.winfo_id()]
        try: hwnds.append(u.GetParent(win.winfo_id()))
        except: pass
        SWP_NOMOVE, SWP_NOSIZE, SWP_NOZORDER, SWP_FRAMECHANGED = 0x0002, 0x0001, 0x0004, 0x0020
        val = ctypes.c_int(1)
        for hwnd in hwnds:
            for attr in (20, 19):
                try:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(val), ctypes.sizeof(val))
                except: pass
            try:
                u.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
            except: pass
    except: pass

def force_dark_appearance(win):
    try:
        win.update_idletasks(); win.update()
    except: pass
    set_dark_titlebar(win)
    def _on_map(e=None):
        set_dark_titlebar(win)
        try: win.unbind("<Map>")
        except: pass
    win.bind("<Map>", _on_map, add="+")


def get_root_hwnd(win):
    """HWND de la ventana RAÍZ real (el toplevel), no de un widget interno.
    winfo_id() puede devolver el HWND de un hijo: sobre él, SetWindowRgn no
    recorta la ventana visible (por eso los artefactos en las esquinas)."""
    try:
        u = ctypes.windll.user32
        hwnd = win.winfo_id()
        root = u.GetAncestor(hwnd, 2)          # GA_ROOT = 2
        return int(root) if root else int(hwnd)
    except Exception:
        try:
            return int(win.winfo_id())
        except Exception:
            return 0


def apply_window_region(win, w, h, radius):
    """Recorta la ventana con esquinas redondeadas, sobre el HWND RAÍZ.
    Devuelve True si Windows aceptó la región."""
    try:
        u = ctypes.windll.user32
        hwnd = get_root_hwnd(win)
        hrgn = ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, int(w) + 1, int(h) + 1,
                                                      int(radius), int(radius))
        return bool(u.SetWindowRgn(hwnd, hrgn, 1))
    except Exception as e:
        print(f"region error: {e}")
        return False


def safe_grab(win, delay_ms=150):
    """grab_set diferido: sobre un CTkToplevel el grab inmediato puede fallar
    porque la ventana todavía no es 'viewable'."""
    def _g():
        try:
            win.grab_set()
        except Exception:
            pass
    win.after(delay_ms, _g)


def enum_windows():
    windows = []
    try:
        u = ctypes.windll.user32
        @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        def callback(hwnd, lparam):
            try:
                if u.IsWindowVisible(hwnd):
                    length = u.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buff = ctypes.create_unicode_buffer(length + 1)
                        u.GetWindowTextW(hwnd, buff, length + 1)
                        title = buff.value
                        if title.strip():
                            windows.append((hwnd, title))
            except: pass
            return True
        u.EnumWindows(callback, 0)
    except Exception as e:
        print(f"enum_windows error: {e}")
    return windows

def force_focus_hwnd(hwnd):
    """Combo completo anti-Foreground-Lock + VERIFICACIÓN honesta.
    Devuelve True SOLO si GetForegroundWindow() == hwnd (ya no miente)."""
    if not hwnd:
        return False
    try:
        u = ctypes.windll.user32
        k = ctypes.windll.kernel32
        try:
            if (u.GetForegroundWindow() or 0) == hwnd:
                return True
        except Exception:
            pass
        # 1) Restaurar si está minimizada
        try:
            if u.IsIconic(hwnd):
                u.ShowWindow(hwnd, 9)      # SW_RESTORE
            else:
                u.ShowWindow(hwnd, 5)      # SW_SHOW
        except Exception:
            pass
        # 2) Truco ALT: una tecla "de usuario" habilita SetForegroundWindow
        try:
            u.keybd_event(0x12, 0, 0, 0)   # ALT down
            time.sleep(0.01)
            u.keybd_event(0x12, 0, 2, 0)   # ALT up
        except Exception:
            pass
        # 3) AttachThreadInput con el thread de la ventana en primer plano
        this_tid = k.GetCurrentThreadId()
        fg = u.GetForegroundWindow() or 0
        fg_tid = u.GetWindowThreadProcessId(fg, None) if fg else 0
        attached = False
        try:
            if fg_tid and fg_tid != this_tid:
                attached = bool(u.AttachThreadInput(this_tid, fg_tid, True))
            u.BringWindowToTop(hwnd)
            u.SetActiveWindow(hwnd)
            u.SetForegroundWindow(hwnd)
        except Exception:
            pass
        finally:
            if attached:
                try: u.AttachThreadInput(this_tid, fg_tid, False)
                except Exception: pass
        # 4) Respaldo: SwitchToThisWindow (equivale a un Alt+Tab)
        time.sleep(0.06)
        try:
            if (u.GetForegroundWindow() or 0) != hwnd:
                u.SwitchToThisWindow(hwnd, True)
        except Exception:
            pass
        # 5) Verificación honesta
        time.sleep(0.06)
        return (u.GetForegroundWindow() or 0) == hwnd
    except Exception as e:
        print(f"force_focus error: {e}")
        return False

def find_and_focus_window(keywords):
    """Busca ventana por título y la enfoca con el combo completo.
    Devuelve (ok_verificado, título) — el resultado ya NO miente."""
    try:
        wins = enum_windows()
        for hwnd, title in wins:
            t_lower = title.lower()
            for kw in keywords:
                if kw and kw.lower() in t_lower:
                    if force_focus_hwnd(hwnd):
                        print(f"✓ Ventana enfocada (verificado): {title}")
                        return True, title
                    print(f"✗ Encontré '{title[:50]}' pero Windows negó el foco")
                    return False, title
    except Exception as e:
        print(f"find_and_focus error: {e}")
    return False, None

def get_foreground_chrome_title():
    try:
        u = ctypes.windll.user32
        hwnd = u.GetForegroundWindow()
        cls = ctypes.create_unicode_buffer(256)
        u.GetClassNameW(hwnd, cls, 256)
        if cls.value == "Chrome_WidgetWin_1":
            buff = ctypes.create_unicode_buffer(1024)
            u.GetWindowTextW(hwnd, buff, 1024)
            t = buff.value.strip()
            if t: return t
    except Exception as e:
        print(f"foreground error: {e}")
    return None

def is_window_open(keywords):
    try:
        wins = enum_windows()
        for hwnd, title in wins:
            t_lower = title.lower()
            for kw in keywords:
                if kw.lower() in t_lower:
                    return True
    except: pass
    return False

def get_chrome_exe():
    if CONFIG.get("chrome_path") and Path(CONFIG["chrome_path"]).exists():
        return CONFIG["chrome_path"]
    try:
        import winreg
        for root_key in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(root_key,
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
                        0, winreg.KEY_READ) as key:
                    path, _ = winreg.QueryValueEx(key, "")
                    if path and os.path.exists(path):
                        return path
            except: pass
    except: pass
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def open_url_smart(url, prefer_chrome=True):
    if not url: return
    if not url.startswith("http"): url = "https://" + url
    chrome = get_chrome_exe()
    if chrome:
        try:
            subprocess.Popen([chrome, url])
            return
        except Exception as e:
            print(f"Error abriendo Chrome: {e}")
    print("✗ Chrome no encontrado. Configurá la ruta en ⚙ → General.")

def launch_powershell(cmd):
    try:
        subprocess.Popen(["powershell.exe", "-NoExit", "-Command", cmd],
                         creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
    except FileNotFoundError:
        try:
            subprocess.Popen(["pwsh.exe", "-NoExit", "-Command", cmd],
                             creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
        except Exception as e:
            print(e)

def open_folder(path_str):
    p = Path(path_str)
    if not p.exists():
        try: p.mkdir(parents=True, exist_ok=True)
        except: pass
    try: os.startfile(str(p))
    except Exception as e: print(e)

def set_autostart_windows(enable):
    if sys.platform != "win32": return False
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        if getattr(sys, 'frozen', False):
            exe_path = f'"{sys.executable}"'
        else:
            python_dir = Path(sys.executable).parent
            pythonw = python_dir / "pythonw.exe"
            if pythonw.exists():
                exe_path = f'"{pythonw}" "{Path(__file__).resolve()}"'
            else:
                exe_path = f'"{sys.executable}" "{Path(__file__).resolve()}"'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            if enable:
                try: winreg.DeleteValue(key, AUTOSTART_KEY_LEGACY)
                except FileNotFoundError: pass
                winreg.SetValueEx(key, AUTOSTART_KEY, 0, winreg.REG_SZ, exe_path)
            else:
                for name in (AUTOSTART_KEY, AUTOSTART_KEY_LEGACY):
                    try: winreg.DeleteValue(key, name)
                    except FileNotFoundError: pass
        return True
    except Exception as e:
        print(f"Error autostart: {e}")
        return False

def is_autostart_enabled():
    if sys.platform != "win32": return False
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ) as key:
            try:
                winreg.QueryValueEx(key, AUTOSTART_KEY)
                return True
            except FileNotFoundError:
                return False
    except: return False

def is_omniroute_running(port=None):
    port = port or CONFIG.get("omni_port", 20128)
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=1):
            return True
    except: return False

def is_dsh_running():
    try:
        req = urllib.request.urlopen(dsh_base_url() + "/", timeout=1.5)
        if req.status == 200:
            req.close()
            return True
        req.close()
    except: pass
    dsh_port = CONFIG.get("dsh_port", 3080)
    try:
        with socket.create_connection(("127.0.0.1", int(dsh_port)), timeout=0.5):
            return True
    except: pass
    return False


def _effective_scaling(win):
    """v15: factor de escala EFECTIVO de una ventana CTk (DPI de SU monitor
    × escala global). Es el mismo factor por el que CTk multiplica el ancho
    y alto de geometry(). En PCs con multimonitor/4K puede diferir de la
    compensación que se le aplicó al dock → era la causa del solape del
    chat (la barra se dibujaba más ancha que el ancho lógico 470)."""
    try:
        f = float(win._get_window_scaling())
        if f > 0.2:
            return f
    except Exception:
        pass
    try:
        f = float(ctk.ScalingTracker.window_scaling)
        if f > 0.2:
            return f
    except Exception:
        pass
    return 1.0


# ---------- v27b: BANDEJA DEL SISTEMA (ICONO DE NOTIFICACIONES) ----------
# El dock deja de tener botón en la barra de tareas y vive como las apps
# "de segundo plano": un icono en la zona de notificaciones (junto al
# reloj / iconos ocultos).
#   - Clic IZQUIERDO en el icono → mostrar / ocultar el dock.
#   - Clic DERECHO → menú: "Mostrar / ocultar UIO Hub" y "Salir".
# Implementación 100% ctypes: ventana oculta propia en un hilo aparte +
# Shell_NotifyIconW (NIM_ADD). Cero dependencias nuevas: el .exe compila
# igual. Las órdenes del usuario se ENCOLAN y el hilo de Tk las consume
# con un poller (after 120ms) — desde este hilo NUNCA se toca Tk.
import ctypes.wintypes as _wt

_NIM_ADD, _NIM_MODIFY, _NIM_DELETE = 0, 1, 2
_NIF_MESSAGE, _NIF_ICON, _NIF_TIP, _NIF_INFO = 0x01, 0x02, 0x04, 0x10
_NIIF_INFO = 0x01
_WM_APP_TRAY = 0x8000              # WM_APP: callback del icono
_TPM_RETURNCMD, _TPM_NONOTIFY, _TPM_RIGHTBUTTON = 0x0100, 0x0080, 0x0004
_MF_STRING, _MF_SEPARATOR = 0x00000000, 0x00000800
_IDC_TOGGLE, _IDC_QUIT = 1001, 1002

class _NOTIFYICONDATAW(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [("uTimeout", ctypes.c_uint),
                    ("uVersion", ctypes.c_uint)]
    _fields_ = [
        ("cbSize", ctypes.c_uint32),
        ("hWnd", ctypes.c_void_p),
        ("uID", ctypes.c_uint32),
        ("uFlags", ctypes.c_uint32),
        ("uCallbackMessage", ctypes.c_uint32),
        ("hIcon", ctypes.c_void_p),
        ("szTip", ctypes.c_wchar * 128),
        ("dwState", ctypes.c_uint32),
        ("dwStateMask", ctypes.c_uint32),
        ("szInfo", ctypes.c_wchar * 256),
        ("uTimeoutOrVersion", ctypes.c_uint32),
        ("szInfoTitle", ctypes.c_wchar * 64),
        ("dwInfoFlags", ctypes.c_uint32),
        ("guidItem", ctypes.c_uint8 * 16),
    ]

def hide_taskbar_button(win):
    """v27b: quita el botón de la barra de tareas del dock (WS_EX_TOOLWINDOW
    sobre el HWND raíz). La ventana queda 'solo en la bandeja', como las
    apps de segundo plano. También la saca de Alt-Tab (comportamiento
    estándar de las tool windows). Devuelve True si quedó aplicado."""
    if sys.platform != "win32":
        return False
    try:
        u = ctypes.windll.user32
        hwnd = get_root_hwnd(win)
        if not hwnd:
            return False
        GWL_EXSTYLE = -20
        WS_EX_TOOLWINDOW = 0x00000080
        if hasattr(u, "GetWindowLongPtrW"):
            st = u.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        else:
            st = u.GetWindowLongW(hwnd, GWL_EXSTYLE)
        if st is None:
            return False
        if st & WS_EX_TOOLWINDOW:
            return True             # ya está oculto (no tocar)
        nuevo = st | WS_EX_TOOLWINDOW
        if hasattr(u, "SetWindowLongPtrW"):
            u.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, nuevo)
        else:
            u.SetWindowLongW(hwnd, GWL_EXSTYLE, nuevo)
        # v31c: refresco del estilo de la ventana SIN ocultarla. Antes se
        # hacía withdraw()+deiconify(); justo en el arranque de Windows ese
        # par podía dejar el dock escondido (y solo quedaba el icono de la
        # bandeja). SetWindowPos con FRAMECHANGED refresca sin tapar nada.
        try:
            _SWP_NOSIZE, _SWP_NOMOVE, _SWP_NOZORDER = 0x0001, 0x0002, 0x0004
            _SWP_FRAMECHANGED, _SWP_SHOWWINDOW = 0x0020, 0x0040
            u.SetWindowPos(hwnd, None, 0, 0, 0, 0,
                           _SWP_NOSIZE | _SWP_NOMOVE | _SWP_NOZORDER |
                           _SWP_FRAMECHANGED | _SWP_SHOWWINDOW)
        except Exception:
            pass
        return True
    except Exception as e:
        print(f"[UIO Hub v31] hide_taskbar_button: {e}")
        return False

class UIOTrayIcon:
    """Icono de bandeja con su propia ventana de mensajes (hilo aparte).
    Órdenes disponibles para el hilo de Tk: pop_commands() → [CMD_TOGGLE |
    CMD_QUIT]. notify() muestra un globo. stop() lo desinstala y cierra."""

    CMD_TOGGLE = 1
    CMD_QUIT = 2
    _CLS_NAME = "UIOHubTrayWnd27"

    def __init__(self, tooltip="UIO Hub"):
        self.tooltip = (tooltip or "UIO Hub")[:127]
        self._q = []
        self._lock = threading.Lock()
        self._thread = None
        self._hwnd = None
        self._nid = None
        self._hicon = None
        self._ico_src = None
        self._ico_tmp = None
        self._cbproc = None          # mantiene vivo el callback Win32
        self._msg_taskbar = 0

    # ---------- API para el hilo de Tk ----------
    def start(self):
        """Lanza el hilo de la bandeja. Devuelve True si el icono quedó
        instalado (espera hasta ~3 s). Fuera de Windows no hace nada."""
        if sys.platform != "win32":
            return False
        self._thread = threading.Thread(target=self._run, daemon=True,
                                        name="UIOHubTray")
        self._thread.start()
        for _ in range(60):
            if self._ready():
                return True
            time.sleep(0.05)
        return False

    def _ready(self):
        with self._lock:
            return bool(self._hwnd and self._nid)

    def pop_commands(self):
        with self._lock:
            cmds = list(self._q)
            self._q = []
        return cmds

    def notify(self, title, msg):
        """Globo de notificación (no roba foco; Windows lo muestra 1 vez)."""
        with self._lock:
            nid = self._nid
        if not nid:
            return
        try:
            n = _NOTIFYICONDATAW()
            n.cbSize = ctypes.sizeof(_NOTIFYICONDATAW)
            n.hWnd = nid.hWnd
            n.uID = nid.uID
            n.uFlags = _NIF_INFO
            n.szInfo = (msg or "")[:255]
            n.szInfoTitle = (title or "")[:63]
            n.dwInfoFlags = _NIIF_INFO
            n.uTimeoutOrVersion = 3000
            ctypes.windll.shell32.Shell_NotifyIconW(_NIM_MODIFY,
                                                    ctypes.byref(n))
        except Exception:
            pass

    def stop(self):
        """Quita el icono y cierra el hilo (join ≤2s)."""
        try:
            if self._hwnd:
                ctypes.windll.user32.PostMessageW(self._hwnd, 0x0010, 0, 0)
        except Exception:
            pass
        t = self._thread
        if t and t.is_alive():
            t.join(timeout=2.0)

    # ---------- hilo propio (Win32) ----------
    def _run(self):
        try:
            self._run_inner()
        except Exception as e:
            print(f"[UIO Hub v31] bandeja: {e}")

    def _run_inner(self):
        u = ctypes.windll.user32
        k = ctypes.windll.kernel32
        shell = ctypes.windll.shell32

        WNDPROC = ctypes.WINFUNCTYPE(_wt.LPARAM, _wt.HWND, _wt.UINT,
                                     _wt.WPARAM, _wt.LPARAM)
        self._cbproc = WNDPROC(self._wnd_proc)

        class WNDCLASSW(ctypes.Structure):
            _fields_ = [("style", ctypes.c_uint),
                        ("lpfnWndProc", WNDPROC),
                        ("cbClsExtra", ctypes.c_int),
                        ("cbWndExtra", ctypes.c_int),
                        ("hInstance", ctypes.c_void_p),
                        ("hIcon", ctypes.c_void_p),
                        ("hCursor", ctypes.c_void_p),
                        ("hbrBackground", ctypes.c_void_p),
                        ("lpszMenuName", ctypes.c_wchar_p),
                        ("lpszClassName", ctypes.c_wchar_p)]

        hinst = k.GetModuleHandleW(None)
        wc = WNDCLASSW()
        wc.lpfnWndProc = self._cbproc
        wc.hInstance = hinst
        wc.lpszClassName = self._CLS_NAME
        u.RegisterClassW(ctypes.byref(wc))
        # ventana oculta normal (NO message-only: la bandeja exige una
        # ventana "de verdad" para recibir el callback del icono)
        self._hwnd = u.CreateWindowExW(0, self._CLS_NAME, "UIOHubTray",
                                       0, 0, 0, 0, 0, None, None, hinst, None)
        if not self._hwnd:
            raise RuntimeError("CreateWindowExW falló")
        self._msg_taskbar = u.RegisterWindowMessageW("TaskbarCreated")
        self._hicon, self._ico_src = self._load_icon()

        nid = _NOTIFYICONDATAW()
        nid.cbSize = ctypes.sizeof(_NOTIFYICONDATAW)
        nid.hWnd = self._hwnd
        nid.uID = 1
        nid.uFlags = _NIF_MESSAGE | _NIF_ICON | _NIF_TIP
        nid.uCallbackMessage = _WM_APP_TRAY
        nid.hIcon = self._hicon
        nid.szTip = self.tooltip
        # el tray de Explorer puede tardar en estar listo (autostart al
        # encender la PC): reintentar hasta ~30 s. self._nid se publica SOLO
        # cuando el icono quedó realmente instalado: asi _ready() miente
        # nunca y el ✕ sabe si el icono existe de verdad.
        for intento in range(15):
            if shell.Shell_NotifyIconW(_NIM_ADD, ctypes.byref(nid)):
                with self._lock:
                    self._nid = nid
                break
            time.sleep(2.0)
        else:
            print("[UIO Hub v31] la bandeja nunca respondió (¿sin Explorer?)")

        msg = _wt.MSG()
        while u.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            u.TranslateMessage(ctypes.byref(msg))
            u.DispatchMessageW(ctypes.byref(msg))
        self._delete_icon()

    def _wnd_proc(self, hwnd, msg, wparam, lparam):
        u = ctypes.windll.user32
        try:
            if msg == _WM_APP_TRAY:
                ev = lparam & 0xFFFF
                if ev == 0x0202:            # WM_LBUTTONUP: mostrar/ocultar
                    with self._lock:
                        self._q.append(self.CMD_TOGGLE)
                elif ev == 0x0205:          # WM_RBUTTONUP: menú
                    self._menu(hwnd)
                return 0
            if msg == self._msg_taskbar:    # Explorer reiniciado: re-agregar
                try:
                    self._delete_icon()
                    ctypes.windll.shell32.Shell_NotifyIconW(
                        _NIM_ADD, ctypes.byref(self._nid))
                except Exception:
                    pass
                return 0
            if msg == 0x0010:               # WM_CLOSE: apagar hilo limpio
                self._delete_icon()
                u.DestroyWindow(hwnd)
                return 0
            if msg == 0x0002:               # WM_DESTROY
                u.PostQuitMessage(0)
                return 0
        except Exception as e:
            print(f"[UIO Hub v31] tray wndproc: {e}")
        return u.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _menu(self, hwnd):
        """Menú contextual (clic derecho). SetForegroundWindow antes del
        TrackPopupMenu es EL fix clásico del menú que no se cierra."""
        u = ctypes.windll.user32
        pt = _wt.POINT()
        u.GetCursorPos(ctypes.byref(pt))
        menu = u.CreatePopupMenu()
        u.AppendMenuW(menu, _MF_STRING, _IDC_TOGGLE,
                      "Mostrar / ocultar UIO Hub")
        u.AppendMenuW(menu, _MF_SEPARATOR, 0, None)
        u.AppendMenuW(menu, _MF_STRING, _IDC_QUIT, "Salir")
        u.SetForegroundWindow(hwnd)
        cmd = u.TrackPopupMenuEx(
            menu, _TPM_RETURNCMD | _TPM_NONOTIFY | _TPM_RIGHTBUTTON,
            pt.x, pt.y, hwnd, None)
        u.PostMessageW(hwnd, 0x0000, 0, 0)   # WM_NULL: cierre limpio del menú
        u.DestroyMenu(menu)
        with self._lock:
            if cmd == _IDC_TOGGLE:
                self._q.append(self.CMD_TOGGLE)
            elif cmd == _IDC_QUIT:
                self._q.append(self.CMD_QUIT)

    def _delete_icon(self):
        try:
            if self._nid:
                ctypes.windll.shell32.Shell_NotifyIconW(
                    _NIM_DELETE, ctypes.byref(self._nid))
        except Exception:
            pass

    # ---------- icono ----------
    def _load_icon(self):
        """HICON para la bandeja, en orden de preferencia:
        1) el icono del propio .exe (instalador: uio_hub.ico del usuario)
        2) uio_hub.ico junto al programa
        3) horneado al vuelo desde el PNG embebido (PIL) — mismo estilo
        4) icono genérico de aplicación (nunca debería llegar aquí)"""
        u = ctypes.windll.user32
        IMAGE_ICON, LR_LOADFROMFILE = 1, 0x10
        # 1) exe con icono
        if getattr(sys, "frozen", False):
            try:
                big = ctypes.c_void_p()
                small = ctypes.c_void_p()
                if ctypes.windll.shell32.ExtractIconExW(
                        sys.executable, 0, ctypes.byref(big),
                        ctypes.byref(small), 1):
                    if big.value:
                        return big.value, "exe"
                    if small.value:
                        return small.value, "exe"
            except Exception:
                pass
        # 2) uio_hub.ico junto al programa
        try:
            p = Path(sys.executable).parent / "uio_hub.ico" \
                if getattr(sys, "frozen", False) \
                else Path(__file__).resolve().parent / "uio_hub.ico"
            if not p.exists() and getattr(sys, "frozen", False):
                p = Path(getattr(sys, "_MEIPASS", "")) / "uio_hub.ico"
            if p.exists():
                h = u.LoadImageW(None, str(p), IMAGE_ICON, 0, 0,
                                 LR_LOADFROMFILE)
                if h:
                    return h, "ico"
        except Exception:
            pass
        # 3) PNG embebido → .ico temporal (el engranaje = identidad UIO)
        try:
            if HAS_PIL and "settings_icon.png" in EMBEDDED_ICONS:
                import base64 as _b64
                import io as _io
                from PIL import Image as _Img
                raw = _b64.b64decode(EMBEDDED_ICONS["settings_icon.png"])
                img = _Img.open(_io.BytesIO(raw)).convert("RGBA")
                tmp = Path(os.path.expandvars(r"%TEMP%")) / "uio_hub_tray.ico"
                img.save(str(tmp), sizes=[(16, 16), (24, 24), (32, 32),
                                          (48, 48)])
                h = u.LoadImageW(None, str(tmp), IMAGE_ICON, 0, 0,
                                 LR_LOADFROMFILE)
                if h:
                    self._ico_tmp = tmp
                    return h, "png-embebido"
        except Exception as e:
            print(f"[UIO Hub v31] icono de bandeja horneado falló: {e}")
        # 4) genérico
        try:
            return u.LoadIconW(None, 32512), "generico"   # IDI_APPLICATION
        except Exception:
            return None, "ninguno"


# ---------- DIÁLOGO BOTÓN CUSTOM ----------
class UIOHubButtonDialog(ctk.CTkToplevel):
    """v21: diálogo ÚNICO para crear/editar cualquier botón del dock.
    mode="custom" → botón personalizado (nombre + tipo + destino + icono).
    mode="base"   → botón del sistema: nombre + icono y, SOLO si
                    editable_target=True, también el destino (URL/carpeta).
                    El tipo se muestra FIJO (no se puede cambiar).
    mode="icon"   → solo icono (Chat/Configuración del pie)."""
    def __init__(self, parent, existing=None, mode="custom",
                 fixed_type=None, editable_target=True, title=None):
        super().__init__(parent)
        self.withdraw()
        self.result = None
        self.mode = mode
        self.title(title or f"{APP_TITLE} - Botón personalizado")
        self.configure(fg_color=BG_POPUP)
        self.attributes("-topmost", True)
        self.transient(parent)
        self.existing = existing or {}

        main = ctk.CTkFrame(self, fg_color=BG_POPUP, corner_radius=0)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- nombre (no aplica a mode="icon") ---
        if mode != "icon":
            ctk.CTkLabel(main, text="Nombre:", text_color="white",
                         font=("Segoe UI", 14), anchor="w").pack(anchor="w", fill=tk.X)
            self.label_var = tk.StringVar(value=self.existing.get("label", ""))
            ctk.CTkEntry(main, textvariable=self.label_var, fg_color="#2a2a2a",
                         border_color="#3a3a3a", text_color="white",
                         font=("Segoe UI", 14)).pack(fill=tk.X, pady=(2, 12))

        # --- tipo ---
        show_target = (mode == "custom") or (mode == "base" and editable_target)
        if mode == "custom":
            ctk.CTkLabel(main, text="Tipo:", text_color="white",
                         font=("Segoe UI", 14), anchor="w").pack(anchor="w", fill=tk.X)
            self.type_var = tk.StringVar(value=self.existing.get("type", "web"))
            ctk.CTkOptionMenu(main, values=["web", "folder", "shell"],
                              variable=self.type_var, fg_color="#2a2a2a",
                              button_color="#3a3a3a", button_hover_color="#4a4a4a",
                              text_color="white", font=("Segoe UI", 14),
                              dropdown_fg_color="#2a2a2a", dropdown_text_color="white",
                              dropdown_hover_color="#3a3a3a",
                              dropdown_font=("Segoe UI", 14)).pack(fill=tk.X, pady=(2, 10))
        elif mode == "base":
            tipo_txt = {"web": "Web (abre una URL)",
                        "folder": "Carpeta",
                        "shell": "Interno (no editable)"}.get(fixed_type or "", fixed_type or "")
            ctk.CTkLabel(main, text=f"Tipo: {tipo_txt}  (fijo)", text_color="#999999",
                         font=("Segoe UI", 13), anchor="w").pack(anchor="w", fill=tk.X)

        # --- destino ---
        if show_target:
            destino_lbl = ("Destino (URL o carpeta):" if mode == "custom"
                           else "Destino (URL/carpeta a la que salta el botón):")
            ctk.CTkLabel(main, text=destino_lbl, text_color="white",
                         font=("Segoe UI", 14), anchor="w").pack(anchor="w", fill=tk.X)
            tf = ctk.CTkFrame(main, fg_color="transparent")
            tf.pack(fill=tk.X, pady=4)
            self.target_var = tk.StringVar(value=self.existing.get("target", ""))
            ctk.CTkEntry(tf, textvariable=self.target_var, fg_color="#2a2a2a",
                         border_color="#3a3a3a", text_color="white",
                         font=("Segoe UI", 14)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
            ctk.CTkButton(tf, text="📁", width=46, corner_radius=8, fg_color="#2a2a2a",
                          hover_color="#3a3a3a", text_color="white",
                          font=("Segoe UI", 14),
                          command=self.browse_target).pack(side=tk.LEFT)
            if mode == "base":
                ctk.CTkLabel(main, text=("Vaciar el destino vuelve al original "
                                         "(y ↺ Restablecer también lo restaura)."),
                             text_color="#999999", font=("Segoe UI", 12),
                             anchor="w").pack(anchor="w", fill=tk.X)

        # --- icono (siempre) ---
        ctk.CTkLabel(main, text="Icono (48x48 ideal, ocupa el botón completo):", text_color="white",
                     font=("Segoe UI", 14), anchor="w").pack(anchor="w", fill=tk.X, pady=(14, 0))
        icon_frame = ctk.CTkFrame(main, fg_color="transparent")
        icon_frame.pack(fill=tk.X, pady=6)
        self.icon_var = tk.StringVar(value=self.existing.get("icon_path", ""))
        ctk.CTkEntry(icon_frame, textvariable=self.icon_var, fg_color="#2a2a2a",
                     border_color="#3a3a3a", text_color="white",
                     font=("Segoe UI", 13)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        ctk.CTkButton(icon_frame, text="🖼️", width=46, corner_radius=8, fg_color="#2a2a2a",
                      hover_color="#3a3a3a", text_color="white",
                      font=("Segoe UI", 14),
                      command=self.browse_icon).pack(side=tk.LEFT)

        self.preview_lbl = ctk.CTkLabel(main, text="Preview: sin icono", text_color="#888888",
                                        font=("Segoe UI", 12), anchor="w")
        self.preview_lbl.pack(anchor="w", fill=tk.X, pady=8)
        self.icon_var.trace_add("write", lambda *_: self.update_preview())
        self.update_preview()

        if mode == "custom":
            self.chrome_var = tk.BooleanVar(value=self.existing.get("prefer_chrome", True))
            ctk.CTkCheckBox(main, text="Abrir en Chrome si es web", variable=self.chrome_var,
                            fg_color=ACCENT, hover_color=ACCENT_HOVER,
                            border_color="#3a3a3a", checkmark_color=ACCENT_TEXT,
                            text_color="white", font=("Segoe UI", 14)).pack(anchor="w", pady=10)

        bf = ctk.CTkFrame(main, fg_color="transparent")
        bf.pack(fill=tk.X, pady=14)
        ctk.CTkButton(bf, text="Cancelar", width=150, height=44, corner_radius=8,
                      fg_color="#333333", hover_color="#3a3a3a", text_color="white",
                      font=("Segoe UI", 14), command=self.destroy).pack(side=tk.RIGHT, padx=5)
        ctk.CTkButton(bf, text="Guardar", width=150, height=44, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=ACCENT_TEXT,
                      font=("Segoe UI", 14, "bold"), command=self.save).pack(side=tk.RIGHT)

        # v15: ventana más grande y a prueba de factor de escala (el tamaño
        # lógico se achica si el factor de ESTA ventana lo va a agrandar
        # más allá de la pantalla)
        try:
            self.update_idletasks()
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            f = _effective_scaling(self)
            w = min(max(self.winfo_reqwidth() + 40, 640), max(500, int((sw - 40) / f)))
            h = min(max(self.winfo_reqheight() + 40, 780), max(420, int((sh - 40) / f)))
            self.geometry(f"{w}x{h}+{max(10,(sw-w)//2)}+{max(10,(sh-h)//2)}")
        except Exception:
            self.geometry("640x780")

        force_dark_appearance(self)
        self.after(60, self.deiconify)
        safe_grab(self)
        self.wait_window()

    def browse_target(self):
        if self.type_var.get() == "folder":
            f = filedialog.askdirectory()
            if f: self.target_var.set(f)

    def browse_icon(self):
        f = filedialog.askopenfilename(filetypes=[("Imágenes","*.png *.jpg *.jpeg *.ico *.webp"),("Todos","*.*")])
        if f: self.icon_var.set(f)

    def update_preview(self):
        p = self.icon_var.get()
        if p and os.path.exists(p):
            # v26: si el icono ya vive en la carpeta interna del programa,
            # el nombre de archivo (ico_xxx.png) no dice nada útil
            try:
                if os.path.dirname(os.path.abspath(p)) == \
                        os.path.abspath(str(ICON_STORE_DIR)):
                    self.preview_lbl.configure(text="✓ guardado en el programa")
                    return
            except Exception:
                pass
            self.preview_lbl.configure(text=f"✓ {Path(p).name}")
        elif p: self.preview_lbl.configure(text="✗ no encontrado")
        else: self.preview_lbl.configure(text="(usará iniciales)")

    def save(self):
        if self.mode == "icon":
            # v21: solo icono (Chat / Configuración del pie)
            # v26: el icono se guarda como COPIA interna (iconos_guardados)
            self.result = {"icon_path": internalizar_icono(
                self.icon_var.get().strip())}
            self.destroy()
            return
        if not self.label_var.get().strip():
            messagebox.showwarning("Falta", "Ponle un nombre al botón")
            return
        target = (self.target_var.get().strip()
                  if hasattr(self, "target_var") else "")
        if self.mode == "custom" and not target:
            messagebox.showwarning("Falta", "Nombre y destino obligatorios")
            return
        # mode="base": destino vacío está permitido (= volver al original)
        base = {"label": self.label_var.get().strip(),
                "target": target,
                # v26: el icono se guarda como COPIA interna
                "icon_path": internalizar_icono(
                    self.icon_var.get().strip())}
        if self.mode == "custom":
            self.result = {
                "id": self.existing.get("id", f"custom_{uuid.uuid4().hex[:8]}"),
                "label": base["label"],
                "type": self.type_var.get(),
                "target": base["target"],
                "icon_path": base["icon_path"],
                "prefer_chrome": bool(self.chrome_var.get())
            }
        else:   # mode == "base": el llamador decide dónde guardar cada campo
            self.result = base
        self.destroy()


# ---------- CONFIGURACIÓN ----------
class UIOHubConfig(ctk.CTkToplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.withdraw()
        self.parent = parent
        self.on_save = on_save_callback
        self.title(f"{APP_TITLE} - Configuración")  # v15: más grande, todo visible
        self.configure(fg_color=BG_POPUP)
        self.attributes("-topmost", True)
        self.transient(parent)
        self._icon_ref = None
        self._apply_window_icon()
        self.create_widgets()
        # v15: ventana MÁS GRANDE para que al abrir se vean todas las
        # secciones de una sola vez (el usuario no debería tener que hacer
        # scroll en una pantalla 4K). El tamaño lógico se ajusta por el
        # factor efectivo de la ventana para no pasarse de la pantalla.
        try:
            self.update_idletasks()
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            f = _effective_scaling(self)
            w = min(max(self.winfo_reqwidth() + 40, 1150), max(600, int((sw - 60) / f)))
            h = min(max(self.winfo_reqheight() + 60, 1150), max(500, int((sh - 60) / f)))
            self.geometry(f"{w}x{h}+{max(10,(sw-w)//2)}+{max(10,(sh-h)//2)}")
            self.minsize(880, 660)
        except Exception:
            self.geometry("1150x1150")
        force_dark_appearance(self)
        self.after(60, self.deiconify)
        safe_grab(self)

    def _apply_window_icon(self):
        try:
            ico = APP_DIR / "favicon.ico"
            if not ico.exists(): ico = Path("favicon.ico")
            if ico.exists():
                self.iconbitmap(default=str(ico)); return
        except Exception as e: print(f"iconbitmap error: {e}")
        try:
            if HAS_PIL:
                logo = APP_DIR / "logo_config.png"
                if not logo.exists(): logo = APP_DIR / "omni_icon.png"
                if logo.exists():
                    img = Image.open(logo).convert("RGBA")
                    img.thumbnail((64, 64), Image.LANCZOS)
                    self._icon_ref = ImageTk.PhotoImage(img)
                    self.iconphoto(True, self._icon_ref); return
        except Exception as e: print(f"iconphoto error: {e}")

    def create_widgets(self):
        # --- v14: fila superior con A− / A+ para escalar TODA la interfaz ---
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill=tk.X, padx=16, pady=(14, 0))
        ctk.CTkLabel(top, text="Tamaño de la interfaz:", text_color="white",
                     font=("Segoe UI", 15, "bold")).pack(side=tk.LEFT)
        self.scale_lbl = ctk.CTkLabel(top, text=self._scale_text(), text_color="#4ade80",
                                      width=72, font=("Segoe UI", 15, "bold"))
        self.scale_lbl.pack(side=tk.RIGHT, padx=(0, 6))
        ctk.CTkButton(top, text="A−", width=56, height=40, corner_radius=8,
                      fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="white",
                      font=("Segoe UI", 15, "bold"),
                      command=lambda: self.bump_scale(-0.1)).pack(side=tk.RIGHT, padx=4)
        ctk.CTkButton(top, text="A+", width=56, height=40, corner_radius=8,
                      fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="white",
                      font=("Segoe UI", 15, "bold"),
                      command=lambda: self.bump_scale(0.1)).pack(side=tk.RIGHT)

        notebook = ctk.CTkTabview(self, fg_color=BG_POPUP,
                                  segmented_button_fg_color=BG_POPUP,
                                  segmented_button_selected_color="#3a3a3a",
                                  segmented_button_selected_hover_color="#4a4a4a",
                                  segmented_button_unselected_color="#2a2a2a",
                                  segmented_button_unselected_hover_color="#333333",
                                  text_color="#bbbbbb", corner_radius=8)
        try:
            notebook._segmented_button.configure(font=("Segoe UI", 15))
        except Exception: pass
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tab1 = notebook.add("  General  ")
        tab_btns = notebook.add("  Botones  ")
        for t in (tab1, tab_btns):
            t.configure(fg_color=BG_POPUP)

        sf = ctk.CTkScrollableFrame(tab1, fg_color=BG_POPUP, corner_radius=0)
        sf.pack(fill=tk.BOTH, expand=True)

        ctk.CTkLabel(sf, text="🚀 Inicio con Windows:", text_color="white",
                     font=("Segoe UI", 16, "bold"), anchor="w").pack(anchor="w", padx=16, pady=(20, 8))
        self.autostart_var = tk.BooleanVar(value=is_autostart_enabled() or CONFIG.get("autostart_enabled", False))
        ctk.CTkCheckBox(sf, text=f"Iniciar {APP_TITLE} al prender la PC", variable=self.autostart_var,
                        fg_color=ACCENT, hover_color=ACCENT_HOVER, border_color="#3a3a3a",
                        checkmark_color=ACCENT_TEXT, text_color="#dddddd",
                        font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=16, pady=4)
        # v29: las casillas "Auto-iniciar OmniRoute" (v28) y "Auto-iniciar
        # DSH Web" ya no existen — NINGÚN servicio arranca solo: los dos
        # se levantan ÚNICAMENTE al apretar su botón (clic → PowerShell).

        ctk.CTkLabel(sf, text="Carpeta proyectos:", text_color="white",
                     font=("Segoe UI", 15, "bold"), anchor="w").pack(anchor="w", padx=16, pady=(22, 6))
        row = ctk.CTkFrame(sf, fg_color="transparent")
        row.pack(fill=tk.X, padx=16, pady=4)
        self.projects_var = tk.StringVar(value=CONFIG.get("projects_path", ""))
        ctk.CTkEntry(row, textvariable=self.projects_var, fg_color="#2a2a2a",
                     border_color="#3a3a3a", text_color="white",
                     font=("Segoe UI", 14)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ctk.CTkButton(row, text="📁", width=46, corner_radius=8, fg_color="#3a3a3a",
                      hover_color="#4a4a4a", text_color="white", font=("Segoe UI", 15),
                      command=lambda: self.browse_folder(self.projects_var)).pack(side=tk.LEFT)

        # v30: la seccion de DeepSeek Harness (puerto, API, sesion, Chrome
        # dedicado, captura de pestaña) fue retirada junto con sus botones.

        ctk.CTkLabel(sf, text="🌐 Ruta de chrome.exe (opcional, si no lo detecta):",
                     text_color="#bbbbbb", font=("Segoe UI", 13),
                     anchor="w").pack(anchor="w", padx=16)
        ch_row = ctk.CTkFrame(sf, fg_color="transparent")
        ch_row.pack(fill=tk.X, padx=16, pady=4)
        self.chrome_path_var = tk.StringVar(value=CONFIG.get("chrome_path", ""))
        ctk.CTkEntry(ch_row, textvariable=self.chrome_path_var, fg_color="#2a2a2a",
                     border_color="#3a3a3a", text_color="white",
                     font=("Segoe UI", 14)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        ctk.CTkButton(ch_row, text="📄", width=46, corner_radius=8, fg_color="#3a3a3a",
                      hover_color="#4a4a4a", text_color="white", font=("Segoe UI", 15),
                      command=self.browse_chrome).pack(side=tk.LEFT)

        ctk.CTkLabel(sf, text="Transparencia:", text_color="white",
                     font=("Segoe UI", 15, "bold"), anchor="w").pack(anchor="w", padx=16, pady=(20, 6))
        opf = ctk.CTkFrame(sf, fg_color="transparent")
        opf.pack(fill=tk.X, padx=16, pady=8)
        ctk.CTkLabel(opf, text="Inactiva:", text_color="#bbbbbb",
                     font=("Segoe UI", 14)).grid(row=0, column=0, sticky="w", pady=5)
        self.op_idle_var = tk.DoubleVar(value=CONFIG.get("opacity_idle", 0.80))
        ctk.CTkSlider(opf, from_=0.2, to=1.0, number_of_steps=16,
                      variable=self.op_idle_var, width=320,
                      button_color=ACCENT, button_hover_color=ACCENT_HOVER,
                      progress_color=ACCENT, fg_color="#2a2a2a").grid(row=0, column=1, padx=12)
        ctk.CTkLabel(opf, text="Activa:", text_color="#bbbbbb",
                     font=("Segoe UI", 14)).grid(row=1, column=0, sticky="w", pady=5)
        self.op_hover_var = tk.DoubleVar(value=CONFIG.get("opacity_hover", 1.0))
        ctk.CTkSlider(opf, from_=0.5, to=1.0, number_of_steps=10,
                      variable=self.op_hover_var, width=320,
                      button_color=ACCENT, button_hover_color=ACCENT_HOVER,
                      progress_color=ACCENT, fg_color="#2a2a2a").grid(row=1, column=1, padx=12)

        # ============ v21: PESTAÑA ÚNICA "BOTONES" ============
        # Unifica lo que antes vivía en DOS pestañas ("Iconos": solo el PNG
        # de los botones fijos; "Custom": solo el listado de personalizados).
        # Ahora TODOS los botones del dock se listan y editan juntos.
        ctk.CTkLabel(tab_btns, text=(
            "Todos los botones del dock en un solo lugar, uno por tarjeta. "
            "Clic sobre una tarjeta para seleccionarla; doble clic (o ✏️ Editar) "
            "para cambiar nombre, destino (la URL o carpeta a la que salta) e icono. "
            "Los del sistema no se pueden eliminar, pero sí se los puede renombrar, "
            "redirigir y cambiarles el icono (↺ Restablecer vuelve al original). "
            "Los cambios se aplican al pulsar Guardar."),
            text_color="#bbbbbb", wraplength=980,
            font=("Segoe UI", 14), justify="left",
            anchor="w").pack(anchor="w", padx=16, pady=14)

        # la fila de acciones se RESERVA PRIMERO (side=BOTTOM, fix v20) para
        # que el listado (expand=True) nunca se la coma.
        bf = ctk.CTkFrame(tab_btns, fg_color="transparent")
        bf.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=(4, 14))
        ctk.CTkButton(bf, text="➕ Agregar botón nuevo", width=220, height=44,
                      corner_radius=8, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      text_color=ACCENT_TEXT,
                      font=("Segoe UI", 13, "bold"),
                      command=self.add_custom).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(bf, text="✏️ Editar", width=130, height=44, corner_radius=8,
                      fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="white",
                      font=("Segoe UI", 13), command=self.edit_selected).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(bf, text="🗑️ Eliminar", width=140, height=44, corner_radius=8,
                      fg_color="#b3373c", hover_color="#d1484e", text_color="white",
                      font=("Segoe UI", 13), command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(bf, text="↺ Restablecer", width=150, height=44, corner_radius=8,
                      fg_color="#3a3a3a", hover_color="#4a4a4a", text_color="#bbbbbb",
                      font=("Segoe UI", 13), command=self.reset_selected).pack(side=tk.LEFT, padx=5)

        # ============ v22b: TARJETAS en lugar de lista de texto ============
        # Cada botón es una TARJETA prolija (antes: puro texto en un
        # Listbox) con el icono real a la izquierda y, apilados, "BOTÓN N",
        # el nombre y el tipo. Espaciado uniforme entre tarjetas.
        self._card_sel = None       # índice seleccionado (posición en _list_map)
        self._card_widgets = []     # [(tarjeta, índice)] para repintar selección
        self._card_imgs = []        # refs a PhotoImage (evita el recolector)
        self.cards_sf = ctk.CTkScrollableFrame(tab_btns, fg_color="#191919",
                                               corner_radius=8)
        self.cards_sf.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        self._list_map = []
        self.refresh_buttons_list()

        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill=tk.X, padx=16, pady=16)
        ctk.CTkButton(bottom, text="Cancelar", width=160, height=46, corner_radius=8,
                      fg_color="#333333", hover_color="#3a3a3a", text_color="white",
                      font=("Segoe UI", 14), command=self.destroy).pack(side=tk.RIGHT, padx=8)
        ctk.CTkButton(bottom, text="Guardar", width=160, height=46, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=ACCENT_TEXT,
                      font=("Segoe UI", 14, "bold"), command=self.save_all).pack(side=tk.RIGHT)

    # ---------- v14: escala de interfaz ----------
    def _scale_text(self):
        try:
            v = float(CONFIG.get("ui_scale", 1.0) or 1.0)
        except Exception:
            v = 1.0
        return f"{int(round(v * 100))}%"

    def bump_scale(self, delta):
        """A− / A+: agranda o achica TODA la interfaz (letras, botones y
        espaciados). Se aplica y guarda al instante, sin tocar Guardar."""
        try:
            cur = float(CONFIG.get("ui_scale", 1.0) or 1.0)
        except Exception:
            cur = 1.0
        new = max(0.8, min(1.8, round(cur + delta, 2)))
        if abs(new - cur) < 0.001:
            return
        CONFIG["ui_scale"] = new
        save_config(CONFIG)
        try:
            self.scale_lbl.configure(text=self._scale_text())
        except Exception:
            pass
        p = self.parent
        try:
            if hasattr(p, "apply_ui_scale"):
                p.apply_ui_scale()
        except Exception as e:
            print(f"apply_ui_scale: {e}")
        # la ventana se recrea para que TODO se redibuje al nuevo tamaño
        self.after(80, lambda: self._recreate(p))

    def _recreate(self, p):
        try: self.destroy()
        except Exception: pass
        try: p.open_config()
        except Exception: pass

    def browse_folder(self, var):
        f = filedialog.askdirectory(initialdir=var.get())
        if f: var.set(f)

    def browse_chrome(self):
        f = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe"), ("Todos", "*.*")])
        if f: self.chrome_path_var.set(f)

    # ---------- v21: lista ÚNICA de botones (sistema + custom + pie) ----------
    def _base_effective(self, bid):
        """(label, target, tipo, target_key) EFECTIVO de un botón del sistema,
        aplicando los overrides guardados en base_labels / base_targets."""
        d = next(x for x in BASE_BUTTONS_DEF if x["id"] == bid)
        label = (CONFIG.get("base_labels", {}) or {}).get(bid) or d["label"]
        ov_t = (CONFIG.get("base_targets", {}) or {}).get(bid, "")
        if ov_t and str(ov_t).strip():
            target = str(ov_t).strip()
        elif d.get("target_key"):
            target = str(CONFIG.get(d["target_key"], ""))
        else:
            target = "(interno)"
        return label, target, d["type"], d.get("target_key")

    # ---------- v22b: tarjetas ----------
    def _card_icon_pil(self, item):
        """PIL del icono REAL del botón para la vista previa de la tarjeta
        (None = sin vista previa). Respeta el PNG personalizado
        (custom_icons, con los alias gdrive/gtasks de load_all_icons), cae
        al PNG de fábrica, y en el pie sin PNG propio dibuja la reserva
        (burbuja / engranaje) para que la tarjeta se vea como el dock."""
        if not HAS_PIL:
            return None
        try:
            if item["kind"] == "custom":
                p = CONFIG["custom_buttons"][item["idx"]].get("icon_path", "")
                return (Image.open(p).convert("RGBA")
                        if p and os.path.exists(p) else None)
            bid = item["id"]
            ci = CONFIG.get("custom_icons", {}) or {}
            for ak in ICON_LOOKUP_ALIAS.get(bid, (bid,)):
                p = ci.get(ak)
                if p and os.path.exists(p):
                    return Image.open(p).convert("RGBA")
            if item["kind"] == "special":
                return draw_gear_glyph(72)
            fn = BUILTIN_ICON_FILES.get(bid)
            if fn:
                for base in (resource_path(fn), str(APP_DIR / fn), fn):
                    if os.path.exists(base):
                        return Image.open(base).convert("RGBA")
                # v25: sin archivo en disco → PNG embebido en el programa
                return _embedded_icon_img(fn)
        except Exception:
            return None
        return None

    def _select_card(self, idx):
        """Marca la tarjeta idx como seleccionada (aro UIO Blue)."""
        self._card_sel = idx
        for f, i in self._card_widgets:
            try:
                sel = (i == idx)
                f.configure(border_color=UIO_BLUE if sel else "#333333",
                            border_width=2 if sel else 1)
            except Exception:
                pass

    def _bind_card(self, w, idx):
        """Clic sobre la tarjeta (o cualquiera de sus widgets) = seleccionar;
        doble clic = editar. Las tarjetas no hacen nada más: editar/eliminar
        siguen en la fila de botones de abajo."""
        try: w.configure(cursor="hand2")
        except Exception: pass
        w.bind("<Button-1>", lambda _e: self._select_card(idx), add="+")
        w.bind("<Double-Button-1>", lambda _e: self.edit_selected(), add="+")
        for c in w.winfo_children():
            self._bind_card(c, idx)

    def _make_card(self, parent, idx, name, tipo_txt, kind_tag, item):
        """Una tarjeta = icono real a la izquierda + apilado 'BOTÓN N',
        nombre y 'Tipo: ...'. Espaciado uniforme (pady=5)."""
        card = ctk.CTkFrame(parent, fg_color="#212121", corner_radius=10,
                            border_width=1, border_color="#333333")
        card.pack(fill=tk.X, padx=10, pady=5)
        inner = ctk.CTkFrame(card, fg_color="transparent", corner_radius=0)
        inner.pack(fill=tk.X, padx=12, pady=8)
        pil = self._card_icon_pil(item)
        if pil is not None:
            try:
                ph = ImageTk.PhotoImage(rounded_tile(pil, 38, 9))
                self._card_imgs.append(ph)
                # tk.Label plano (los CTkLabel con imagen colapsan en CTk 6.x,
                # misma razón por la que v19 horneó la cara del botón enviar)
                ic = tk.Label(inner, image=ph, bg="#212121", bd=0,
                              highlightthickness=0)
                ic.pack(side=tk.LEFT, padx=(0, 12))
            except Exception:
                pass
        col = ctk.CTkFrame(inner, fg_color="transparent", corner_radius=0)
        col.pack(side=tk.LEFT, fill=tk.X, expand=True)
        head = ctk.CTkFrame(col, fg_color="transparent", corner_radius=0)
        head.pack(fill=tk.X)
        ctk.CTkLabel(head, text=f"BOTÓN {idx + 1}", text_color="#8f8f8f",
                     font=("Segoe UI", 11, "bold"), anchor="w").pack(side=tk.LEFT)
        tag_color = {"sistema": "#8f8f8f", "personalizado": "#4ade80",
                     "pie": "#a1b2c3"}.get(kind_tag, "#8f8f8f")
        ctk.CTkLabel(head, text=kind_tag, text_color=tag_color,
                     font=("Segoe UI", 11), anchor="e").pack(side=tk.RIGHT)
        ctk.CTkLabel(col, text=name or "(sin nombre)", text_color="#ececec",
                     font=("Segoe UI", 15), anchor="w"
                     ).pack(fill=tk.X, pady=(1, 0))
        ctk.CTkLabel(col, text=f"Tipo: {tipo_txt}", text_color="#9a9a9a",
                     font=("Segoe UI", 12), anchor="w").pack(fill=tk.X)
        self._card_widgets.append((card, idx))
        self._bind_card(card, idx)

    def refresh_buttons_list(self):
        """v22b: reconstruye las TARJETAS (antes: filas de texto de un
        Listbox). Orden = el del dock: sistema → personalizados → pie."""
        try:
            for w in self.cards_sf.winfo_children():
                w.destroy()
        except Exception:
            pass
        self._card_widgets.clear()
        self._card_imgs.clear()
        self._list_map = []
        rows = []   # (nombre, tipo_display, etiqueta_kinda, item)
        # 1) sistema (en el orden del dock)
        for d in BASE_BUTTONS_DEF:
            bid = d["id"]
            label, _target, btype, _tk = self._base_effective(bid)
            rows.append((label, TIPO_CARD.get(btype, btype), "sistema",
                         {"kind": "base", "id": bid}))
            self._list_map.append({"kind": "base", "id": bid})
        # 2) personalizados
        for i, btn in enumerate(CONFIG.get("custom_buttons", [])):
            bt = btn.get("type", "") or ""
            rows.append((btn.get("label", ""), TIPO_CARD.get(bt, bt),
                         "personalizado", {"kind": "custom", "idx": i}))
            self._list_map.append({"kind": "custom", "idx": i})
        # 3) pie del dock (solo icono; el nombre sin el apéndice largo)
        for bid, blabel in FOOTER_SPECIALS:
            rows.append((blabel.replace(" (pie del dock)", ""), "pie", "pie",
                         {"kind": "special", "id": bid}))
            self._list_map.append({"kind": "special", "id": bid})
        # la selección puede haber quedado fuera de rango tras eliminar
        if self._card_sel is not None and self._card_sel >= len(rows):
            self._card_sel = None
        for n, (name, tipo_txt, kind_tag, item) in enumerate(rows):
            self._make_card(self.cards_sf, n, name, tipo_txt, kind_tag, item)
        if self._card_sel is not None:
            self._select_card(self._card_sel)

    def add_custom(self):
        dlg = UIOHubButtonDialog(self)
        if dlg.result:
            CONFIG.setdefault("custom_buttons", []).append(dlg.result)
            self.refresh_buttons_list()

    def edit_selected(self):
        sel = self._card_sel
        if sel is None or sel >= len(self._list_map):
            messagebox.showinfo("Selecciona", "Selecciona un botón de la lista "
                                             "(clic sobre su tarjeta)")
            return
        item = self._list_map[sel]
        # --- personalizado: flujo de siempre ---
        if item["kind"] == "custom":
            idx = item["idx"]
            dlg = UIOHubButtonDialog(self, CONFIG["custom_buttons"][idx])
            if dlg.result:
                CONFIG["custom_buttons"][idx] = dlg.result
                self.refresh_buttons_list()
            return
        # --- del pie: solo icono ---
        if item["kind"] == "special":
            bid = item["id"]
            existing = {"icon_path": (CONFIG.get("custom_icons", {}) or {}).get(bid, "")}
            dlg = UIOHubButtonDialog(self, existing, mode="icon",
                                     title=f"{APP_TITLE} - Icono del botón (pie)")
            if dlg.result:
                icn = (dlg.result.get("icon_path") or "").strip()
                CONFIG.setdefault("custom_icons", {})
                if icn: CONFIG["custom_icons"][bid] = icn
                else: CONFIG["custom_icons"].pop(bid, None)
                self.refresh_buttons_list()
            return
        # --- del sistema: nombre + destino (si aplica) + icono ---
        bid = item["id"]
        d = next(x for x in BASE_BUTTONS_DEF if x["id"] == bid)
        label, target, _tp, _tk = self._base_effective(bid)
        existing = {
            "label": label,
            "target": target if d.get("target_key") else "",
            "icon_path": (CONFIG.get("custom_icons", {}) or {}).get(bid, ""),
        }
        dlg = UIOHubButtonDialog(self, existing, mode="base",
                                 fixed_type=d["type"],
                                 editable_target=bid in BASE_EDITABLE_TARGET,
                                 title=f"{APP_TITLE} - Editar '{label}'")
        if not dlg.result:
            return
        r = dlg.result
        lbl = (r.get("label") or "").strip()
        tgt = (r.get("target") or "").strip()
        icn = (r.get("icon_path") or "").strip()
        CONFIG.setdefault("base_labels", {})
        # el nombre solo se guarda si difiere del original
        if lbl and lbl != d["label"]:
            CONFIG["base_labels"][bid] = lbl
        else:
            CONFIG["base_labels"].pop(bid, None)
        CONFIG.setdefault("base_targets", {})
        # el destino solo se guarda si difiere del de fábrica
        if tgt and d.get("target_key") and tgt != str(CONFIG.get(d["target_key"], "")):
            CONFIG["base_targets"][bid] = tgt
        else:
            CONFIG["base_targets"].pop(bid, None)
        CONFIG.setdefault("custom_icons", {})
        if icn: CONFIG["custom_icons"][bid] = icn
        else: CONFIG["custom_icons"].pop(bid, None)
        self.refresh_buttons_list()

    def delete_selected(self):
        sel = self._card_sel
        if sel is None or sel >= len(self._list_map):
            messagebox.showinfo("Selecciona", "Selecciona un botón de la lista "
                                             "(clic sobre su tarjeta)")
            return
        item = self._list_map[sel]
        if item["kind"] != "custom":
            messagebox.showinfo(
                "Botón del sistema",
                "Los botones del sistema (Proyectos, Drive, Notion, Tasks "
                "y Configuración) no se pueden eliminar:\n"
                "son parte del dock.\n\n"
                "Igualmente podés editarles el nombre, el destino y el icono, "
                "o usar '↺ Restablecer' para volver al original.")
            return
        idx = item["idx"]
        if messagebox.askyesno("Eliminar", f"¿Eliminar {CONFIG['custom_buttons'][idx]['label']}?"):
            del CONFIG["custom_buttons"][idx]
            self.refresh_buttons_list()

    def reset_selected(self):
        sel = self._card_sel
        if sel is None or sel >= len(self._list_map):
            messagebox.showinfo("Selecciona", "Selecciona un botón de la lista "
                                             "(clic sobre su tarjeta)")
            return
        item = self._list_map[sel]
        if item["kind"] == "custom":
            messagebox.showinfo("Restablecer",
                                "Los botones personalizados se restauran "
                                "editándolos o eliminándolos.")
            return
        bid = item["id"]
        changed = False
        for key in ("base_labels", "base_targets"):
            dd = CONFIG.get(key) or {}
            if bid in dd:
                dd.pop(bid, None)
                changed = True
        ci = CONFIG.get("custom_icons") or {}
        if bid in ci:
            ci.pop(bid, None)
            changed = True
        if changed:
            self.refresh_buttons_list()
        else:
            messagebox.showinfo("Restablecer",
                                "Ese botón ya está con sus valores originales.")

    def save_all(self):
        CONFIG["projects_path"] = self.projects_var.get()
        # v30: sin DSH ni Chrome dedicado — no hay puertos ni sesiones
        # que guardar (esas claves salieron de la configuración).
        CONFIG["chrome_path"] = self.chrome_path_var.get().strip()
        CONFIG["opacity_idle"] = round(float(self.op_idle_var.get()), 2)
        CONFIG["opacity_hover"] = round(float(self.op_hover_var.get()), 2)
        CONFIG["autostart_enabled"] = bool(self.autostart_var.get())
        # v29: autostart_omni (v28) y autostart_dsh eliminados — los dos
        # servicios SOLO se levantan con su botón.
        # v21: los iconos (custom_icons) y los overrides de los botones del
        # sistema (base_labels/base_targets) los escribe DIRECTAMENTE cada
        # diálogo de la pestaña "Botones" — aquí solo se persiste todo.
        set_autostart_windows(CONFIG["autostart_enabled"])
        save_config(CONFIG)
        self.on_save()
        self.destroy()



# v30: la barra de chat lateral (UIOHubSidePanel) fue retirada junto
# con el botoncito de Chat del pie: el usuario ya no la usa.

# ---------- BOTONERA PRINCIPAL ----------
class UIOHubBar(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=TRANSPARENT)
        self.config_data = load_config()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", self.config_data["opacity_idle"])
        self.wm_attributes("-transparentcolor", TRANSPARENT)
        self.title(APP_TITLE)
        self.geometry(f"+{self.config_data['window_x']}+{self.config_data['window_y']}")
        self._apply_dpi_compensation()

        self._drag_px = None
        self._drag_py = None
        self._drag_wx = 0
        self._drag_wy = 0
        self._drag_active = False
        # v30: sin OmniRoute/DSH/Chat → sin estado de servicios, sin barra
        # lateral, sin parpadeos de captura ni pulsos de inicio.
        self.icons = {}            # PhotoImage por clave de icono (tamaño = botón)
        self.pil_icons = {}        # PIL originales (para regenerar al escalar)
        self.icon_labels = {}      # v14: etiquetas superpuestas del icono
        self._tooltips = []        # v17: tooltips activos (guiño guía §21)
        self._round_after = None
        self._tray = None            # v27b: icono de bandeja
        self._tray_ok = False
        self._tray_job = None
        self._tray_hidden_once = False
        self._user_hid = False       # v29b: el usuario ocultó el dock a mano

        if HAS_PIL:
            self.load_all_icons()

        # Contenedor principal: CTk dibuja el rectángulo con esquinas
        # redondeadas; el fondo exterior en TRANSPARENT se vuelve invisible
        # (transparentcolor) y la región raíz recorta la ventana de verdad.
        self.main_container = ctk.CTkFrame(self, fg_color=BG_MAIN,
                                           corner_radius=CORNER_R,
                                           border_width=1, border_color=BORDER,
                                           bg_color=TRANSPARENT)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        header = ctk.CTkFrame(self.main_container, fg_color="transparent", height=20)
        header.pack(fill=tk.X, padx=8, pady=(5, 0))   # v31a: 10→8 y 6→5

        drag_dot = ctk.CTkLabel(header, text="•••", text_color="#5c6570",
                                font=("Segoe UI", 9))
        drag_dot.pack(side=tk.LEFT)
        # v19: marcador de versión — pasar el mouse por "•••" dice qué
        # versión ESTÁ corriendo realmente (la captura del usuario mostró
        # v17 pese a existir la v18: el auto-arranque guardó la ruta vieja)
        self._tooltips.append(Tooltip(
            drag_dot, lambda: f"UIO Hub v31\nArrastrar para mover el dock",
            delay=350))

        close = ctk.CTkLabel(header, text="✕", text_color="#7a828a",
                             font=("Segoe UI", 12, "bold"))
        close.pack(side=tk.RIGHT, padx=(0, 4))
        close.bind("<Button-1>", lambda e: self.on_close())
        close.bind("<Enter>", lambda e: close.configure(text_color="#ff5555"))
        close.bind("<Leave>", lambda e: close.configure(text_color="#7a828a"))
        # v27b: el ✕ ya no apaga: oculta a la bandeja (el menú del icono
        # de la bandeja tiene el "Salir" real)
        self._tooltips.append(Tooltip(
            close, lambda: "Ocultar (queda en la bandeja)\n"
                           "Salir de verdad: clic derecho en el icono de la bandeja"))

        self.grid_frame = ctk.CTkFrame(self.main_container, fg_color="transparent",
                                       corner_radius=0)
        self.grid_frame.pack(padx=2, pady=(4, 2))   # v31b: menos aire abajo

        self.btn_widgets = {}
        self.indicators = {}
        self.build_grid()

        # v23a: separador NUEVO entre los botones de arriba y el pie
        # (Configuración): misma altura sutil de 1px y el MISMO color
        # de paleta (#343434, el aro de los iconos) que el separador de
        # arriba. v24a: con PEQUEÑA SEPARACIÓN de los botones (el aire
        # alrededor escala con ui_scale) y el ancho SINCRONIZADO con la
        # línea de arriba (ver _sync_sep_widths).
        _sc = max(1, round(1 * getattr(self, "ui_scale", 1.0)))
        _sp = max(0, round(3 * getattr(self, "ui_scale", 1.0)))
        _sp2 = max(0, round(4 * getattr(self, "ui_scale", 1.0)))   # v31b: 5→4
        self.foot_sep = tk.Frame(self.main_container, bg=SEP_COLOR, height=_sc,
                                 bd=0, highlightthickness=0)
        self.foot_sep.pack(fill=tk.X, padx=5, pady=(_sp, _sp2))   # v31a: 6→5

        # v17 guía §32-33 / v30: pie con UN solo botón — el engranaje de
        # Configuración (el Chat del pie se retiró con su barra lateral).
        footer = ctk.CTkFrame(self.main_container, fg_color="transparent")
        footer.pack(fill=tk.X, pady=(4, 2), padx=4)   # v31b: abajo 4→2; v31a: 6→4
        foot_row = ctk.CTkFrame(footer, fg_color="transparent")
        foot_row.pack()

        self.cfg_btn = ctk.CTkButton(foot_row, text="", width=FOOT_SIZE, height=FOOT_SIZE,
                                     corner_radius=BTN_RADIUS, fg_color=BTN_BG,
                                     hover_color=BTN_HOVER, border_width=0,
                                     command=self.open_config)
        self.cfg_btn.grid_propagate(False)
        self._add_footer_overlay(self.cfg_btn, "settings", "⚙")
        self.cfg_btn.pack(side=tk.LEFT)

        # tooltips del pie (los overlays cubren el botón completo)
        self._tooltips.append(Tooltip(self.icon_labels.get("settings") or self.cfg_btn,
                                      lambda: "Configuración"))

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Configure>", self._on_configure)
        # ARRASTRE desde cualquier parte del dock (todos los widgets);
        # el filtro por toplevel excluye los diálogos.
        self.bind_all("<ButtonPress-1>", self._global_drag_start, add="+")
        self.bind_all("<B1-Motion>", self._global_drag_motion, add="+")

        self.refit_window()
        self.after(120, self.refresh_rounding)
        # v30: sin monitoreo de OmniRoute/DSH (sus botones ya no existen)

        # v27b: BANDEJA DEL SISTEMA — fuera de la barra de tareas + icono
        # en la zona de notificaciones (clic izq: mostrar/ocultar; clic der:
        # menú con Salir). El ✕ del dock también oculta a la bandeja.
        if sys.platform == "win32":
            self.update_idletasks()
            hide_taskbar_button(self)
        if sys.platform == "win32" and self.config_data.get("tray_enabled", True):
            try:
                self._tray = UIOTrayIcon(
                    tooltip="UIO Hub v31 — clic: mostrar/ocultar")
                self._tray_ok = self._tray.start()
                # v27b: el poller SIEMPRE corre si hay objeto de bandeja:
                # cubre el caso "Explorer tardó y el icono se instaló a los
                # 10 segundos" (start() se rindió a los 3s pero el icono
                # existe): los clics se atienden igual.
                self._tray_job = self.after(120, self._poll_tray)
                if self._tray_ok:
                    print("[UIO Hub v31] Bandeja lista: clic izq = "
                          "mostrar/ocultar · clic der = menú (Salir)")
                else:
                    print("[UIO Hub v31] Bandeja todavía no instalada "
                          "(¿Explorer tardando?); reintenta en segundo plano")
            except Exception as e:
                print(f"[UIO Hub v31] Bandeja no disponible: {e}")
                self._tray_ok = False

        # v29b: el dock NACE VISIBLE. Con "Iniciar UIO Hub al prender la
        # PC" a veces la ventana quedaba escondida (Explorer arrancando
        # lento) y el hub solo existía en la bandeja: si el usuario no lo
        # ocultó él mismo, se re-muestra solo a los ~1 s y ~3 s.
        self.after(1000, self._asegurar_visible, 1)

    # ---------- ARRASTRE DESDE CUALQUIER PARTE DEL DOCK ----------
    def _apply_dpi_compensation(self):
        """CustomTkinter multiplica los tamaños por el factor de escala de
        Windows (125% / 150%): por eso la v12 se veía más grande que la
        botonera original. Con la escala invertida, 48px vuelven a medir
        48px REALES. v14: se multiplica además por ui_scale (botones A− / A+
        de la ventana de Configuración)."""
        self.ui_scale = self._read_ui_scale()
        if sys.platform != "win32":
            # fuera de Windows no hay DPI que compensar, pero la escala
            # elegida con A− / A+ sí se aplica igual
            try:
                ctk.set_widget_scaling(self.ui_scale)
                ctk.set_window_scaling(1.0)
            except Exception:
                pass
            return
        try:
            u = ctypes.windll.user32
            dpi = 0
            try:
                dpi = u.GetDpiForWindow(get_root_hwnd(self))
            except Exception:
                pass
            if not dpi:
                try:
                    dpi = ctypes.windll.shcore.GetDpiForSystem()
                except Exception:
                    dpi = 96
            factor = (dpi or 96) / 96.0
            print(f"DPI del monitor: {dpi} (factor {factor:.2f}); "
                  f"escala de interfaz: {self.ui_scale:.2f}")
            inv = 1.0 / factor
            ctk.set_widget_scaling(inv * self.ui_scale)
            ctk.set_window_scaling(inv)
            if abs(factor - 1.0) > 0.001:
                print("✓ Compensación aplicada: tamaño original restaurado")
        except Exception as e:
            print(f"dpi_comp: {e}")

    def _read_ui_scale(self):
        # v14-fix: la fuente de verdad es el CONFIG global (lo actualizan los
        # botones A− / A+ y Guardar); la copia del dock puede quedar vieja.
        try:
            v = float(CONFIG.get("ui_scale", 1.0) or 1.0)
        except Exception:
            try:
                v = float(self.config_data.get("ui_scale", 1.0) or 1.0)
            except Exception:
                v = 1.0
        return max(0.8, min(1.8, v))

    def apply_ui_scale(self):
        """Botones A− / A+ de Configuración: re-escala TODA la interfaz
        (letras, botones y espaciados de CTk responden solos; los iconos se
        regeneran al nuevo tamaño) y reacomoda la ventana."""
        self.ui_scale = self._read_ui_scale()
        self.config_data["ui_scale"] = self.ui_scale
        self._apply_dpi_compensation()
        if HAS_PIL:
            self.load_all_icons()
        self.build_grid()
        # v23a: el separador del pie también sigue la escala elegida
        try:
            _s = getattr(self, "ui_scale", 1.0)
            self.foot_sep.configure(height=max(1, round(1 * _s)))
            # v24a: el aire alrededor de la línea también escala
            self.foot_sep.pack_configure(
                pady=(max(0, round(3 * _s)), max(0, round(5 * _s))))
        except Exception:
            pass
        self._refresh_footer_icons()
        self.refit_window()

    # ---------- ICONOS A BOTÓN COMPLETO (v14) ----------
    def _bind_overlay(self, btn, ov):
        """El icono superpuesto delega clic y hover al botón real."""
        def on_enter(_e=None):
            try:
                if btn.cget("state") != "disabled":
                    ov.configure(bg=btn.cget("hover_color") if btn.cget("hover_color") else BTN_HOVER)
                    btn._on_enter()
            except Exception:
                pass
        def on_leave(_e=None):
            try:
                if btn.cget("state") != "disabled":
                    ov.configure(bg=btn.cget("fg_color") or BTN_BG)
                    btn._on_leave()
            except Exception:
                pass
        ov.bind("<Button-1>", lambda e: btn.invoke())
        ov.bind("<Enter>", on_enter, add="+")
        ov.bind("<Leave>", on_leave, add="+")

    def _make_overlay(self, btn, key, fallback_text, size):
        """Dibuja el icono ocupando el botón COMPLETO sobre una etiqueta
        superpuesta (la imagen interna de CTk recorta los lados)."""
        icon = self.icons.get(key)
        if icon is not None:
            ov = tk.Label(btn, image=icon, bg=BTN_BG, bd=0, highlightthickness=0)
        else:
            ov = tk.Label(btn, text=fallback_text, font=("Segoe UI", 16),
                          bg=BTN_BG, fg="#e0e0e0", bd=0, highlightthickness=0)
        ov.place(relx=0.5, rely=0.5, anchor="center")
        self.icon_labels[key] = ov
        self._bind_overlay(btn, ov)
        return ov

    def _add_footer_overlay(self, btn, key, fallback_text):
        self._make_overlay(btn, key, fallback_text, FOOT_ICON)

    def _make_grid_button(self, parent_cell_holder, key, label=""):
        """Botón CUADRADO de la grilla: propagación desactivada (queda 46x46
        exacto) + icono superpuesto ocupando el botón completo (v17: tile
        redondeado estilo macOS con anillo sutil)."""
        btn = ctk.CTkButton(parent_cell_holder, text="", width=BTN_SIZE,
                            height=BTN_SIZE, corner_radius=BTN_RADIUS,
                            fg_color=BTN_BG, hover_color=BTN_HOVER,
                            border_width=0)
        btn.grid_propagate(False)
        ov = self._make_overlay(btn, key, "", BTN_SIZE)
        self._bind_pressed(btn, ov)
        return btn

    def _bind_pressed(self, btn, ov=None):
        """v17 guía §20: estado PRESIONADO sutil (más oscuro), sin mover el
        layout. Al soltar: hover si el mouse sigue encima, normal si no."""
        def press(_e=None):
            try:
                if btn.cget("state") == "disabled": return
                btn.configure(fg_color=BTN_PRESSED)
                if ov is not None: ov.configure(bg=BTN_PRESSED)
            except Exception: pass
        def release(_e=None):
            try:
                if btn.cget("state") == "disabled": return
                mx, my = btn.winfo_pointerxy()
                bx, by = btn.winfo_rootx(), btn.winfo_rooty()
                inside = (bx <= mx < bx + max(1, btn.winfo_width()) and
                          by <= my < by + max(1, btn.winfo_height()))
                face = BTN_HOVER if inside else BTN_BG
                btn.configure(fg_color=face)
                if ov is not None: ov.configure(bg=face)
            except Exception: pass
        for w in (btn, ov):
            if w is None: continue
            try:
                w.bind("<Button-1>", press, add="+")
                w.bind("<ButtonRelease-1>", release, add="+")
            except Exception: pass

    def _refresh_footer_icons(self):
        """Tras cambiar la escala o los iconos, actualiza el pie sin recrear
        los botones (conserva comandos y referencias)."""
        for key, fallback in (("settings", "⚙"),):
            ov = self.icon_labels.get(key)
            icon = self.icons.get(key)
            if ov is not None and ov.winfo_exists():
                # v30: el pie tiene un solo botón (Configuración): el icono
                # es SIEMPRE el mismo.
                if icon is not None:
                    ov.configure(image=icon, text="")
                else:
                    ov.configure(image="", text=fallback)

    def _global_drag_start(self, e):
        """Clic en CUALQUIER parte del dock (fondo, header, botones...):
        guarda el ancla. El arrastre recién arranca si movés más de 4px,
        así un clic simple sigue funcionando en los botones."""
        try:
            if e.widget.winfo_toplevel() is not self:
                return                # eventos de la barra de chat o diálogos
        except Exception:
            return
        self._drag_active = False
        self._drag_px, self._drag_py = e.x_root, e.y_root
        self._drag_wx, self._drag_wy = self.winfo_x(), self.winfo_y()

    def _global_drag_motion(self, e):
        if self._drag_px is None:
            return
        dx = e.x_root - self._drag_px
        dy = e.y_root - self._drag_py
        if not self._drag_active and abs(dx) < 4 and abs(dy) < 4:
            return
        self._drag_active = True
        x, y = self._drag_wx + dx, self._drag_wy + dy
        self.geometry(f"+{x}+{y}")
        self.config_data["window_x"] = x
        self.config_data["window_y"] = y

    # ---------- botones web: CHROME NORMAL (v30) ----------
    def open_web_async(self, url, prefer_chrome=True):
        """v30: abre la url en la sesión de Google Chrome de SIEMPRE (el
        perfil de todos los días del usuario). Ya no existe el Chrome
        dedicado con perfil aparte ni el ruteo por CDP."""
        if not url:
            return
        url = str(url) if str(url).startswith("http") else "https://" + str(url)
        open_url_smart(url, prefer_chrome)

    def refit_window(self):
        try:
            self.update_idletasks()
            # v14: sin techo de 126px — ese recorte CORTABA los iconos por los
            # lados cuando los botones crecían. Ahora el ancho lo manda el
            # contenido (con la propagación bloqueada vuelve a ser compacto).
            # v31a: piso 64 (antes 110, pensado para DOS columnas: con el hub
            # de UNA columna dejaba ~23px de aire a cada lado de los iconos).
            w = self.winfo_reqwidth()
            if w < 64: w = 64
            h = self.winfo_reqheight()
            if h < 100: h = 100
            x = self.config_data.get("window_x", 100)
            y = self.config_data.get("window_y", 100)
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            if x + w > sw: x = max(0, sw - w)
            if y + h > sh: y = max(0, sh - h)
            self.geometry(f"{w}x{h}+{x}+{y}")
            self.config_data["window_x"] = x
            self.config_data["window_y"] = y
            # v24a: tras reacomodar la ventana, igualar el ancho de las dos
            # líneas separadoras (la del pie copia la de arriba)
            self.after(80, self._sync_sep_widths)
            self.after(60, self.refresh_rounding)
        except Exception as e:
            print(f"refit error: {e}")

    def _sync_sep_widths(self):
        """v24a: las DOS líneas separadoras deben tener EXACTAMENTE el mismo
        ancho ("de punta a punta de los iconos"). Antes la de arriba medía
        grid−8 y la del pie main−12 (padx fijos que, además, no escalan con
        el DPI) → la de abajo se veía más corta. Ahora se mide la extensión
        de la línea de arriba (sep_frame, DENTRO de grid_frame) y a la del
        pie se le copia con pack_configure(padx=(izq, der)). Todo el cálculo
        es RELATIVO AL PADRE (winfo_x/width, sin rootx) → inmune a la
        escala, al DPI, a la posición de la ventana y a los re-flow."""
        try:
            sep = getattr(self, "sep_frame", None)
            foot = getattr(self, "foot_sep", None)
            grid = getattr(self, "grid_frame", None)
            if sep is None or foot is None or grid is None:
                return
            if not (sep.winfo_exists() and foot.winfo_exists()
                    and grid.winfo_exists()):
                return
            self.update_idletasks()
            main = self.main_container
            if main.winfo_width() < 2 or grid.winfo_width() < 2:
                return          # layout todavía sin asentar
            # la línea de arriba vive en grid_frame con padx propio
            # (sticky="ew" → su extensión es grid − 2·padx); la del pie
            # vive en main_container → se copia esa MISMA extensión
            left = grid.winfo_x() + sep.winfo_x()
            right = (main.winfo_width() - grid.winfo_x()
                     - grid.winfo_width() + sep.winfo_x())
            if left >= 0 and right >= 0:
                foot.pack_configure(padx=(left, right))
        except Exception:
            pass

    def _on_configure(self, e=None):
        if e is not None and e.widget is not self: return
        if self._round_after:
            try: self.after_cancel(self._round_after)
            except: pass
        self._round_after = self.after(80, self.refresh_rounding)

    def refresh_rounding(self):
        self._round_after = None
        try: self.update_idletasks()
        except Exception: pass
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 * CORNER_R + 10 or h < 2 * CORNER_R + 10: return
        # FIX esquinas: la región se aplica sobre el HWND RAÍZ (antes se
        # aplicaba sobre winfo_id(), que puede ser un HWND hijo → artefactos).
        apply_window_region(self, w, h, CORNER_R)
        # v24a: tras CADA re-flow asentado (arranque, refit, escala, drag)
        # se re-igualan los anchos de las dos líneas separadoras
        self._sync_sep_widths()

    def load_all_icons(self):
        """v14: cada icono se genera CON EL TAMAÑO DE SU BOTÓN (48 para la
        grilla, 44 para el pie) con fit_icon_image → nunca se recorta un lado.
        Son PhotoImage planos: se superponen sobre el botón (ver _make_overlay).
        v16 FIX: el diálogo de Configuración guarda los PNG con el id del
        botón ("drive", "tasks") pero acá se buscaban con las claves internas
        antiguas ("gdrive", "gtasks") → los íconos de Drive y Tasks (columna
        derecha, debajo de D) nunca se aplicaban. Ahora se aceptan AMBAS
        claves para cada botón."""
        custom_icons_map = self.config_data.get("custom_icons", {})
        # v16: limpiar el caché de íconos de la pasada anterior → si el
        # usuario QUITA un PNG (✖ en Configuración), el cambio se ve al
        # instante al Guardar (antes el ícono viejo quedaba pegado hasta
        # reiniciar la app).
        self.icons.clear()
        self.pil_icons.clear()
        # v30: sin omni/dsh/chat/go — solo los iconos que siguen en el dock.
        built_default = {
            "folder": "folder_icon.png", "gdrive": "gdrive_icon.png",
            "notion": "notion_icon.png", "gtasks": "gtasks_icon.png",
            "settings": "settings_icon.png"
        }
        # alias: clave interna del dock → claves bajo las que pudo guardar el
        # diálogo de Configuración (la primera que exista gana)
        custom_aliases = {
            "gdrive": ("gdrive", "drive"),
            "gtasks": ("gtasks", "tasks"),
        }
        for key, default_fname in built_default.items():
            pil_img = None
            custom_path = None
            for ak in custom_aliases.get(key, (key,)):
                p = custom_icons_map.get(ak)
                if p and os.path.exists(p):
                    custom_path = p
                    break
            if custom_path:
                try:
                    pil_img = Image.open(custom_path).convert("RGBA")
                except: pil_img = None
            if pil_img is None:
                for base in [resource_path(default_fname), str(APP_DIR / default_fname), default_fname]:
                    if os.path.exists(base):
                        try:
                            pil_img = Image.open(base).convert("RGBA")
                            break
                        except: pass
            if pil_img is None:
                # v25: el PNG de fábrica NO está en disco → sale del
                # PROGRAMA (base64 embebido). Mover/borrar los archivos
                # ya NO deja botones sin icono.
                pil_img = _embedded_icon_img(default_fname)
            if pil_img is not None:
                if key == "settings":
                    pil_img = force_light_icon(pil_img)
                    # v19 FIX del tile del chat vacío: un PNG que sea una
                    # mancha uniforme (sin glifo distinguible) se ve como un
                    # tile vacío → se sustituye por el ícono de reserva
                    # dibujado con PIL (burbuja / engranaje).
                    if image_is_featureless(pil_img):
                        try:
                            print(f"[UIO Hub v31] icono del pie '{key}' sin "
                                  f"detalle (PNG uniforme) → uso ícono de reserva")
                            pil_img = draw_gear_glyph(96)
                        except Exception:
                            pass
                self.pil_icons[key] = pil_img
                target = FOOT_ICON if key == "settings" else BTN_SIZE
                sc = getattr(self, "ui_scale", 1.0)
                px = max(1, round(target * sc))
                rad = max(2, round(BTN_RADIUS * sc))
                try:
                    tile = rounded_tile(pil_img, px, rad)
                    self.icons[key] = ImageTk.PhotoImage(tile)
                except Exception:
                    pass

        # v19: si al final el pie NO tiene ícono (sin PNG y sin archivo
        # default), se genera el de reserva DIBUJADO con PIL — el botón nunca
        # queda vacío y deja de depender de glifos de fuente (💬/⚙ podían
        # salir como tofu o línea fina según la fuente de Windows).
        if HAS_PIL:
            for key, gen in (("settings", draw_gear_glyph),):
                if key in self.icons:
                    continue
                try:
                    pil_img = gen(96)
                    self.pil_icons[key] = pil_img
                    sc = getattr(self, "ui_scale", 1.0)
                    px = max(1, round(FOOT_ICON * sc))
                    rad = max(2, round(BTN_RADIUS * sc))
                    tile = rounded_tile(pil_img, px, rad)
                    self.icons[key] = ImageTk.PhotoImage(tile)
                except Exception:
                    pass

        for c in self.config_data.get("custom_buttons", []):
            ip = c.get("icon_path")
            if ip and os.path.exists(ip):
                try:
                    img = Image.open(ip).convert("RGBA")
                    self.pil_icons[c["id"]] = img
                    sc = getattr(self, "ui_scale", 1.0)
                    px = max(1, round(BTN_SIZE * sc))
                    rad = max(2, round(BTN_RADIUS * sc))
                    self.icons[c["id"]] = ImageTk.PhotoImage(
                        rounded_tile(img, px, rad))
                except: pass

    def build_grid(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.btn_widgets.clear()
        self.indicators.clear()

        base_buttons = [
            # v30: OmniRoute y DeepSeek Harness retirados — el dock arranca
            # directo con Proyectos.
            {"id": "folder", "label": "Proyectos", "icon_key": "folder", "type": "folder", "target_key": "projects_path"},
            {"id": "drive", "label": "Drive", "icon_key": "gdrive", "type": "web", "target_key": "drive_url"},
            {"id": "notion", "label": "Notion", "icon_key": "notion", "type": "web", "target_key": "notion_url"},
            {"id": "tasks", "label": "Tasks", "icon_key": "gtasks", "type": "web", "target_key": "tasks_url"},
        ]
        # v21: overrides del usuario (Configuración → "Botones"): nombre y
        # destino personalizados de los botones del sistema (el icono ya
        # vía custom_icons en load_all_icons). Sin override → valores de
        # fábrica (target_key lee la URL/carpeta de la config en vivo).
        _bl = self.config_data.get("base_labels", {}) or {}
        _bt = self.config_data.get("base_targets", {}) or {}
        for _b in base_buttons:
            _nl = str(_bl.get(_b["id"]) or "").strip()
            if _nl:
                _b["label"] = _nl
            _nt = str(_bt.get(_b["id"]) or "").strip()
            if _nt:
                _b["target"] = _nt
                _b.pop("target_key", None)   # destino directo, ya no la clave
        all_buttons = base_buttons + self.config_data.get("custom_buttons", [])
        sub_map = {"web": "Abrir web", "folder": "Abrir carpeta",
                   "shell": "Ejecutar comando"}

        # v30: UNA SOLA COLUMNA — cada botón en su propia fila y centrado,
        # en lugar de la grilla de dos columnas. Así el dock se ve como un
        # hub vertical (pedido expreso del usuario).
        for idx, bdef in enumerate(all_buttons):
            grid_row = idx
            cell = ctk.CTkFrame(self.grid_frame, fg_color="transparent", corner_radius=0)
            # v31a: padx 3→2, pady 4→3 (laterales y filas más juntas)
            cell.grid(row=grid_row, column=0, padx=2, pady=3, sticky="nsew")

            icon_key = bdef.get("icon_key") or bdef.get("id")
            label = bdef.get("label", "Btn")

            if HAS_PIL and (self.icons.get(icon_key) or self.icons.get(bdef.get("id"))):
                key = icon_key if icon_key in self.icons else bdef.get("id")
                btn = self._make_grid_button(parent_cell_holder=cell, key=key, label=label)
            else:
                btn_kwargs = dict(width=BTN_SIZE, height=BTN_SIZE, corner_radius=BTN_RADIUS,
                                  fg_color=BTN_BG, hover_color=BTN_HOVER,
                                  border_width=0)
                initials = "".join([w[0] for w in label.split()[:1]]).upper()[:2]
                btn = ctk.CTkButton(cell, text=initials, text_color="white",
                                    font=("Segoe UI", 11, "bold"), **btn_kwargs)
                btn.grid_propagate(False)
                self._bind_pressed(btn, None)
                self._tooltips.append(Tooltip(btn, lambda l=label: l))

            if bdef.get("type") == "shell":
                btn.configure(command=lambda t=bdef.get("target", ""): launch_powershell(t))
            elif bdef.get("type") == "folder":
                tk_key = bdef.get("target_key")
                if tk_key:
                    btn.configure(command=lambda k=tk_key: open_folder(self.config_data.get(k, "")))
                else:
                    btn.configure(command=lambda t=bdef.get("target", ""): open_folder(t))
            elif bdef.get("type") == "web":
                tk_key = bdef.get("target_key")
                if tk_key:
                    btn.configure(command=lambda k=tk_key: self.open_web_async(self.config_data.get(k, ""), True))
                else:
                    btn.configure(command=lambda t=bdef.get("target", ""),
                                           pc=bdef.get("prefer_chrome", True): self.open_web_async(t, pc))

            btn.pack()

            # v30: sin indicadores de servicio (OmniRoute/DSH retirados).
            # Queda el espaciador compacto bajo cada botón (v17: CTkLabel
            # tiene 28px mínimos por defecto → sin height=6 metía ~60px
            # de aire invisible).
            ctk.CTkLabel(cell, text="", fg_color="transparent",
                         font=("Segoe UI", 2), height=6).pack()

            # v17 guía §21: tooltip con nombre + acción (aparece a ~450ms)
            try:
                bid = bdef["id"]
                sub = sub_map.get(bdef.get("type", ""), "Abrir")
                self._tooltips.append(Tooltip(
                    self.icon_labels.get(icon_key) or
                    self.icon_labels.get(bid) or btn,
                    lambda l=label, s=sub: f"{l}\n{s}"))
            except Exception:
                pass

            btn.bdef = bdef
            self.btn_widgets[bdef["id"]] = btn
            btn.bind("<Enter>", lambda e: self.on_enter())
            btn.bind("<Leave>", lambda e: self.on_leave())

        # v30: separador ÚNICO al PIE de la columna (antes iba tras la fila
        # Omni+DeepSeek; con el hub de una columna va después del último
        # botón). Misma receta v23a: tk.Frame de 1px REAL — píxel exacto,
        # siempre visible — con un color de la PALETA (#343434, el mismo aro
        # de los iconos). sticky="ew" lo estira al ancho real de la grilla y
        # la línea del pie copia su ancho en vivo (ver _sync_sep_widths).
        _s = getattr(self, "ui_scale", 1.0)
        _sc = max(1, round(1 * _s))
        sep = tk.Frame(self.grid_frame, bg=SEP_COLOR, height=_sc,
                       bd=0, highlightthickness=0)
        sep.grid(row=len(all_buttons), column=0, sticky="ew", padx=4,
                 pady=(max(0, round(3 * _s)), max(0, round(5 * _s))))
        self.sep_frame = sep
        # v24a: la línea del pie copia el ancho real de esta (en vivo)
        try:
            self.after_idle(self._sync_sep_widths)
        except Exception:
            pass

        self.grid_frame.grid_columnconfigure(0, weight=1, uniform="col")
        for i in range(len(all_buttons) + 1):
            self.grid_frame.grid_rowconfigure(i, weight=0)

    def _asegurar_visible(self, intento=1):
        """v29b/v31c: garantiza que el dock se VEA al arrancar. Con "Iniciar
        UIO Hub al prender la PC" la ventana a veces quedaba escondida
        (Explorer todavía arrancando al prender la máquina) y el hub solo
        existía en la zona de iconos de la bandeja. Si el usuario no lo
        ocultó él mismo (✕ o clic en la bandeja), se re-muestra solo:
        intentos a los ~1 s, ~3 s y ~5 s. Después ya no vuelve a molestar:
        respetar el ✕ del usuario es prioridad.
        v31c: además de re-mostrar, CLAVA la posición dentro del área útil
        del monitor (si guardó la posición de un monitor que ya no está,
        la ventana quedaba fuera de pantalla) y fuerza topmost + foco
        (por si la ventana quedó visible pero DETRÁS de otras)."""
        try:
            if self._user_hid:
                return
            try:
                self.update_idletasks()
                w = max(80, self.winfo_reqwidth())
                h = max(60, self.winfo_reqheight())
                x, y = self.winfo_x(), self.winfo_y()
                if sys.platform == "win32":
                    try:
                        class _RECT(ctypes.Structure):
                            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                                        ("right", ctypes.c_long), ("bottom", ctypes.c_long)]
                        rc = _RECT()
                        # SPI_GETWORKAREA (0x0030): área útil sin la barra
                        if ctypes.windll.user32.SystemParametersInfoW(
                                0x0030, 0, ctypes.byref(rc), 0):
                            x2 = max(rc.left + 8, min(x, max(rc.left + 8, rc.right - w - 8)))
                            y2 = max(rc.top + 8, min(y, max(rc.top + 8, rc.bottom - h - 8)))
                            if (x2, y2) != (x, y):
                                self.geometry(f"+{x2}+{y2}")
                    except Exception:
                        pass
                if self._dock_oculto():
                    print(f"[UIO Hub v31] el dock arrancó escondido: "
                          f"re-mostrando (intento {intento})")
                    self.deiconify()
                self.attributes("-topmost", True)
                self.lift()
                try:
                    self.focus_force()
                except Exception:
                    pass
            except Exception:
                pass
            if intento < 3:
                self.after(2200, self._asegurar_visible, intento + 1)
        except Exception as e:
            print(f"[UIO Hub v31] asegurar visible: {e}")

    def on_enter(self, e=None):
        self.attributes("-alpha", self.config_data["opacity_hover"])

    def on_leave(self, e=None):
        self.after(150, self._check_leave)

    def _check_leave(self):
        x, y = self.winfo_pointerxy()
        wx, wy = self.winfo_rootx(), self.winfo_rooty()
        if not (wx <= x <= wx + self.winfo_width() and wy <= y <= wy + self.winfo_height()):
            self.attributes("-alpha", self.config_data["opacity_idle"])

    def open_config(self):
        UIOHubConfig(self, self.on_config_saved)

    def on_config_saved(self):
        global CONFIG
        CONFIG = load_config()
        self.config_data = CONFIG
        # v14: escala + iconos + grilla + pie + ventana, todo re-aplicado
        self.apply_ui_scale()
        self.attributes("-alpha", self.config_data["opacity_idle"])
        save_config(self.config_data)

    # ---------- v27b: BANDEJA (mostrar/ocultar/salir) ----------
    def _poll_tray(self):
        """Consume las órdenes del icono de bandeja (hilo Win32 → hilo Tk).
        El poller corre solo si la bandeja quedó instalada."""
        cmds = []
        try:
            if self._tray:
                cmds = self._tray.pop_commands()
        except Exception:
            cmds = []
        for c in cmds:
            if c == UIOTrayIcon.CMD_TOGGLE:
                self._tray_toggle()
            elif c == UIOTrayIcon.CMD_QUIT:
                self._real_quit()
                return
        try:
            self._tray_job = self.after(120, self._poll_tray)
        except Exception:
            pass

    def _dock_oculto(self):
        try:
            return self.state() == "withdrawn"
        except Exception:
            return False

    def hide_to_tray(self):
        """Oculta el dock (sigue corriendo en la bandeja)."""
        self._user_hid = True        # v29b: lo ocultó el usuario → no re-mostrar
        try:
            self.withdraw()
            save_config(self.config_data)
        except Exception:
            pass
        if not self._tray_hidden_once:
            self._tray_hidden_once = True
            try:
                if self._tray:
                    self._tray.notify("UIO Hub sigue abierto",
                                      "Está acá en la bandeja: clic para "
                                      "mostrar/ocultar, clic derecho para Salir.")
            except Exception:
                pass

    def show_from_tray(self):
        try:
            self.deiconify()
            self.attributes("-topmost", True)
            self.lift()
            try:
                self.focus_force()
            except Exception:
                pass
        except Exception:
            pass

    def _tray_toggle(self):
        if self._dock_oculto():
            self.show_from_tray()
        else:
            self.hide_to_tray()

    def tray_activo(self):
        """v27b: hay icono de bandeja UTILIZABLE ahora mismo (se instaló de
        una, o terminó de instalarse tras el arranque lento de Explorer)."""
        try:
            return bool(self._tray and (self._tray_ok or self._tray._ready()))
        except Exception:
            return False

    def on_close(self):
        """v27b: el ✕ OCULTA a la bandeja (modo segundo plano); el "Salir"
        real está en el menú del icono de la bandeja. Sin bandeja (no
        disponible), ✕ apaga como siempre."""
        try:
            if self.tray_activo():
                self.hide_to_tray()
                return
        except Exception:
            pass
        self._real_quit()

    def _real_quit(self):
        """Apagado real: bandeja fuera, config, ventana y proceso."""
        try:
            if self._tray_job:
                self.after_cancel(self._tray_job)
        except Exception:
            pass
        try:
            if self._tray:
                self._tray.stop()
        except Exception:
            pass
        save_config(self.config_data)
        try: self.destroy()
        except: pass
        time.sleep(0.1)
        os._exit(0)


if __name__ == "__main__":
    ensure_builtin_icons()          # v25: restaura PNG de fábrica si faltan
    _cambio = migrar_iconos_internos(CONFIG)   # v26: iconos propios → dentro del programa
    _cambio = reparar_rutas_iconos(CONFIG) or _cambio  # v26: repara rutas si la carpeta se mudó
    if _cambio:
        save_config(CONFIG)
    app = UIOHubBar()
    app.mainloop()