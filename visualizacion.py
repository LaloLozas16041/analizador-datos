import streamlit as st
from streamlit_option_menu import option_menu
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit.components.v1 as components
from autovisualizador import visualizaciones_auto

from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit.components.v1 as components

def explorador_pygwalker(dataset):
    try:
        init_streamlit_comm()
        html = get_streamlit_html(dataset, use_kernel_calc=True)
        components.html(html, height=1000, scrolling=True)
    except Exception as e:
        st.error(f"Error al cargar Pygwalker: {e}")

def visualizaciones():
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, proporciona los datos para continuar.")
        return

    st.write("<h1 style='text-align: center; color: #0166FF;'>Visualizador</h1>", unsafe_allow_html=True)
    st.markdown("""
    **Explora tus datos visualmente con dos herramientas poderosas.**

    **Visualización Personalizada**: Crea gráficos y diagramas personalizados.

    **Visualización Automática**: Genera automáticamente una variedad de visualizaciones analíticas de tus datos.
    """)

    dataset = st.session_state.df
    opcion_tabla_viz = option_menu(
        menu_title="Visualización",
        options=["Visualización Personalizada", "Visualización Automática"],
        orientation='horizontal',
    )
    if opcion_tabla_viz == "Visualización Automática":
        visualizaciones_auto()
    elif opcion_tabla_viz == "Visualización Personalizada":
        explorador_pygwalker(dataset)

if __name__ == "__main__":
    visualizaciones()
