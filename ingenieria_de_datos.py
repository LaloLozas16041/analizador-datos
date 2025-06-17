import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from sklearn.impute import SimpleImputer, KNNImputer
import numpy as np
from manejo_atipico import outlier_detection_handling
from categorica import codificacion_categorica
from datos_normalizados import normalizacion_de_datos
from creacion_de_caracteristicas import crear_caracteristica_personalizada

# Función para realizar la imputación de datos
def imputar_datos(data, nombre_columna, metodo_imputacion, n_vecino, valor_constante):
    if metodo_imputacion == 'siguiente':
        st.write("Llenar valores propagando la óltima observación válida a la siguiente válida.")
        data[nombre_columna] = data[nombre_columna].fillna(method='ffill')
    elif metodo_imputacion == 'anterior':
        data[nombre_columna] = data[nombre_columna].fillna(method='bfill')
    elif metodo_imputacion == 'knn':
        knn_imputer = KNNImputer(n_neighbors=n_vecino)
        data[nombre_columna] = knn_imputer.fit_transform(data[[nombre_columna]])
    elif metodo_imputacion == 'máximo':
        data[nombre_columna] = data[nombre_columna].fillna(data[nombre_columna].max())
    elif metodo_imputacion == 'mínimo':
        data[nombre_columna] = data[nombre_columna].fillna(data[nombre_columna].min())
    elif metodo_imputacion == 'más_frecuente':
        data[nombre_columna] = data[nombre_columna].fillna(data[nombre_columna].mode().iloc[0])
    elif metodo_imputacion == 'media':
        data[nombre_columna] = data[nombre_columna].fillna(data[nombre_columna].mean())
    elif metodo_imputacion == 'mediana':
        data[nombre_columna] = data[nombre_columna].fillna(data[nombre_columna].median())
    elif metodo_imputacion == 'constante':
        data[nombre_columna] = data[nombre_columna].fillna(valor_constante)
    elif metodo_imputacion == 'aleatorio':
        data[nombre_columna] = data[nombre_columna].apply(lambda x: np.random.choice(data[nombre_columna].dropna()) if pd.isnull(x) else x)
    elif metodo_imputacion == 'interpolación':
        data[nombre_columna] = data[nombre_columna].interpolate(method='linear', limit_direction='both')
    elif metodo_imputacion == 'extrapolación':
        data[nombre_columna] = data[nombre_columna].interpolate(method='linear', limit_direction='forward')
    elif metodo_imputacion == 'Eliminar columna seleccionada':
        data.drop(columns=[nombre_columna], inplace=True)
    elif metodo_imputacion == 'Eliminar filas con valores nulos':
        data = data.dropna(axis=0, subset=[nombre_columna])
        data = data.reset_index(drop=True)
    else:
        st.warning(f"Método de imputación no soportado: {metodo_imputacion}")

    return data

# Aplicación Streamlit
def pestana_imputacion():
    if st.session_state.df is not None:
        st.write("**1. Seleccionar Columna:**")
        nombre_columna = st.selectbox("Selecciona una columna para imputación", st.session_state.df.columns)

        st.write(f"**2. Número de Valores Faltantes en {nombre_columna}:**")
        cantidad_valores_faltantes = st.session_state.df[nombre_columna].isnull().sum()
        st.write(f"Hay {cantidad_valores_faltantes} valores faltantes en la columna seleccionada.")

        st.write("**3. Seleccionar Mtodo de Imputacin:**")
        tipo_dato_columna = str(st.session_state.df[nombre_columna].dtype)
        metodos_imputacion = {
            'int64': ['media', 'mediana', 'constante', 'más_frecuente', 'aleatorio', 'interpolación', 'extrapolación', 'mínimo',
                      'máximo' , 'anterior','siguiente','knn','Eliminar columna seleccionada','Eliminar filas con valores nulos'],
            'float64': ['media', 'mediana', 'constante', 'más_frecuente', 'aleatorio', 'interpolación', 'extrapolación', 'mínimo',
                        'máximo' , 'anterior','siguiente','knn','Eliminar columna seleccionada','Eliminar filas con valores nulos'],
            'object': ['más_frecuente', 'constante', 'aleatorio','anterior','siguiente','Eliminar columna seleccionada',
                       'Eliminar filas con valores nulos' ],
            'datetime64[ns]': ['mas_frecuente', 'constante', 'aleatorio','anterior','siguiente','Eliminar columna seleccionada',
                               'Eliminar filas con valores nulos' ]
        }

        if tipo_dato_columna in metodos_imputacion:
            metodo_imputacion = st.selectbox("Selecciona el método de imputación", metodos_imputacion[tipo_dato_columna])
        else:
            st.warning("No hay método de imputación disponible para el tipo de dato seleccionado.")

        if metodo_imputacion == 'knn':
            n_vecino = st.number_input("Selecciona el número de vecinos para KNN", value=2, step=1)
        else:
            n_vecino = 2

        valor_constante = None  # Inicializar valor_constante con un valor predeterminado
        if metodo_imputacion == 'constante':
            if st.session_state.df[nombre_columna].dtype in ['float64', 'int64']:
                valor_constante = st.number_input("Ingresa un valor constante")
            else:
                valor_constante = st.text_input("Ingresa un valor constante")

        st.write("**4. Imputar Datos:**")
        if st.button("Imputar Datos"):
            st.session_state.df = imputar_datos(st.session_state.df, nombre_columna, metodo_imputacion, n_vecino, valor_constante)
            st.success("Datos imputados exitosamente!")

        st.write("**5. Mostrar Datos después de la Imputación:**")
        st.dataframe(st.session_state.df)

