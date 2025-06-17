import streamlit as st
from streamlit_option_menu import option_menu

def eliminar_columnas(dataframe, columnas_a_eliminar):
    return dataframe.drop(columns=columnas_a_eliminar, axis=1)

def actualizar(edf):
    edf.to_csv('datos_actualizados.csv', index=False)
    # load_df.clear()

def editar_tabla(df):
    try:
        edf = st.data_editor(df, num_rows="dynamic", hide_index=False)
    except Exception as e:
        st.error(str(e))
    boton_guardar = st.button('Guardar')
    if boton_guardar:
        st.session_state.df = edf

def editar_datos():
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, proporciona los datos para continuar.")
        return
    df = st.session_state.df
    st.write("<h1 style='text-align: center; color: #0166FF;'>Editor de Datos</h1>", unsafe_allow_html=True)
    st.write("**El Editor de Datos proporciona dos funcionalidades principales para ayudarte a gestionar y refinar tu conjunto de datos.**")
    st.markdown("""
    1. **Editar Tabla**: En esta pestaña, puedes interactuar directamente con tu conjunto de datos utilizando 
    el Editor de Datos. Esto permite:
        - Ver tu conjunto de datos en formato tabular.
        - Realizar cambios directamente en celdas individuales.
        - Agregar o eliminar filas según sea necesario.
          - **Agregar nueva fila**: Ve al extremo inferior de la tabla y haz clic en el símbolo "+".
          - **Eliminar fila**: Selecciona las filas desde el extremo izquierdo (primera columna) y luego haz clic en el símbolo de basurero sobre la tabla.
        - Guardar tus cambios para análisis posteriores.
    2. **Eliminar Columnas**: En esta pestaña, tienes la capacidad de eliminar columnas no deseadas de tu conjunto de datos.
    (Si necesitas agregar nuevas columnas, ve a la pestaña de Ingeniería de Datos y luego a la pestaña de Creación de Características).
    """)
    st.write(" ")
    paginas = ["Editar Tabla", "Eliminar columna"]
    opcion_tabla_editar = option_menu(
        menu_title="Editar",
        options=paginas,
        icons=['pencil-square', 'trash'],
        menu_icon="list",
        default_index=0,
        orientation='horizontal',
    )
    if opcion_tabla_editar == "Editar Tabla":
        editar_tabla(df)
    elif opcion_tabla_editar == "Eliminar columna":
        # Multiselecci�n para elegir columnas a eliminar
        columnas_a_eliminar = st.multiselect("Selecciona las columnas a eliminar", df.columns)

        # Bot�n para eliminar
        if st.button("Eliminar Columnas"):
            if columnas_a_eliminar:
                try:
                    # Eliminar las columnas seleccionadas
                    df = eliminar_columnas(df, columnas_a_eliminar)
                    st.success(f"¡Columnas {columnas_a_eliminar} eliminadas exitosamente!")
                    # Mostrar el dataframe actualizado
                    st.session_state.df = df
                    st.write("Dataframe Actualizado:")
                    st.dataframe(df)
                except Exception as e:
                    st.error(str(e))
            else:
                st.warning("No se han seleccionado columnas para eliminar")