import streamlit as st
from datetime import datetime
import time
import pytz

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="CLARK KENT MODE", page_icon="👓", layout="centered")

# --- ESTILO VISUAL (CSS PERSONALIZADO) ---
st.markdown("""
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
    """, unsafe_allow_html=True)

# --- TIEMPO Y NAVEGACIÓN (TIJUANA) ---
tz = pytz.timezone('America/Tijuana') 
hoy_tj = datetime.now(tz)
dias_es = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", 
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}
dia_actual = dias_es.get(hoy_tj.strftime("%A"), "Lunes")

# --- PERSISTENCIA TEMPORAL: RECORDAR PESOS ---
if "historial_pesos" not in st.session_state:
    st.session_state.historial_pesos = {}

# --- GENERADOR AUTOMÁTICO DE VIDEOS DESDE GITHUB ---
def obtener_url_video(nombre_ejercicio):
    """
    Formatea el nombre del ejercicio idénticamente para buscarlo en tu repositorio de GitHub.
    Reemplaza los nombres de tu usuario, repositorio y carpeta según corresponda.
    """
    # Limpieza estándar: minúsculas, quitar paréntesis y cambiar espacios por guiones bajos
    nombre_limpio = nombre_ejercicio.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    # Quitar acentos comunes de forma manual para evitar fallos de URL
    for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]:
        nombre_limpio = nombre_limpio.replace(a, b)
        
    # Cambia 'TU_USUARIO', 'TU_REPOSITORIO' y 'videos' por los datos reales de tu GitHub
    url_base_github = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/videos/"
    return f"{url_base_github}{nombre_limpio}.mp4"

# --- HEADER ---
st.title("👓 CLARK KENT MODE: PROTOCOL 🦸‍♂️")
st.write("---")

c_r1, c_r2 = st.columns(2)
with c_r1:
    st.subheader(f"📅 Hoy es {dia_actual}")
with c_r2:
    st.markdown(f"<p style='text-align: right; color: #94a3b8;'>{hoy_tj.strftime('%d / %m / %Y')}</p>", unsafe_allow_html=True)

# --- BASE DE DATOS DE RUTINAS OPTIMIZADAS ---
rutinas = {
    "Lunes": [
        ("Press de Banca Plano (Barra Recta)", "3 × 6 a 8", 120, "Máxima tensión mecánica en el pecho."),
        ("Press Inclinado (Mancuernas)", "3 × 8 a 10", 90, "Estímulo a la porción superior (clavicular)."),
        ("Press Militar Sentado (Barra Recta)", "3 × 8 a 10", 90, "Masa general en el hombro y trapecio."),
        ("Elevaciones Laterales (Mancuernas)", "4 × 12 a 15", 60, "Ensanchar la silueta de lado a lado.")
    ],
    "Martes": [
        ("Remo Inclinado (Barra Recta)", "4 × 8 a 10", 90, "Trabaja romboides y trapecio medio."),
        ("Remo a una mano (Mancuerna)", "3 × 10 (por lado)", 90, "Mayor rango de estiramiento para tus brazos largos."),
        ("Rompecráneos (Barra Z en banco)", "3 × 10 a 12", 60, "Estimula la cabeza larga (gruesa) del tríceps."),
        ("Curl de Bíceps (Barra Z / Agarre normal)", "3 × 10 a 12", 60, "Hipertrofia directa en la cabeza del bíceps.")
    ],
    "Miércoles": [], 
    "Jueves": [
        ("Press Militar de pie (Mancuernas)", "3 × 10", 90, "Fuerza postural y estabilidad del core a tus 1.97 m."),
        ("Flexiones en banco (Manos elevadas)", "3 × Al fallo", 60, "Estímulo de pecho bajo y bombeo de tríceps."),
        ("Elevaciones Laterales (Mancuernas)", "4 × 12 a 15", 45, "Volumen metabólico en el deltoides lateral."),
        ("Curl Martillo (Mancuernas)", "3 × 10 a 12", 60, "Desarrolla el braquial (ensancha el brazo de lado)."),
        ("Copa de Tríceps (Una mancuerna pesada)", "3 × 12", 60, "Estiramiento profundo bajo carga para el tríceps.")
    ],
    "Viernes": [
        ("Prensa de Piernas (La de tu banco)", "4 × 12 a 15", 120, "Estímulo seguro a los cuádriceps."),
        ("Peso Muerto Rumano (Barra Recta)", "3 × 10 a 12", 90, "Fortalece femorales, glúteos y protege la zona lumbar."),
        ("Elevación de talones (Pantorrillas de pie)", "4 × 15 a 20", 45, "Rompe la elasticidad del tendón (aguanta 1s arriba/abajo)."),
        ("Elevación de Piernas (Acostado en banco)", "4 × 15 a 20", 60, "Hipertrofia del abdomen bajo (la 'V' del abdomen)."),
        ("Crunch Abdominal (En el suelo)", "3 × 15 a 20", 60, "Relieve e hipertrofia en los cuadritos superiores.")
    ],
    "Sábado": [], 
    "Domingo": [
        ("Plancha Abdominal (Plank tradicional)", "3 × 45-60 seg", 45, "Fortalece el core global en isometría."),
        ("Plancha Lateral (Side Plank)", "3 × 30 seg (por lado)", 30, "Activa oblicuos y da soporte lateral a la columna."),
        ("Bird-Dog (Perro de caza)", "3 × 12 repcs", 45, "Gran ejercicio biomecánico para la salud espinal."),
        ("Vacío Abdominal (Vacuum)", "4 × 30 seg", 30, "Reduce la circunferencia de la cintura (transverso).")
    ]
}

