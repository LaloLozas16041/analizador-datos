import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, Normalizer


# Funcin para realizar la normalizacin de datos segn la tcnica seleccionada
def normalizar_datos(data, columnas_a_normalizar, tecnica):
    columnas_numericas = data.select_dtypes(include=['number']).columns
    columnas_a_normalizar = [col for col in columnas_a_normalizar if col in columnas_numericas]

    if tecnica == 'Escalamiento Min-Max':
        scaler = MinMaxScaler()
    elif tecnica == 'Estandarizacin':
        scaler = StandardScaler()
    elif tecnica == 'Escalamiento Robusto':
        scaler = RobustScaler()
    elif tecnica == 'Normalizacin':
        scaler = Normalizer()
    elif tecnica == 'Transformacin Logartmica':
        data[columnas_a_normalizar] = data[columnas_a_normalizar].apply(lambda x: np.log1p(x))
        return data
    else:
        return data

    data[columnas_a_normalizar] = scaler.fit_transform(data[columnas_a_normalizar])
    return data


def normalizacion_de_datos():
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state:
        st.session_state.df = None

    data = st.session_state.df

    st.write("**Datos:**")
    st.dataframe(data)

    # Seleccin de columnas para normalizacin
    columnas_numericas = data.select_dtypes(include=['number']).columns
    columnas_a_normalizar = st.multiselect("Selecciona las columnas a normalizar:", columnas_numericas)

    # Seleccin de tcnica de normalización
    tecnicas = ['Escalamiento Min-Max', 'Estandarización', 'Escalamiento Robusto', 'Normalización', 'Transformacin Logarítmica']
    tecnica = st.selectbox("Selecciona la técnica de normalización:", tecnicas)

    # Realizar la normalizacin y mostrar resultados
    if st.button("Normalizar Datos"):
        try:
            datos_normalizados = normalizar_datos(data.copy(), columnas_a_normalizar, tecnica)
            st.session_state.df = datos_normalizados
            st.write("Datos Normalizados:")
            st.dataframe(st.session_state.df)
        except ValueError as e:
            st.error(str(e))