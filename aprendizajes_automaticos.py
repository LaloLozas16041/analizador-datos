import pandas as pd
import streamlit as st
from modelo_clasificacion import clasificacion
from modelo_regresion import regresion
from clustering_pycaret import clusteringPycaret
from series_de_tiempo import series_temporales_pycaret
from anomaly_pycaret import anomalyPycaret

@st.cache_data
def cargar_datos():
    if 'df' in st.session_state:
        return st.session_state.df
        
def aprendizaje_automatico():
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, proporciona los datos para continuar.")
        return
    st.write("<h1 style='text-align: center; color: #3045ffff;'>Aprendizaje Automático</h1>", unsafe_allow_html=True)
    st.markdown("""
    **Automatiza tu flujo de trabajo de aprendizaje automático.**
    """)
    
    conjunto_datos = cargar_datos()

    if len(conjunto_datos) > 0:
        # Utilizando HTML para aplicar el estilo personalizado a la etiqueta del selectbox
        tipo_ml = st.selectbox('Selecciona el modelo de Aprendizaje Automatico a utilizar:', ["Regresión", "Clasificación", "Agrupamiento", "Detección de Anomalías", "Series Temporales"])

        if tipo_ml == "Clasificación":
            clasificacion()
        elif tipo_ml == "Regresión":
            regresion()
        elif tipo_ml == "Agrupamiento":
            clusteringPycaret()
        elif tipo_ml == "Series Temporales":
            series_temporales_pycaret()
        elif tipo_ml == "Detección de Anomalías":
            anomalyPycaret()
    else:
        st.error("Por favor, proporciona los datos para continuar.")