def cambiar_tipo_dato():
    df_copia = st.session_state.df.copy()
    tipos_datos_df = pd.DataFrame(st.session_state.df.dtypes, columns=['Tipo de Dato']).reset_index()

    columna = st.selectbox("Selecciona una columna", st.session_state.df.columns, key="seleccion_columna")
    nuevo_tipo = st.selectbox("Selecciona un nuevo tipo de dato", ["float", "int", "object", "bool", "datetime64[ns]"],
                            key="seleccion_tipo")

    if st.button('Cambiar Tipo de Dato'):
        if nuevo_tipo == "object":
                # Manejar caso donde el usuario elige tipo 'object'
                st.warning("Cambiar a tipo 'object' puede resultar en prdida de información numérica.")
                st.session_state.df[columna] = st.session_state.df[columna].astype(nuevo_tipo)

        elif nuevo_tipo == "float" or nuevo_tipo == "int":
            # Manejar conversión para números con comas
            try:
                st.session_state.df[columna] = st.session_state.df[columna].replace(',', '', regex=True).astype(nuevo_tipo)
                st.success(f"Columna {columna} convertida a {nuevo_tipo}")
            except Exception as e:
                st.error(f"Error cambiando tipo de dato: {e}")

        elif nuevo_tipo == "datetime64[ns]":
            # df_copia = st.session_state.df.copy()
            try:
                st.session_state.df[columna] = pd.to_datetime(st.session_state.df[columna], errors='coerce')
                st.success(f"Columna {columna} convertida a {nuevo_tipo}")

            except Exception as e:
                st.error(f"Error cambiando tipo de dato: {e}")

    col1,col2 = st.columns(2)
    with col1:
        st.write("Tipos de Datos Actuales:")
        st.write(df_copia.dtypes)
    with col2:
        st.write("Tipos de Datos Actualizados:")
        st.write(st.session_state.df.dtypes)

def eliminar_duplicados():
    num_duplicados = st.session_state.df.duplicated().sum()
    st.write(f"Número total de filas duplicadas en los datos: ",num_duplicados)
    if num_duplicados > 0:
        st.write("Deseas eliminar estas filas duplicadas?")
        if st.button("Eliminar Duplicados"):
            st.session_state.df = st.session_state.df.drop_duplicates()
            st.write("Se han eliminado las filas duplicadas. Aquí tienes un resumen de los datos limpios:")
            st.dataframe(st.session_state.df.describe())
            return st.session_state.df

def ingenieria_datos():
    # Inicializar variables de estado de sesión si no existen
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, proporciona los datos para continuar.")
        return
    st.write("<h1 style='text-align: center; color: #0166FF;'>Ingeniera de Datos</h1>", unsafe_allow_html=True)
    st.markdown("""
    **Mejora tu conjunto de datos con diversas transformaciones utilizando las siguientes pestaas:**

    - **Cambiar tipo de dato**: Modifica los tipos de datos de las columnas segn tus necesidades de anlisis.
    - **Eliminar duplicados**: Elimina filas duplicadas de tu conjunto de datos para obtener datos ms limpios.
    - **Imputación**: Rellena los valores faltantes utilizando estrategias adecuadas.
    - **Manejo de valores atípicos**: Aborda los valores atpicos en tus datos para mejorar el rendimiento del modelo.
    - **Codificacin de datos categricos**: Codifica variables categricas para algoritmos de aprendizaje automtico.
    - **Normalizacin de datos**: Escala los datos numricos a un rango estndar para un mejor rendimiento del modelo.
    - **Creacin de caractersticas**: Genera nuevas caractersticas derivadas de las existentes para capturar ms informacin.

    Explora cada pestaa para preprocesar tus datos de manera efectiva para el análisis y modelado.
    """)
    st.write("")
    # Definir navegación entre pestañas
    paginas = ["Cambiar tipo de dato", "Eliminar duplicados", "Imputacion", "Manejo de valores atipicos", "Codificación de datos categoricos",
             "Normalizacion de datos", "Creacion de caracteristicas"]

    opcion_seleccionada = option_menu(
        menu_title="",
        options=paginas,
        orientation='horizontal',
    )

    if opcion_seleccionada == "Cambiar tipo de dato":
        cambiar_tipo_dato()
    elif opcion_seleccionada == "Eliminar duplicados":
        eliminar_duplicados()
    elif opcion_seleccionada == "Imputacion":
        pestana_imputacion()
    elif opcion_seleccionada == "Manejo de valores atipicos":
        outlier_detection_handling()
    elif opcion_seleccionada == "Codificacion de datos categoricos":
        codificacion_categorica()
    elif opcion_seleccionada == "Normalizacion de datos":
        normalizacion_de_datos()
    elif opcion_seleccionada == "Creacion de caracteristicas":
        crear_caracteristica_personalizada()

if __name__ == "__main__":
    ingenieria_datos()