# --- LÓGICA DE OVERDRIVE / SELECCIÓN DE SESIÓN ---
if "overdrive" not in st.session_state: 
    st.session_state.overdrive = False

es_descanso_nativo = dia_actual in ["Miércoles", "Sábado"]

if es_descanso_nativo and not st.session_state.overdrive:
    st.info(f"🛌 Protocolo de Recuperación: Hoy {dia_actual} es descanso absoluto.")
    if st.button("⚡ FORCE OVERDRIVE MODE"):
        st.session_state.overdrive = True
        st.rerun()
else:
    if st.session_state.overdrive or es_descanso_nativo:
        st.warning("⚡ MODO OVERDRIVE ACTIVADO")
        seleccion_dia = st.selectbox("Selecciona el protocolo a ejecutar:", list(rutinas.keys()), index=list(rutinas.keys()).index(dia_actual))
        if st.button("❌ Volver a agenda normal"):
            st.session_state.overdrive = False
            st.rerun()
    else:
        seleccion_dia = st.selectbox("Protocolo activo:", list(rutinas.keys()), index=list(rutinas.keys()).index(dia_actual))

    ejercicios = rutinas.get(seleccion_dia, [])

    if not ejercicios:
        st.info("Formato de descanso seleccionado. No hay ejercicios agendados.")
    else:
        st.subheader(f"📋 Ejercicios – Enfoque de {seleccion_dia}")
        
        for nombre, reps, desc, enfoque in ejercicios:
            key_base = f"{seleccion_dia}_{nombre.replace(' ', '_')}"
            
            with st.expander(f"🏋️ {nombre} ➔ {reps}"):
                st.markdown(f"🎯 **Enfoque Técnico:** {enfoque}")
                st.markdown(f"⏱️ **Tiempo de Descanso:** {desc} segundos")
                
                # --- FUNCIÓN DE CARGAS (RECUERDA EL PESO) ---
                peso_anterior = st.session_state.historial_pesos.get(key_base, 0.0)
                peso_actual = st.number_input(
                    f"Registrar Peso Máximo (lb/kg):", 
                    min_value=0.0, 
                    value=float(peso_anterior), 
                    step=2.5, 
                    key=f"input_{key_base}"
                )
                st.session_state.historial_pesos[key_base] = peso_actual
                
                # --- CARGA DE VIDEOS DESDE GITHUB (IDÉNTICO) ---
                url_video = obtener_url_video(nombre)
                try:
                    st.video(url_video)
                except:
                    st.caption("⚠️ *Error al conectar con el archivo de video en GitHub.*")
                
                st.write("") 
                
                # --- TEMPORIZADOR ---
                if st.button(f"✅ CONCLUIR SERIE", key=f"btn_{key_base}"):
                    msg = st.empty()
                    bar = st.progress(0)
                    
                    for s in range(desc, -1, -1):
                        msg.subheader(f"⏳ Descansando: {s}s")
                        bar.progress((desc - s) / desc)
                        time.sleep(1)
                    
                    msg.success("💪 ¡Tiempo cumplido! Inicia la siguiente serie.")
                    st.balloons()
                    time.sleep(1)

# --- SIDEBAR: RESUMEN DE CARGAS MÁXIMAS ---
with st.sidebar:
    st.header("👓 Cuaderno de Cargas")
    st.write("Pesos usados en esta sesión:")
    
    if st.session_state.historial_pesos:
        for ej, peso in st.session_state.historial_pesos.items():
            if peso > 0:
                nombre_limpio = ej.split("_", 1)[1].replace("_", " ")
                st.markdown(f"• **{nombre_limpio}**: {peso}")
    else:
        st.caption("Aún no has registrado pesos hoy.")
        
    st.divider()
    st.caption("Clark Kent Protocol v2.6")
