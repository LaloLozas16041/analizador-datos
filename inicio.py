import streamlit as st 
import pandas as pd

def cargar_y_datos_previos(): 
    cargarArchivo = st.file_uploader("Seleccionar archivo CSV o Excel:", key="file_uploader", type=["csv","xlsx"], 
                                     help="Haz clic aquí para cargar un archivo CSV o Excel")

    if cargarArchivo is not None:
        try:
            if cargarArchivo.name.endswith('.csv'):
                df = pd.read_csv(cargarArchivo)
            elif cargarArchivo.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(cargarArchivo)
          
            return df
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
    return None

def pagina_inicio():
    # Título y descripción de la APP
    st.write("<h1 style='text-align: center; color: #0166FF;'>Bienvenido a la plataforma</h1>", unsafe_allow_html=True)

    st.markdown("""
        **Esta plataforma simplifica el análisis de datos y el proceso de aprendizaje automático a través de una interfaz simple de usar. 
        Carga, edita, visualiza y analiza características fácilmente a partir de tus datos, sin necesidad de ninguna codificación. Usa de forma automatizada 
        el aprendizaje automático para crear modelos predictivos.**

        #### Características:
        - **Cargar datos:** Carga fácilmente datos en formato CSV o Excel.
        - **Chatear con datos:** DataBot te permite chatear con tus datos.
        - **Edición de datos:** Realiza cambios en tu conjunto de datos directamente desde la aplicación.
        - **Visualización de datos:** Crea visualizaciones detalladas y personalizadas para comprender mejor los datos.
        - **Análisis de datos:** Genera análisis automáticos partiendo de tus datos.
        - **Ingeniería de datos:** Ejecuta diversas técnicas de ingeniería para preparar tus datos para el modelado.
        - **Aprendizaje automático:** Utiliza el aprendizaje automático automatizado para crear modelos predictivos sin escribir una sola línea de código.
        """)
    
    st.markdown(""" 
        #### Cómo se usa: 
        1. **Carga tus datos:** Haz clic en el botón "Seleccionar archivo" para elegir un archivo en formato CSV o Excel. 
        2. **Chatea con los datos:** Escribe cualquier pregunta sobre los datos cargados. El Chat proporcionará respuestas a todas tus consultas. Si no estás satisfecho vuelva a preguntar.
        3. **Edita tus datos:** Navega a la pestaña "Editor" para hacer modificaciones en el conjunto de datos.
        4. **Visualiza los datos:** Utiliza la pestaña "Visualizador" para generar diferentes tipos de cuadros y gráficos que permitirán analizar mejor tus datos.
        5. **Analiza los datos:** Ingresa a "Analizador" para analizar profesionalmente los datos.
        6. **Ingeniería de datos:** Ve a la pestaña "Ingeniería" para crear y modificar funciones en los datos.
        7. **Aprendizaje automático:** Visita "Aprendizaje Automático" para entrenar y evaluar automáticamente modelos de aprendizaje automático.
        ---
        """)
    
    # Inicialización del estado de la sesión
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    st.session_state.df = cargar_y_datos_previos()
    
    if st.session_state.df is not None:
        st.write("**Datos:**")
        st.write(st.session_state.df)
