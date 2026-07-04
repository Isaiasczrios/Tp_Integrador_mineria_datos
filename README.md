# 🎬 Proyecto Integrador: Análisis de Usuarios de Streaming

**Minería de Datos 1 — FCEyT — UNSE**

Análisis reproducible, trazable y estructurado sobre el perfil demográfico, hábitos de consumo e incidencias de soporte de los usuarios de una plataforma de streaming regional, con limpieza de datos basada en evidencia, análisis exploratorio (EDA), reducción de dimensionalidad (PCA) y una app interactiva en Streamlit.

## 👥 Integrantes

- Carlos Isaias Cazazola Rios
- *[Nombre del Segundo Integrante]*

**Comisión:** [Número de Comisión] · **Fecha:** Julio 2026

## 📁 Estructura del repositorio

```
tp_integrador_mineria_datos/
│
├── notebooks/
│   ├── 01_inspeccion_inicial.ipynb     # Carga y primer diagnóstico del dataset crudo
│   ├── 02_calidad_y_limpieza.ipynb     # Detección y tratamiento de inconsistencias/outliers
│   ├── 03_eda.ipynb                    # Análisis exploratorio univariado/bivariado/multivariado
│   ├── 04_pca.ipynb                    # Escalamiento Z-score y PCA
│   └── 05_conclusiones.ipynb           # Síntesis de hallazgos y limitaciones
│
├── data/
│   ├── streaming_users_dirty.json      # Dataset original, sin procesar
│   ├── streaming_users_clean.csv       # Dataset final, limpio y validado
│   └── pipeline_log.csv                # Bitácora de cada transformación aplicada (paso, filas, nulos, retención)
│
└── app/
    ├── pi_mineria_datos_1.py           # Página principal de la app Streamlit
    ├── requirements.txt                # Dependencias
    ├── streaming_users_clean.csv       # Copia del dataset limpio usada por la app
    └── pages/
        ├── 01_dataset_py.py            # Página: inspección del dataset
        ├── 02_eda_py.py                # Página: análisis exploratorio
        ├── 03_pca_py.py                # Página: PCA
        └── 04_conclusiones_py.py       # Página: conclusiones finales
```

> **Nota:** el CSV usado por la app (`app/streaming_users_clean.csv`) debe estar en la carpeta `app/`, un nivel por encima de `app/pages/`, ya que las páginas resuelven la ruta como `../streaming_users_clean.csv` respecto a su propia ubicación.

## 🧪 Metodología

1. **Inspección inicial:** carga del dataset crudo (8160 filas) y diagnóstico de tipos, nulos y rangos.
2. **Calidad y limpieza (basada en evidencia):**
   - Unificación de categorías en `subscription_plan` (variantes como *Basic*, *Std*, *Standard*, *Premiun* y mezclas de mayúsculas → *Básico*, *Estándar*, *Premium*).
   - Corrección de edades imposibles (0 años y 150 años/negativas) imputando por la moda robusta.
   - Corrección de outliers en `monthly_watch_time_mins` (valores >2000 o <0) imputando por la media.
   - Corrección del error de carga de 99 tickets en `customer_support_tickets` mediante mediana robusta.
   - Conversión de `last_login_date` a formato `datetime`.
   - Cada paso queda registrado en `pipeline_log.csv` (filas, nulos y % de retención).
3. **EDA:** distribuciones univariadas (edad, país), relaciones bivariadas (plan vs. consumo, edad vs. tickets) y multivariadas (consumo por edad condicionado por plan).
4. **PCA:** escalamiento `StandardScaler` obligatorio sobre `age`, `monthly_watch_time_mins` y `customer_support_tickets`, seguido de PCA para resumir la variabilidad en dos componentes principales.
5. **Conclusiones:** síntesis de hallazgos, impacto de la limpieza sobre el modelo y limitaciones del alcance transversal del dataset.

## 📊 Hallazgos principales

- El **Plan de Suscripción** (no la edad) es el factor determinante del consumo mensual en minutos.
- **CP1** (edad + tickets de soporte) define un perfil de "madurez y asistencia"; **CP2** aísla la intensidad de consumo (dominada por `monthly_watch_time_mins`).
- Mantener los outliers sin tratar (150 años, 99 tickets) habría distorsionado la varianza y sesgado artificialmente el PCA.

## 🚀 Cómo ejecutar la app localmente

```bash
cd app
pip install -r requirements.txt
streamlit run pi_mineria_datos_1.py
```

## ☁️ Despliegue en Streamlit Community Cloud

1. Subir el repositorio a GitHub manteniendo la estructura de carpetas indicada arriba.
2. En [share.streamlit.io](https://share.streamlit.io), crear una nueva app apuntando a:
   - **Repository:** este repositorio
   - **Main file path:** `app/pi_mineria_datos_1.py`
3. Streamlit detecta automáticamente las páginas dentro de `app/pages/`.
4. Las dependencias se instalan desde `app/requirements.txt`.

## 🛠️ Tecnologías utilizadas

- Python, pandas, numpy
- matplotlib, seaborn
- scikit-learn (`StandardScaler`, `PCA`)
- Streamlit (app interactiva multi-página)

## 🔮 Limitaciones y mejoras futuras

- El dataset es un corte transversal (no permite analizar *churn* ni estacionalidad).
- Se propone incorporar métricas de retención (CAC, churn rate) y automatizar reglas de calidad de datos en el origen (validación de esquemas/regex al registrar usuarios).

## 🔗 Enlaces

- Repositorio: [GitHub](https://github.com/)
