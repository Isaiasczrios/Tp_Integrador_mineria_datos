import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Análisis Exploratorio de Datos (EDA)")
st.markdown("---")

# ==========================================
# CÓDIGO BLINDADO PARA ENCONTRAR EL CSV
# ==========================================
try:
    df_clean = pd.read_csv('data/processed/streaming_users_clean.csv')
except FileNotFoundError:
    try:
        df_clean = pd.read_csv('streaming_users_clean.csv')
    except FileNotFoundError:
        try:
            df_clean = pd.read_csv('app/streaming_users_clean.csv')
        except FileNotFoundError:
            st.error("🚨 Error crítico: No se encuentra el archivo 'streaming_users_clean.csv' en GitHub.")
            st.stop()
# ==========================================

sns.set_theme(style="whitegrid")

# --- VISUALIZACIONES UNIVARIADAS ---
st.markdown("## 📈 1. Distribuciones Univariadas")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.histplot(data=df_clean, x='age', bins=15, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribución de Edad')
    st.pyplot(fig)
    st.caption("**Interpretación:** La población se concentra en un rango adulto-joven de entre 25 y 40 años.")

with col2:
    fig, ax = plt.subplots()
    country_counts = df_clean['country'].value_counts()
    sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis', ax=ax)
    ax.set_title('Volumen de Usuarios por País')
    st.pyplot(fig)
    st.caption("**Interpretación:** Distribución geográfica equilibrada tras consolidar errores.")

# --- VISUALIZACIONES BIVARIADAS ---
st.markdown("## 📊 2. Relaciones Bivariadas")
col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots()
    sns.boxplot(data=df_clean, x='subscription_plan', y='monthly_watch_time_mins', palette='Set2', ax=ax)
    ax.set_title('Consumo Mensual según Plan')
    st.pyplot(fig)
    st.caption("**Interpretación:** Premium y Estándar registran medianas superiores.")

with col4:
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_clean, x='age', y='customer_support_tickets', alpha=0.5, color='coral', ax=ax)
    ax.set_title('Edad vs. Tickets de Soporte')
    st.pyplot(fig)
    st.caption("**Interpretación:** No se observa correlación lineal. Incidencias ajenas a la edad.")

# --- VISUALIZACIÓN MULTIVARIADA ---
st.markdown("## 🔮 3. Análisis Multivariado")
fig_multi, ax_multi = plt.subplots(figsize=(8, 4))
sns.scatterplot(data=df_clean, x='age', y='monthly_watch_time_mins', hue='subscription_plan', palette='deep', alpha=0.7, ax=ax_multi)
ax_multi.set_title('Consumo por Edad Condicionado por el Plan')
st.pyplot(fig_multi)
st.markdown(
    "**Interpretación Obligatoria:** La visualización expone una clara estratificación horizontal. "
    "El factor determinante en el nivel de consumo es el **Plan de Suscripción**."
)
