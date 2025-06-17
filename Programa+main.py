import streamlit as st
from streamlit_option_menu import option_menu
from inicio import pagina_inicio
from chat_con_datos import chat_datos
from edit_datos import editar_datos
from analizador_datos import perfiles
from visualizacion import visualizaciones
from ingenieria_de_datos import ingenieria_datos
from aprendizajes_automaticos import aprendizaje_automatico
from informaciones import informacion
from contactos import contacto
import base64

# Configuración de Página
st.set_page_config(
    page_title="Lozas_Modeler",
    page_icon="Fondo.png",
    layout="wide",
)

# Variables de estado y funciones de autenticación
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""
if "contraseña" not in st.session_state:
    st.session_state["contraseña"] = ""

def cred_ingresada():
    st.session_state["autenticado"] = (st.session_state["usuario"].strip() == "joker" and st.session_state["contraseña"].strip() == "joker")


def autenticacion_usuario():
    if not st.session_state["autenticado"]:
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image('Fondo.png')
            st.write("<h1 style='text-align: center; color: #3045ffff;'>Bienvenido a la Plataforma    </h1>", unsafe_allow_html=True)
            usuario_input = st.text_input(label="Usuario :", value="", key="usuario")
            contrasena_input = st.text_input(label="Contraseña :", value="", key="contraseña", type="password")
            if st.button("Entrar", key="boton_entrar", help="Ingresar al sistema", type='primary', on_click=cred_ingresada):
                cred_ingresada()
                if not st.session_state["autenticado"]:
                    st.error("Usuario o contraseña inválido.")
        
        for col in [col1, col3]:
            if not usuario_input or not contrasena_input:
                st.empty()
            
        return False
    else:
        return True


# Función principal para renderizar las páginas
def main():

    with st.sidebar:

        # Ruta de la imagen a usar como fondo de sidebar
        imagen_fondo = 'slider-fondo.jpg'

        # Leer la imagen y codificarla en base64
        with open(imagen_fondo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # Aplicar el estilo CSS para la barra lateral con la imagen de fondo
        estilo_sidebar = f"""
            <style>
            [data-testid="stSidebar"] {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
            }}
            [data-testid="stSidebar"] .st-emotion-cache-1cypcdb {{
                color: white !important;
            }}
            [data-testid="stSidebar"] .st-emotion-cache-1oe5cao {{
                color: white !important;
            }}
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
                color: white !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="tab-list"] button[data-baseweb="tab"] {{
                color: white !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="tab-list"] button[data-baseweb="tab"][aria-selected="true"] {{
                background-color: white !important;
                color: black !important;
            }}
            </style>
            """

        # Usar el decorador markdown para aplicar el estilo
        st.markdown(estilo_sidebar, unsafe_allow_html=True)

        pages = ["Inicio", "Editor", "Chat", "Visualizador", "Analizador", "Ingeniería", "Aprendizaje Automático", "Información", "Contacto"]
        nav_tab_op = option_menu(
            menu_title="Menú", 
            options=pages,
            icons=['house', 'pencil-square', 'chat', 'bar-chart-line', 'file-earmark-bar-graph', 'tools', 'robot', 'info-circle', 'envelope'],
            menu_icon="cast", 
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#7586fbff"},
                "icon": {"color": "#eeece1ff", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "color": "#eeece1ff", "--hover-color": "#0166FF"},
                "nav-link-selected": {"background-color": "#5265fdff"},
            }
        )
        # Botón para cerrar la sesión
        if st.button("Salir", type='primary'):
            st.session_state.clear()
            st.rerun()


    if autenticacion_usuario(): 
        if nav_tab_op == "Inicio":
            pagina_inicio()
        elif nav_tab_op == "Editor":
            editar_datos()
        elif nav_tab_op == "Chat":
            chat_datos()
        elif nav_tab_op == "Visualizador":
            visualizaciones()
        elif nav_tab_op == "Analizador":
            perfiles()
        elif nav_tab_op == "Ingeniería":
            ingenieria_datos()
        elif nav_tab_op == "Aprendizaje Automático":
            aprendizaje_automatico()
        elif nav_tab_op == "Información":
            informacion()
        elif nav_tab_op == "Contacto":
            contacto()


if __name__ == "__main__":
    main()
