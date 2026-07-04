# -*- coding: utf-8 -*-
"""04_Conclusiones.py

Adaptado desde Colab para despliegue en Streamlit Community Cloud.
"""

import streamlit as st

st.title("📝 Conclusiones Finales")
st.markdown("---")

st.markdown("### 💡 Hallazgos Principales")
st.write(
    "El nivel de consumo en la plataforma está ligado directamente a la estructura contractual "
    "del plan adquirido por el usuario (Premium/Estándar), y no a variables biológicas o demográficas "
    "como la edad."
)

st.markdown("### ⚠️ Limitaciones Detectadas")
st.warning(
    "El dataset presenta un corte transversal estático (un momento fijo en el tiempo). "
    "Al no disponer de series temporales o registros históricos continuos, no es posible evaluar "
    "causalidad directa en la deserción de clientes (churn)."
)

st.markdown("### 🚀 Próximos Pasos y Mejoras")
st.write(
    "1. Incorporar variables cualitativas de soporte técnico basadas en categorías de problemas.\n"
    "2. Implementar un esquema automatizado de validación continua de datos en la interfaz de registro "
    "para bloquear el ingreso de cadenas inconsistentes o edades biológicamente imposibles."
)
