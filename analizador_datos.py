import streamlit as st
import subprocess
import os
from streamlit.components.v1 import html

def perfiles():
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, carga un dataset para poder analizarlo")
        return

    st.title("📊 Análisis exploratorio de los datos")

    df_path = "temp_data.csv"
    html_output = "temp_profile.html"

    # Guardar el dataframe como CSV temporal
    st.session_state.df.to_csv(df_path, index=False)

    with st.spinner("Se está generando el reporte..."):

        # Ejecutar script externo de profiling
        subprocess.run([
            r"venv_perfilador\Scripts\python.exe",  # Ruta al Python del entorno externo
            "perfilador_externo.py", df_path, html_output
        ], check=True)


        # Leer HTML generado y embeberlo
        with open(html_output, "r", encoding="utf-8") as f:
            report_html = f.read()

        html(report_html, height=1000, scrolling=True)

    # Limpiar archivos temporales si quieres
    os.remove(df_path)
    os.remove(html_output)
