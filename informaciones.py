import streamlit as st

def informacion():
    st.write("<h1 style='text-align: center; color: #3045ffff;'>Acerca del Modelador</h1>", unsafe_allow_html=True)

    st.markdown("""
    **Esta Modelador tiene como objetivo simplificar el anlisis de datos y el proceso de aprendizaje automtico proporcionando una 
    interfaz fcil de usar por cualquier usuario.**

    ### Caractersticas clave:
    - **Manejo de datos**: Cargue archivos CSV o Excel, edite datos y realice tareas de preprocesamiento como la imputacin 
    y manejo de valores atpicos.
    - **Visualizacin y Anlisis**: Explore los datos visualmente utilizando herramientas de visualizacin y anlisis personalizadas y automatizadas.
    - **Ingeniera de Datos**: Transforme y cree nuevas funciones para mejorar el rendimiento del modelo.
    - **Aprendizaje Automtico**: Cree y compare automticamente modelos de aprendizaje automtico para regresin, clasificacin, agrupacin, 
    deteccin de anomalas y pronstico de series temporales utilizando PyCaret.

   ### Tecnologas utilizadas:
    - **[AutoViz](https://pypi.org/project/autoviz/0.0.6/)**: Proporciona la seleccin de grficos automatizada para un anlisis rpido de datos.
    - **[PyCaret](https://pycaret.org)**: Potencia las capacidades de aprendizaje automtico para la creacin y optimizacin de modelos.
    - **[pygwalker](https://kanaries.net/pygwalker)**: Permite visualizaciones de datos personalizables para obtener conocimientos ms profundos.
    - **[Streamlit](https://streamlit.io)**: Se utiliza para crear interfaces de usuario profesionales, interactivas y responsivas.
    """)

if __name__ == "__main__":
    informacion()