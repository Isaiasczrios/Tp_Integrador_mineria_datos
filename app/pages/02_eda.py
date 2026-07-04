# -*- coding: utf-8 -*-
"""02_EDA.py

Adaptado desde Colab para despliegue en Streamlit Community Cloud.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Análisis Exploratorio de Datos (EDA)")
st.markdown("---")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_PATHS = [
    os.path.join(SCRIPT_DIR, 'streaming_users_clean.csv'),
    os.path.join(SCRIPT_DIR, '..', 'streaming_users_clean.csv'),
    os.path.join(SCRIPT_DIR, '..', '..', 'streaming_users_clean.csv'),
]
CSV_PATH = next((p for p in CANDIDATE_PATHS if os.path.exists(p)), None)
if CSV_PATH is None:
    st.error(
        "No se encontró 'streaming_users_clean.csv'. Se buscó en:\n\n"
        + "\n".join(f"- {os.path.normpath(p)}" for p in CANDIDATE_PATHS)
        + "\n\nVerificá que el archivo esté subido a GitHub en alguna de esas rutas."
    )
    st.stop()
df_clean = pd.read_csv(CSV_PATH)
sns.set_theme(style="whitegrid")

# --- VISUALIZACIONES UNIVARIADAS ---
st.markdown("## 📈 1. Distribuciones Univariadas")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.histplot(data=df_clean, x='age', bins=15, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribución de Edad de los Usuarios')
    st.pyplot(fig)
    st.caption("**Interpretación:** La población se concentra en un rango adulto-joven de entre 25 y 40 años.")

with col2:
    fig, ax = plt.subplots()
    country_counts = df_clean['country'].value_counts()
    sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis', ax=ax)
    ax.set_title('Volumen de Usuarios por País')
    st.pyplot(fig)
    st.caption("**Interpretación:** Distribución geográfica regional equilibrada tras consolidar los errores de tipeo.")

# --- VISUALIZACIONES BIVARIADAS ---
st.markdown("## 📊 2. Relaciones Bivariadas")
col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots()
    sns.boxplot(data=df_clean, x='subscription_plan', y='monthly_watch_time_mins', palette='Set2', ax=ax)
    ax.set_title('Consumo Mensual según Plan')
    st.pyplot(fig)
    st.caption("**Interpretación:** Los planes Premium y Estándar registran medianas de visualización marcadamente superiores.")

with col4:
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_clean, x='age', y='customer_support_tickets', alpha=0.5, color='coral', ax=ax)
    ax.set_title('Edad vs. Tickets de Soporte')
    st.pyplot(fig)
    st.caption("**Interpretación:** No se observa correlación lineal. Las incidencias técnicas ocurren de forma ajena a la edad.")

# --- VISUALIZACIÓN MULTIVARIADA ---
st.markdown("## 🔮 3. Análisis Multivariado")
fig_multi, ax_multi = plt.subplots(figsize=(8, 4))
sns.scatterplot(data=df_clean, x='age', y='monthly_watch_time_mins', hue='subscription_plan', palette='deep', alpha=0.7, ax=ax_multi)
ax_multi.set_title('Consumo por Edad Condicionado por el Plan')
st.pyplot(fig_multi)
st.markdown(
    "**Interpretación Obligatoria:** La visualización expone una clara estratificación horizontal. "
    "El factor determinante en el nivel de consumo de minutos mensuales es el **Plan de Suscripción**, "
    "operando de manera independiente a la edad cronológica del usuario."
)
