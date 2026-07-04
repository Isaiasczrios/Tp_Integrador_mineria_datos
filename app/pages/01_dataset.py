# -*- coding: utf-8 -*-
"""01_Dataset.py

Adaptado desde Colab para despliegue en Streamlit Community Cloud.
"""

import os
import streamlit as st
import pandas as pd

st.title("🗃️ Inspección del Dataset")
st.markdown("---")

# Ruta del CSV relativa a la ubicación de este script (funciona sin importar
# desde qué directorio de trabajo Streamlit Cloud ejecute la app)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_PATHS = [
    os.path.join(SCRIPT_DIR, 'streaming_users_clean.csv'),            # misma carpeta que el script
    os.path.join(SCRIPT_DIR, '..', 'streaming_users_clean.csv'),      # un nivel arriba (app/)
    os.path.join(SCRIPT_DIR, '..', '..', 'streaming_users_clean.csv'),# raíz del repo
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
