import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
st.title("📊 Análisis Exploratorio de Datos")

@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/processed/streaming_users_clean.csv")
    except FileNotFoundError:
        try:
            return pd.read_csv("streaming_users_clean.csv")
        except FileNotFoundError:
            try:
                return pd.read_csv("app/streaming_users_clean.csv")
            except FileNotFoundError:
                st.error("🚨 Error crítico: No se encuentra 'streaming_users_clean.csv'.")
                st.stop()

df = load_data()
sns.set_theme(style="whitegrid", palette="muted")
orden_plan = ['Básico', 'Estándar', 'Premium']
colors_plan = ['#5b9bd5', '#70ad47', '#ed7d31']

st.markdown("---")
st.markdown("## Análisis univariado")

# VIZ 1
st.markdown("### Visualización 1 — Distribución del tiempo de visualización mensual")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(df['monthly_watch_time_mins'], bins=40, color='steelblue', edgecolor='white')
med = df['monthly_watch_time_mins'].median()
axes[0].axvline(med, color='red', linestyle='--', label=f'Mediana: {med:.0f}')
axes[0].set_title('Distribución del watch time')
axes[0].set_xlabel('Minutos por mes')
axes[0].set_ylabel('Frecuencia')
axes[0].legend()
axes[1].boxplot(df['monthly_watch_time_mins'], patch_artist=True, boxprops=dict(facecolor='steelblue'))
axes[1].set_title('Boxplot del watch time')
axes[1].set_ylabel('Minutos por mes')
axes[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tight_layout()
st.pyplot(fig)
st.info("""
**Interpretación:** El tiempo de visualización tiene una distribución bimodal o asimétrica, 
con concentración de usuarios tanto en valores bajos como altos. La mediana se sitúa 
alrededor de los 800 minutos mensuales.
""")

st.markdown("---")
st.markdown("## Análisis bivariado")

# VIZ 2
st.markdown("### Visualización 2 — Relación entre plan y tiempo de visualización")
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.boxplot(x='subscription_plan', y='monthly_watch_time_mins', data=df, 
            order=orden_plan, palette=colors_plan, ax=ax2)
ax2.set_title('Watch time según plan de suscripción')
ax2.set_xlabel('Plan')
ax2.set_ylabel('Minutos por mes')
st.pyplot(fig2)
st.info("""
**Interpretación (Pregunta 1):** Sí, el plan influye. Se observa un escalonamiento claro: 
los usuarios Premium consumen más que los Estándar, y estos a su vez más que los del plan Básico.
""")

# VIZ 3
st.markdown("### Visualización 3 — Relación entre tiempo de visualización y tickets de soporte")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.boxplot(x='customer_support_tickets', y='monthly_watch_time_mins', data=df, 
            color='lightgray', ax=ax3)
ax3.set_title('Watch time vs Cantidad de tickets')
ax3.set_xlabel('Cantidad de tickets de soporte')
ax3.set_ylabel('Minutos por mes')
st.pyplot(fig3)
st.info("""
**Interpretación (Pregunta 2):** No hay relación aparente. Las medianas de consumo 
son similares sin importar si el usuario generó 0 o más tickets.
""")

st.markdown("---")
st.markdown("## Análisis multivariado")

# VIZ 4
st.markdown("### Visualización 4 — Matriz de correlación y resúmenes")
fig5, axes5 = plt.subplots(1, 3, figsize=(16, 5))
corr = df[['age', 'monthly_watch_time_mins', 'customer_support_tickets']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            ax=axes5[0], linewidths=0.5)
axes5[0].set_title('Correlaciones numéricas')
edad_plan = df.groupby('subscription_plan')['age'].mean().reindex(orden_plan)
axes5[1].bar(orden_plan, edad_plan.values, color=colors_plan, edgecolor='white')
axes5[1].set_title('Edad promedio por plan')
axes5[1].set_xlabel('Plan')
axes5[1].set_ylabel('Edad promedio')
for i, v in enumerate(edad_plan.values):
    axes5[1].text(i, v + 0.2, f'{v:.1f}', ha='center', fontweight='bold')
wt_genre = df.groupby('favorite_genre')['monthly_watch_time_mins'].mean().sort_values(ascending=False)
axes5[2].barh(wt_genre.index, wt_genre.values, color='steelblue', edgecolor='white')
axes5[2].set_title('Watch time por género favorito')
axes5[2].set_xlabel('Minutos promedio')
plt.suptitle('Análisis multivariado', fontsize=13)
plt.tight_layout()
st.pyplot(fig5)
st.info("""
**Interpretación (Pregunta 3):** Las variables numéricas tienen correlaciones lineales muy bajas entre sí. 
La edad promedio es constante (~35 años) entre los distintos planes, lo que indica que el plan 
depende de otros factores y no de la edad.
""")
