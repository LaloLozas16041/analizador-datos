from autoviz.AutoViz_Class import AutoViz_Class
import streamlit as st
import tempfile
import os

def visualizaciones_auto():
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, proporciona los datos para proceder.")
        return
    df = st.session_state.df

    # Inicializar AutoViz
    AV = AutoViz_Class()

    # Aplicaci�n de Streamlit

    formato_grafico = st.selectbox("Elija el formato del gráfico", ["html", "svg"])
    
    # Usar un directorio temporal para guardar las salidas de AutoViz
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generar visualizaciones de AutoViz
        st.write("Generando Visualizaciones...")
        try:
            av_html = AV.AutoViz(
                filename="",
                dfte=df,
                depVar='',
                verbose=2,  # Establecer verbose en un nivel m�s alto para m�s informaci�n de depuraci�n
                lowess=False,
                chart_format=formato_grafico,  # Establecer el formato del gr�fico a 'svg'
                save_plot_dir=temp_dir
            )
        except Exception as e:
            st.error(f"Error al generar visualizaciones: {e}")
            st.error("Por favor, intenta usar un método de visualización diferente.")

        # Verificar si se generaron archivos SVG en el directorio anidado
        nested_dir = os.path.join(temp_dir, "AutoViz")
        if not os.path.exists(nested_dir):
            st.write("El directorio de salida no existe.")
        else:
            formato_grafico_fm = "." + formato_grafico
            v_files = [os.path.join(nested_dir, f) for f in os.listdir(nested_dir) if f.endswith(formato_grafico_fm)]
            if not v_files:
                st.write("No se generaron archivos " + formato_grafico)
            else:
                st.write(f"Se encontraron {len(v_files)} archivos {formato_grafico}.")
                st.write(" ")
                # Mostrar archivos SVG generados por AutoViz
                for file_path in v_files:
                    file_name = os.path.basename(file_path)
                    st.write("###", file_name)
                    with open(file_path, "r", encoding='utf-8') as f:
                        content = f.read()
                        etiqueta = "Descargar " + formato_grafico
                        if formato_grafico == 'html':
                            mime = "text/html"
                        else:
                            mime = "image/svg+xml"
                        st.download_button(
                            label=etiqueta,
                            data=content,
                            file_name=os.path.basename(file_path),
                            mime=mime
                        )
                        st.components.v1.html(content, height=600, scrolling=True)
