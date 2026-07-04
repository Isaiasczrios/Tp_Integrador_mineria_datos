import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

st.title("🔮 Reducción de Dimensionalidad (PCA)")
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

variables_num = ['age', 'monthly_watch_time_mins', 'customer_support_tickets']

st.markdown("### 🛠️ Configuración de Escalamiento")
st.info(
    "**Condición No Negociable:** Se aplicó un escalamiento Z-score (`StandardScaler`) previo al algoritmo. "
    "Esto iguala las magnitudes numéricas evitando sesgos artificiales."
)

# Preparación segura y remoción de NaNs
X_pure = df_clean[variables_num].dropna()
X_scaled = StandardScaler().fit_transform(X_pure)

pca = PCA()
X_pca = pca.fit_transform(X_scaled)
var_explicada = pca.explained_variance_ratio_

# Visualización 1: Scree Plot 
st.markdown("### 📈 1. Varianza Explicada Acumulada")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(range(1, len(var_explicada) + 1), np.cumsum(var_explicada), marker='o', linestyle='--', color='darkblue')
ax.axhline(y=0.85, color='red', linestyle=':', label='Umbral 85%')
ax.set_xticks(range(1, len(var_explicada) + 1))
ax.set_xlabel('Número de Componentes')
ax.set_ylabel('% Varianza Retenida')
ax.legend()
st.pyplot(fig)

# Visualización 2: Carga de Variables (Loadings)
st.markdown("### 🔍 2. Matriz de Loadings (Contribución de Variables)")
loadings = pd.DataFrame(pca.components_.T, columns=['CP1', 'CP2', 'CP3'], index=variables_num)
st.dataframe(loadings.round(3))

st.markdown(
    "**Interpretación de Componentes:**\n"
    "* **CP1 (Perfil de Madurez y Asistencia):** Representa de forma conjunta a la edad y a los tickets técnicos abiertos.\n"
    "* **CP2 (Eje de Intensidad de Consumo):** Dominada casi en su totalidad por los minutos mensuales."
)
