import streamlit as st
import pandas as pd
import numpy as np

def crear_caracteristica_personalizada():

    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state:
        st.session_state.df = None

    datos = st.session_state.df

    st.write("**Datos:**")
    st.write(datos)

    # Opciones de Ingeniera de Caractersticas
    st.write("**Selecciona las características y operaciones para crear características personalizadas:**")

    nuevas_caracteristicas = []

    # Operaciones matemticas entre columnas
    if st.checkbox("Agregar nueva característica por operaciones matemáticas entre columnas"):
        st.subheader("Operaciones Matemáticas")
        caracteristica1 = st.selectbox("Seleccionar primera característica", datos.select_dtypes(include=[np.number]).columns)
        operacion = st.selectbox("Seleccionar operación", ['+', '-', '*', '/'])
        caracteristica2 = st.selectbox("Seleccionar segunda característica", datos.select_dtypes(include=[np.number]).columns)
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva característica")

        if st.button("Crear Característica"):
            try:
                if operacion == '+':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica1] + datos[caracteristica2]
                elif operacion == '-':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica1] - datos[caracteristica2]
                elif operacion == '*':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica1] * datos[caracteristica2]
                elif operacion == '/':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica1] / datos[caracteristica2]

                st.write(f"Se creó la característica '{nombre_nueva_caracteristica}'")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al crear la característica: {e}")

    # Operaciones matemticas con constantes
    if st.checkbox("Agregar nueva caracterstica por operaciones matemáticas con constantes"):
        st.subheader("Operaciones Matemáticas con Constantes")
        caracteristica = st.selectbox("Seleccionar característica", datos.select_dtypes(include=[np.number]).columns, key="ops_matematicas_caracteristica")
        operacion = st.selectbox("Seleccionar operación", ['+', '-', '*', '/'], key="ops_matematicas_operacion")
        constante = st.number_input("Ingresar valor constante", value=1.0, key="ops_matematicas_constante")
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva caracterstica para la operación con constante", key="ops_matematicas_nombre_nueva_caracteristica")

        if st.button("Crear Característica con Constante"):
            try:
                if operacion == '+':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica] + constante
                elif operacion == '-':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica] - constante
                elif operacion == '*':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica] * constante
                elif operacion == '/':
                    datos[nombre_nueva_caracteristica] = datos[caracteristica] / constante

                st.write(f"Se creó la característica '{nombre_nueva_caracteristica}' con operación constante")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al crear la característica con constante: {e}")

    # Transformaciones logartmicas, raz cuadrada, exponencial
    if st.checkbox("Agregar nueva característica por transformaciones"):
        st.subheader("Transformaciones")
        caracteristica = st.selectbox("Seleccionar caracterstica para la transformación", datos.select_dtypes(include=[np.number]).columns)
        transformacion = st.selectbox("Seleccionar transformación", ['log', 'sqrt', 'exp'])
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva característica para la transformación")

        if st.button("Crear Caracterstica Transformada"):
            try:
                if transformacion == 'log':
                    datos[nombre_nueva_caracteristica] = np.log(datos[caracteristica])
                elif transformacion == 'sqrt':
                    datos[nombre_nueva_caracteristica] = np.sqrt(datos[caracteristica])
                elif transformacion == 'exp':
                    datos[nombre_nueva_caracteristica] = np.exp(datos[caracteristica])

                st.write(f"Se creó la característica '{nombre_nueva_caracteristica}' con transformación")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al crear la característica transformada: {e}")

    # Binning
    if st.checkbox("Agregar nueva caracterstica por binning"):
        st.subheader("Binning")
        caracteristica = st.selectbox("Seleccionar característica para binning", datos.select_dtypes(include=[np.number]).columns)
        bins = st.slider("Número de bins", min_value=2, max_value=10, value=5)
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva caracterstica binneada")

        if st.button("Crear Caracterstica Binneda"):
            try:
                datos[nombre_nueva_caracteristica] = pd.cut(datos[caracteristica], bins)
                st.write(f"Se creó la caracterstica binneda '{nombre_nueva_caracteristica}'")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al crear la característica binneda: {e}")

    # Caractersticas polinomiales
    if st.checkbox("Agregar características polinomiales"):
        st.subheader("Caractersticas Polinomiales")
        caracteristica = st.selectbox("Seleccionar característica para transformación polinomial", datos.select_dtypes(include=[np.number]).columns)
        grado = st.slider("Grado del polinomio", min_value=2, max_value=5, value=2)
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva característica polinomial")

        if st.button("Crear Característica Polinomial"):
            try:
                datos[nombre_nueva_caracteristica] = datos[caracteristica] ** grado
                st.write(f"Se creó la característica polinomial '{nombre_nueva_caracteristica}' con grado {grado}")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al crear la característica polinomial: {e}")

    # Contaminar columnas de objeto
    if st.checkbox("Contaminar columnas de objeto"):
        st.subheader("Contaminar Columnas de Objeto")
        caracteristica = st.selectbox("Seleccionar columna de objeto para contaminar", datos.select_dtypes(include=['object']).columns)
        contaminacion = st.text_input("Ingresar cadena de contaminacin")
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva caracterstica para la columna contaminada")

        if st.button("Contaminar Columna"):
            try:
                datos[nombre_nueva_caracteristica] = datos[caracteristica] + contaminacion
                st.write(f"Columna contaminada '{nombre_nueva_caracteristica}' con cadena '{contaminacion}'")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al contaminar columna: {e}")

    # Concatenar columnas de objeto
    if st.checkbox("Concatenar dos columnas de objeto"):
        st.subheader("Concatenar Columnas de Objeto")
        caracteristica1 = st.selectbox("Seleccionar primera columna de objeto", datos.select_dtypes(include=['object']).columns)
        caracteristica2 = st.selectbox("Seleccionar segunda columna de objeto", datos.select_dtypes(include=['object']).columns)
        separador = st.text_input("Separador", value="")
        nombre_nueva_caracteristica = st.text_input("Nombre de la nueva característica concatenada")

        if st.button("Concatenar Columnas"):
            try:
                datos[nombre_nueva_caracteristica] = datos[caracteristica1].astype(str) + separador + datos[caracteristica2].astype(str)
                st.write(f"Se concatenaron las columnas '{caracteristica1}' y '{caracteristica2}' en '{nombre_nueva_caracteristica}' con separador '{separador}'")
                st.session_state.df = datos
                st.dataframe(st.session_state.df)
                nuevas_caracteristicas.append(nombre_nueva_caracteristica)
            except Exception as e:
                st.error(f"Error al concatenar columnas: {e}")

    st.write(nuevas_caracteristicas)