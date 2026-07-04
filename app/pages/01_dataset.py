import streamlit as st
import pandas as pd

st.title("🗃️ Inspección del Dataset")
st.markdown("---")

# ==========================================
# CÓDIGO BLINDADO PARA ENCONTRAR EL CSV
# ==========================================
try:
    # Intento 1: Ruta ideal (Si respetaste la estructura data/processed/ en GitHub)
    df_clean = pd.read_csv('data/processed/streaming_users_clean.csv')
except FileNotFoundError:
    try:
        # Intento 2: Por si subiste el CSV suelto en la raíz de tu GitHub
        df_clean = pd.read_csv('streaming_users_clean.csv')
    except FileNotFoundError:
        try:
            # Intento 3: Por si lo pusiste adentro de la carpeta app/
            df_clean = pd.read_csv('app/streaming_users_clean.csv')
        except FileNotFoundError:
            # Si falla todo, mostramos un error en rojo
            st.error("🚨 Error crítico: No se encuentra el archivo 'streaming_users_clean.csv' en GitHub.")
            st.stop()
# ==========================================

st.markdown("### 📋 Descripción General")
st.write(f"El conjunto de datos final procesado cuenta con **{df_clean.shape[0]}** filas y **{df_clean.shape[1]}** columnas.")

st.markdown("### 🔍 Resumen de Calidad y Transformaciones")
st.success(
    "Durante la etapa de preparación en el Notebook 02, se aplicó una limpieza consciente basada en evidencia:\n"
    "1. **Corrección de Tipeo:** Se estandarizaron las inconsistencias por mayúsculas intercaladas y faltas de ortografía "
    "en los nombres de países (`country`) y planes de suscripción (`subscription_plan`), unificando en Básico, Estándar y Premium.\n"
    "2. **Tratamiento de Outliers:** Los valores atípicos severos (150 años de edad y 99 tickets de soporte) fueron imputados "
    "mediante la mediana robusta de la distribución para no sesgar las varianzas.\n"
    "3. **Conversión Temporal:** Se tipificó `last_login_date` como formato datetime."
)

st.markdown("### 👀 Vista Previa de los Datos Limpios")
st.dataframe(df_clean.head(15))
