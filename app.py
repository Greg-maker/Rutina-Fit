import os
import re
import time
import unicodedata
from datetime import datetime

import pytz
import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="CLARK KENT MODE", page_icon="👓", layout="centered"
)

# --- ESTILO VISUAL (CSS PERSONALIZADO) ---
st.markdown(
    """
    <style>
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .stExpander { border: 1px solid #334155; border-radius: 8px; background-color: #0f172a; margin-bottom: 10px; }
    
    div.stButton > button:first-child { 
        background-color: #1d4ed8; 
        color: white; 
        border: none; 
        font-weight: bold; 
        width: 100%; 
        height: 3em;
        font-size: 1.2em;
        border-radius: 6px;
    }
    div.stButton > button:first-child:hover { background-color: #1e40af; }
    .stProgress > div > div > div > div { background-color: #dc2626; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TIEMPO Y NAVEGACIÓN (TIJUANA) ---
tz = pytz.timezone("America/Tijuana")
hoy_tj = datetime.now(tz)
dias_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}
dia_actual = dias_es.get(hoy_tj.strftime("%A"), "Lunes")

# --- PERSISTENCIA TEMPORAL: RECORDAR PESOS ---
if "historial_pesos" not in st.session_state:
    st.session_state.historial_pesos = {}


# --- LOCALIZADOR DE ARCHIVOS DE VIDEO EN LA RAÍZ ---
def obtener_ruta_local_video(nombre_ejercicio):
    # 1. Eliminar acentos/tildes (ej: "Bíceps" -> "Biceps")
    nombre_normalizado = unicodedata.normalize("NFD", nombre_ejercicio)
    nombre_sin_acentos = "".join(
        c for c in nombre_normalizado if unicodedata.category(c) != "MN"
    )

    # 2. Convertir a minúsculas y limpiar caracteres especiales o paréntesis
    nombre_limpio = nombre_sin_acentos.lower().strip()
    nombre_limpio = re.sub(r"\s+", "_", nombre_limpio)  # Reemplaza espacios por _
    nombre_limpio = re.sub(
        r"[^a-z0-9_]", "", nombre_limpio
    )  # Solo letras, números y _

    # 3. Ruta directa en el directorio raíz
    ruta_archivo = f"{nombre_limpio}.mp4"

    # 4. Verificar existencia
    if os.path.exists(ruta_archivo):
        return ruta_archivo

    return None


# --- FUNCIÓN REUTILIZABLE PARA TEMPORIZADOR ---
def ejecutar_temporizador(segundos, key_btn):
    if st.button(f"✅ CONCLUIR SERIE", key=key_btn):
        msg = st.empty()
        bar = st.progress(0)
        for s in range(segundos, -1, -1):
            msg.subheader(f"⏳ Descansando: {s}s")
            bar.progress((segundos - s) / segundos)
            time.sleep(1)
        msg.success("💪 ¡Tiempo cumplido!")
        st.balloons()
        time.sleep(1)


# --- BASE DE DATOS DE RUTINAS ---
rutinas = {
    "Lunes": [
        (
            "Press de Banca Plano (Barra Recta)",
            "3 × 6 a 8",
            120,
            "Máxima tensión mecánica en el pecho.",
        ),
        (
            "Press Inclinado (Mancuernas)",
            "3 × 8 a 10",
            90,
            "Estímulo a la porción superior (clavicular).",
        ),
        (
            "Press Militar Sentado (Barra Recta)",
            "3 × 8 a 10",
            90,
            "Masa general en el hombro y trapecio.",
        ),
        (
            "Elevaciones Laterales (Mancuernas)",
            "4 × 12 a 15",
            60,
            "Ensanchar la silueta de lado a lado.",
        ),
    ],
    "Martes": [
        (
            "Remo Inclinado (Barra Recta)",
            "4 × 8 a 10",
            90,
            "Trabaja romboides y trapecio medio.",
        ),
        (
            "Remo a una mano (Mancuerna)",
            "3 × 10 (por lado)",
            90,
            "Mayor rango de estiramiento para tus brazos largos.",
        ),
        (
            "Rompecráneos (Barra Z en banco)",
            "3 × 10 a 12",
            60,
            "Estimula la cabeza larga (gruesa) del tríceps.",
        ),
        (
            "Curl de Bíceps (Barra Z / Agarre normal)",
            "3 × 10 a 12",
            60,
            "Hipertrofia directa en la cabeza del bíceps.",
        ),
    ],
    "Miércoles": [],
    "Jueves": [
        (
            "Press Militar de pie (Mancuernas)",
            "3 × 10",
            90,
            "Fuerza postural y estabilidad del core a tus 1.97 m.",
        ),
        (
            "Flexiones en banco (Manos elevadas)",
            "3 × Al fallo",
            60,
            "Estímulo de pecho bajo y bombeo de tríceps.",
        ),
        (
            "Elevaciones Laterales (Mancuernas)",
            "4 × 12 a 15",
            45,
            "Volumen metabólico en el deltoides lateral.",
        ),
        (
            "Curl Martillo (Mancuernas)",
            "3 × 10 a 12",
            60,
            "Desarrolla el braquial (ensancha el brazo de lado).",
        ),
        (
            "Copa de Tríceps (Una mancuerna pesada)",
            "3 × 12",
            60,
            "Estiramiento profundo bajo carga para el tríceps.",
        ),
    ],
    "Viernes": [
        (
            "Prensa de Piernas (La de tu banco)",
            "4 × 12 a 15",
            120,
            "Estímulo seguro a los cuádriceps.",
        ),
        (
            "Peso Muerto Rumano (Barra Recta)",
            "3 × 10 a 12",
            90,
            "Fortalece femorales, glúteos y protege la zona lumbar.",
        ),
        (
            "Elevación de talones (Pantorrillas de pie)",
            "4 × 15 a 20",
            45,
            "Rompe la elasticidad del tendón (aguanta 1s arriba/abajo).",
        ),
        (
            "Elevación de Piernas (Acostado en banco)",
            "4 × 15 a 20",
            60,
            "Hipertrofia del abdomen bajo (la 'V' del abdomen).",
        ),
        (
            "Crunch Abdominal (En el suelo)",
            "3 × 15 a 20",
            60,
            "Relieve e hipertrofia en los cuadritos superiores.",
        ),
    ],
    "Sábado": [],
    "Domingo": [
        (
            "Plancha Abdominal (Plank tradicional)",
            "3 × 45-60 seg",
            45,
            "Fortalece el core global en isometría.",
        ),
        (
            "Plancha Lateral (Side Plank)",
            "3 × 30 seg (por lado)",
            30,
            "Activa oblicuos y da soporte lateral a la columna.",
        ),
        (
            "Bird-Dog (Perro de caza)",
            "3 × 12 repcs",
            45,
            "Gran ejercicio biomecánico para la salud espinal.",
        ),
        (
            "Vacío Abdominal (Vacuum)",
            "4 × 30 seg",
            30,
            "Reduce la circunferencia de la cintura (transverso).",
        ),
    ],
}

# --- SIDEBAR: CUADERNO DE CARGAS Y CONTROLES ---
with st.sidebar:
    st.header("👓 Cuaderno de Cargas")

    st.subheader("🔥 Protocolos Especiales")
    modo_grip = st.toggle(
        "🟢 RUTINA VASCULAR GRIP",
        value=False,
        help="Activa de forma fija la rutina de Hand Grip e hipertrofia de antebrazo.",
    )

    st.divider()
    st.write("Pesos guardados:")

    hay_pesos = False
    for ej_key, peso in st.session_state.historial_pesos.items():
        if peso > 0:
            hay_pesos = True
            nombre_mostrar = (
                ej_key.replace("ej_", "")
                .split("_", 1)[1]
                .replace("_", " ")
                .title()
            )
            st.markdown(f"• **{nombre_mostrar}**: {peso}")

    if not hay_pesos:
        st.caption("Aún no has registrado pesos hoy.")

    st.divider()
    st.caption("Clark Kent Protocol v2.9")

# --- HEADER PRINCIPAL ---
st.title("👓 CLARK KENT MODE: PROTOCOL 🦸‍♂️")
st.write("---")

c_r1, c_r2 = st.columns(2)
with c_r1:
    st.subheader(f"📅 Hoy es {dia_actual}")
with c_r2:
    st.markdown(
        f"<p style='text-align: right; color: #94a3b8;'>{hoy_tj.strftime('%d / %m / %Y')}</p>",
        unsafe_allow_html=True,
    )


# ==========================================
# LÓGICA 1: MODO VASCULAR GRIP ACTIVADO
# ==========================================
if modo_grip:
    st.warning(
        "💪 MODO VASCULAR GRIP FIJO – Enfoque: Antebrazos de Acero y Agarre Aplastante"
    )

    # FASE 1: Calentamiento
    st.subheader("🟢 FASE 1: El Calentamiento (Obligatorio)")
    st.info(
        "Haz esto para lubricar las articulaciones, llevar sangre al músculo y evitar lesiones."
    )

    with st.expander("👋 1. Rotación de muñecas (30 seg)"):
        st.write(
            "Entrelaza los dedos de ambas manos y haz giros suaves hacia la derecha y hacia la izquierda."
        )
        ejecutar_temporizador(30, "cal_1")

    with st.expander("👐 2. Abrir y cerrar al aire (1 min)"):
        st.write(
            "Estira los brazos al frente y abre y cierra las manos lo más rápido posible (abriendo bien los dedos) de forma continua."
        )
        ejecutar_temporizador(60, "cal_2")

    with st.expander("⚙️ 3. Serie de aproximación (15 repes x lado)"):
        st.write(
            "Pon tu hand grip en la resistencia más baja y haz 15 repeticiones fluidas con cada mano."
        )
        ejecutar_temporizador(45, "cal_3")

    # FASE 2: Rutina Principal
    st.subheader("🔥 FASE 2: La Rutina 'Vascular Grip'")
    st.caption(
        "🚨 **Nota sobre el descanso:** Haz la mano derecha, luego la izquierda sin parar, y ahí cuentas el tiempo de descanso antes de la siguiente serie."
    )

    # Ejercicio 1
    with st.expander(
        "⚡ Ejercicio 1: Compresión Lenta (Fuerza y Grosor) ➔ 3 × 10 a 12"
    ):
        st.markdown(
            "**Cómo se hace:** Sujeta el hand grip normalmente. Ciérralo lentamente hasta que peguen las dos manijas. Mantén la presión al máximo durante 3 segundos y luego abre la mano despacio, controlando la bajada."
        )
        st.markdown(
            "🎯 **Volumen:** 3 series de 10 a 12 repeticiones por mano."
        )

        peso_previo = st.session_state.historial_pesos.get(
            "ej_grip_compresion_lenta", 0.0
        )
        peso_nuevo = st.number_input(
            "Registrar Resistencia/Peso:",
            min_value=0.0,
            value=float(peso_previo),
            step=1.0,
            key="input_grip_1",
        )
        st.session_state.historial_pesos["ej_grip_compresion_lenta"] = (
            peso_nuevo
        )

        st.markdown("⏱️ **Tiempo de Descanso:** 60 a 90 segundos")
        ejecutar_temporizador(75, "btn_grip_1")

    # Ejercicio 2
    with st.expander(
        "⚡ Ejercicio 2: Compresión Rápida (El Quemador / Bombeo) ➔ 3 × 30 seg"
    ):
        st.markdown(
            "**Cómo se hace:** Baja un poco la resistencia. Cierra y abre la mano lo más rápido que puedas de forma fluida. No te detengas aunque el ritmo baje en los últimos segundos por el cansancio."
        )
        st.markdown(
            "🎯 **Volumen:** 3 series de 30 segundos continuos por mano."
        )

        peso_previo = st.session_state.historial_pesos.get(
            "ej_grip_compresion_rapida", 0.0
        )
        peso_nuevo = st.number_input(
            "Registrar Resistencia/Peso:",
            min_value=0.0,
            value=float(peso_previo),
            step=1.0,
            key="input_grip_2",
        )
        st.session_state.historial_pesos["ej_grip_compresion_rapida"] = (
            peso_nuevo
        )

        st.markdown(
            "⏱️ **Tiempo de Descanso:** ¡Solo 15 segundos! (Para acumular el máximo bombeo)"
        )
        ejecutar_temporizador(15, "btn_grip_2")

    # Ejercicio 3
    with st.expander(
        "⚡ Ejercicio 3: Sostenimiento Estático (Isometría / Venas a tope) ➔ 3 × Al Fallo"
    ):
        st.markdown(
            "**Cómo se hace:** Cierra el hand grip por completo con todas tus fuerzas y mantenlo cerrado, apretando duro sin soltar el agarre hasta que los dedos se te abran solos por el cansancio."
        )
        st.markdown(
            "🎯 **Volumen:** 3 series por mano (buscando aguantar entre 20 y 30 segundos por serie)."
        )

        peso_previo = st.session_state.historial_pesos.get(
            "ej_grip_sostenimiento_estatico", 0.0
        )
        peso_nuevo = st.number_input(
            "Registrar Resistencia/Peso:",
            min_value=0.0,
            value=float(peso_previo),
            step=1.0,
            key="input_grip_3",
        )
        st.session_state.historial_pesos["ej_grip_sostenimiento_estatico"] = (
            peso_nuevo
        )

        st.markdown("⏱️ **Tiempo de Descanso:** 60 segundos")
        ejecutar_temporizador(60, "btn_grip_3")

    # Ejercicio 4
    with st.expander(
        "⚡ Ejercicio 4: Agarre de Pinza (Fuerza de Dedos y Rocosidad) ➔ 3 × Al Fallo"
    ):
        st.markdown(
            "**Cómo se hace:** Sujeta el hand grip usando solo las yemas de tus dedos (el pulgar en un mango y los otros cuatro dedos en el otro, sin que el aparato toque la palma de tu mano). Ciérralo y mantén la presión."
        )
        st.markdown("🎯 **Volumen:** 3 series al fallo por mano.")

        peso_previo = st.session_state.historial_pesos.get(
            "ej_grip_agarre_pinza", 0.0
        )
        peso_nuevo = st.number_input(
            "Registrar Resistencia/Peso:",
            min_value=0.0,
            value=float(peso_previo),
            step=1.0,
            key="input_grip_4",
        )
        st.session_state.historial_pesos["ej_grip_agarre_pinza"] = peso_nuevo

        st.markdown("⏱️ **Tiempo de Descanso:** 45 a 60 segundos")
        ejecutar_temporizador(50, "btn_grip_4")


# ==========================================
# LÓGICA 2: MODO AGENDA NORMAL
# ==========================================
else:
    if "overdrive" not in st.session_state:
        st.session_state.overdrive = False

    es_descanso_nativo = dia_actual in ["Miércoles", "Sábado"]

    if es_descanso_nativo and not st.session_state.overdrive:
        st.info(
            f"🛌 Protocolo de Recuperación: Hoy {dia_actual} es descanso absoluto."
        )
        if st.button("⚡ FORCE OVERDRIVE MODE"):
            st.session_state.overdrive = True
            st.rerun()
    else:
        if st.session_state.overdrive or es_descanso_nativo:
            st.warning("⚡ MODO OVERDRIVE ACTIVADO")
            seleccion_dia = st.selectbox(
                "Selecciona el protocolo:",
                list(rutinas.keys()),
                index=list(rutinas.keys()).index(dia_actual),
            )
            if st.button("❌ Volver a agenda normal"):
                st.session_state.overdrive = False
                st.rerun()
        else:
            seleccion_dia = st.selectbox(
                "Protocolo activo:",
                list(rutinas.keys()),
                index=list(rutinas.keys()).index(dia_actual),
            )

        ejercicios = rutinas.get(seleccion_dia, [])

        if not ejercicios:
            st.info("Formato de descanso seleccionado.")
        else:
            st.subheader(f"📋 Ejercicios – {seleccion_dia}")

            for nombre, reps, desc, enfoque in ejercicios:
                id_unico = f"ej_{seleccion_dia}_{nombre.replace(' ', '_')}".lower()

                with st.expander(f"🏋️ {nombre} ➔ {reps}"):

                    # 1. ENTRADA DE PESO RECORDATORIO
                    peso_previo = st.session_state.historial_pesos.get(
                        id_unico, 0.0
                    )
                    peso_nuevo = st.number_input(
                        "Registrar Peso Máximo (lb/kg):",
                        min_value=0.0,
                        value=float(peso_previo),
                        step=2.5,
                        key=f"input_{id_unico}",
                    )
                    st.session_state.historial_pesos[id_unico] = peso_nuevo

                    st.markdown(f"🎯 **Enfoque Técnico:** {enfoque}")
                    st.markdown(f"⏱️ **Tiempo de Descanso:** {desc} segundos")

                    # 2. REPRODUCTOR DE VIDEO LOCAL (.mp4) EN LA RAÍZ
                    ruta_video = obtener_ruta_local_video(nombre)

                    if ruta_video:
                        st.video(ruta_video)
                    else:
                        nombre_limpio_sugerido = (
                            "".join(
                                c
                                for c in unicodedata.normalize(
                                    "NFD", nombre.lower()
                                )
                                if unicodedata.category(c) != "MN"
                            )
                            .replace(" ", "_")
                            .replace("(", "")
                            .replace(")", "")
                            .replace("/", "_")
                        )
                        st.caption(
                            f"ℹ️ Video no encontrado. Nómbralo como: `{nombre_limpio_sugerido}.mp4` junto a este archivo."
                        )

                    st.write("---")

                    # 3. TEMPORIZADOR DE DESCANSO
                    ejecutar_temporizador(desc, f"btn_{id_unico}")
