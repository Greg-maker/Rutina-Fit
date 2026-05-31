import streamlit as st
from datetime import datetime
import time
import pytz

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="CLARK KENT MODE", page_icon="👓", layout="centered")

# --- ESTILO VISUAL (CSS PERSONALIZADO) ---
st.markdown("""
    <style>
    /* Cambiar el fondo general y tarjetas a tonos oscuros/azules acero */
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .stExpander { border: 1px solid #334155; border-radius: 8px; background-color: #0f172a; margin-bottom: 10px; }
    
    /* Botón de acción principal en Azul Metrópolis / Superman */
    div.stButton > button:first-child { 
        background-color: #1d4ed8; 
        color: white; 
        border: none; 
        font-weight: bold; 
        width: 100%; 
        height: 3em;
        font-size: 1.2em;
        border-radius: 6px;
        transition: background-color 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #1e40af;
    }
    
    /* Barra de progreso en rojo sutil */
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
        ("Elevaciones Laterales (Mancuernas)", "4 × 12 to 15", 60, "Ensanchar la silueta de lado a lado.")
    ],
    "Martes": [
        ("Remo Inclinado (Barra Recta)", "4 × 8 a 10", 90, "Trabaja romboides y trapecio medio."),
        ("Remo a una mano (Mancuerna)", "3 × 10 (por lado)", 90, "Mayor rango de estiramiento para tus brazos largos."),
        ("Rompecráneos (Barra Z en banco)", "3 × 10 a 12", 60, "Estimula la cabeza larga (gruesa) del tríceps."),
        ("Curl de Bíceps (Barra Z / Agarre normal)", "3 × 10 a 12", 60, "Hipertrofia directa en la cabeza del bíceps.")
    ],
    "Miércoles": [], # Descanso absoluto
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
    "Sábado": [], # Descanso total
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

# Verificar si el día actual de forma nativa es de descanso (Miércoles o Sábado)
es_descanso_nativo = dia_actual in ["Miércoles", "Sábado"]

if es_descanso_nativo and not st.session_state.overdrive:
    st.info(f"🛌 Protocolo de Recuperación: Hoy {dia_actual} es descanso absoluto. Permite que el sistema nervioso se adapte.")
    if st.button("⚡ FORCE OVERDRIVE MODE"):
        st.session_state.overdrive = True
        st.rerun()
else:
    # Selector de días visible si estás en Overdrive o si quieres revisar otra sesión
    if st.session_state.overdrive or es_descanso_nativo:
        st.warning("⚡ MODO OVERDRIVE ACTIVADO (Entrenamiento fuera de agenda)")
        seleccion_dia = st.selectbox("Selecciona el protocolo a ejecutar:", list(rutinas.keys()), index=list(rutinas.keys()).index(dia_actual))
        if st.button("❌ Volver a agenda normal"):
            st.session_state.overdrive = False
            st.rerun()
    else:
        # Por defecto muestra el día de la semana en el que estás, con opción de cambiarlo abajo
        seleccion_dia = st.selectbox("Protocolo activo:", list(rutinas.keys()), index=list(rutinas.keys()).index(dia_actual))

    ejercicios = rutinas.get(seleccion_dia, [])

    if not ejercicios:
        st.info("Formato de descanso seleccionado. No hay ejercicios agendados.")
    else:
        st.subheader(f"📋 Ejercicios – Enfoque de {seleccion_dia}")
        
        # Iterar sobre los ejercicios optimizados
        for nombre, reps, desc, enfoque in ejercicios:
            with st.expander(f"🏋️ {nombre} ➔ {reps}"):
                st.markdown(f"🎯 **Enfoque Técnico:** {enfoque}")
                st.markdown(f"⏱️ **Tiempo de Descanso:** {desc} segundos")
                
                # Sistema de temporizador integrado por ejercicio
                if st.button(f"✅ CONCLUIR SERIE", key=f"btn_{nombre.replace(' ', '_')}"):
                    msg = st.empty()
                    bar = st.progress(0)
                    
                    for s in range(desc, -1, -1):
                        msg.subheader(f"⏳ Descansando: {s}s")
                        bar.progress((desc - s) / desc)
                        time.sleep(1)
                    
                    msg.success("💪 ¡Tiempo cumplido! Inicia la siguiente serie.")
                    st.balloons()
                    time.sleep(1)

# --- SIDEBAR ---
with st.sidebar:
    st.header("👓 Configuración")
    st.caption("Clark Kent Protocol v2.0")
    st.write("Diseñado específicamente para optimizar palancas largas y control postural.")
