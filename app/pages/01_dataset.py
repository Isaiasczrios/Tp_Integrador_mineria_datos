import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Dataset", page_icon="📂", layout="wide")
st.title("📂 Dataset")

@st.cache_data
def load_data():
    # 1. Búsqueda blindada del JSON original
    try:
        with open("data/raw/streaming_users_dirty.json") as f:
            raw = pd.DataFrame(json.load(f))
    except FileNotFoundError:
        try:
            with open("streaming_users_dirty.json") as f:
                raw = pd.DataFrame(json.load(f))
        except FileNotFoundError:
            st.error("🚨 No se encontró el archivo JSON original.")
            st.stop()
            
    # 2. Búsqueda blindada del CSV limpio
    try:
        clean = pd.read_csv("data/processed/streaming_users_clean.csv")
    except FileNotFoundError:
        try:
            clean = pd.read_csv("streaming_users_clean.csv")
        except FileNotFoundError:
            try:
                clean = pd.read_csv("app/streaming_users_clean.csv")
            except FileNotFoundError:
                st.error("🚨 Error crítico: No se encuentra 'streaming_users_clean.csv'.")
                st.stop()
                
    return raw, clean

raw, clean = load_data()

st.markdown("## Descripción general")
st.markdown("""
El dataset contiene registros de usuarios de una plataforma de streaming con variables
demográficas, de comportamiento y de soporte. Fue provisto por la cátedra en formato JSON.

**Variables del dataset:**
- `user_id`: identificador único del usuario (sin valor analítico)
- `age`: edad del usuario (numérica)
- `subscription_plan`: plan contratado — Básico / Estándar / Premium (categórica ordinal)
- `monthly_watch_time_mins`: minutos de visualización en el mes (numérica continua)
- `country`: país del usuario (categórica nominal)
- `favorite_genre`: género favorito (categórica nominal)
- `last_login_date`: fecha del último acceso a la plataforma (fecha)
- `customer_support_tickets`: cantidad de tickets de soporte generados (numérica entera)
""")

st.markdown("---")
st.markdown("## Calidad del dataset original")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Filas originales", f"{raw.shape[0]}")
col2.metric("Nulos detectados", "320")
col3.metric("Fechas futuras", "882")
col4.metric("Filas finales", f"{clean.shape[0]}")

st.markdown("### Principales problemas y acciones tomadas")
problemas = pd.DataFrame({
    "Variable": ["user_id", "subscription_plan", "country", "favorite_genre", "monthly_watch_time_mins", "monthly_watch_time_mins", "age", "customer_support_tickets", "last_login_date", "last_login_date", "Múltiples"],
    "Problema detectado": [
        "100 registros duplicados",
        "15 variantes para 3 planes (Std, STANDARD, Basic, Premiun, estandar...)",
        "26 variantes para 7 países (Brazil/Brasil/BRA, Mexico/México/MEX...)",
        "29 variantes para 7 géneros + 240 nulos (CRIME/Crime/Crimen, comedy/Comedia...)",
        "Valores imposibles: -5 (21 registros), 130 (34), 150 (19)",
        "Valores negativos: -120 (29 registros), -1 (20)",
        "Valores imposibles: 50000 (11 registros), 99999 (20) + 193 nulos",
        "Valores imposibles: -1 (29 registros), 99 (35), 150 (32)",
        "Formatos mixtos: YYYY-MM-DD y YYYY/MM/DD",
        "882 fechas futuras posteriores al 2025-06-27",
        "320 valores nulos"
    ],
    "Acción": [
        "Eliminación de duplicados",
        "Mapeo a 3 categorías normalizadas",
        "Mapeo a 7 países normalizados",
        "Mapeo a 7 géneros normalizados + imputación con moda",
        "Eliminación del registro",
        "Eliminación del registro",
        "Eliminación del registro + imputación con mediana",
        "Eliminación del registro",
        "Unificación con pd.to_datetime(format='mixed')",
        "Eliminación de registros inconsistentes",
        "Eliminación de filas con nulos (dropna)"
    ]
})
st.table(problemas)

st.markdown("---")
st.markdown("## Dataset limpio")
st.dataframe(clean)
