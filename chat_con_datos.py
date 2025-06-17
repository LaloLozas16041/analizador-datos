import streamlit as st
import os
import google.generativeai as genai
import pandas as pd
import json
import plotly.express as px
from pycaret.datasets import get_data
from dotenv import load_dotenv
import plotly.graph_objects as go

load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = "AIzaSyA8pv75KBG6auxNGZEIORR9FCwEN948REc"
# Configurar GenAI con la API Key
genai.configure(api_key=GOOGLE_API_KEY)

def chat_datos():
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.error("Por favor, proporciona los datos para continuar.")
        return

    st.write("<h1 style='text-align: center; color: #0166FF;'>Chat con Datos</h1>", unsafe_allow_html=True)
    st.empty()
    st.markdown("###### Este Chat te permite interactuar de manera personalizada con tus datos.")
    st.empty()

    if st.session_state.df is not None:
        df = st.session_state.df
        st.write("**Datos:**")
        st.dataframe(df)

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "asistente", "content": "Hola, ¿en qué puedo ayudarte?"}]
        
        if st.session_state.get("messages"):
            messages = st.session_state["messages"]
        else:
            messages = []

        for msg in messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if user_query := st.chat_input():
            st.chat_message("usuario").write(user_query)
            system_instruction = f"Analizar estos datos: {df} \n\nPregunta: {user_query}"
            model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=system_instruction)
            prompt = (f"Si la respuesta requiere generar código, inclúyelo en la respuesta. "
                      f"Formatea el código en un objeto JSON bajo la clave 'code' y la respuesta de texto bajo la clave 'answer'. Por ejemplo, si el usuario pregunta "
                      f"cómo graficar un diagrama de barras para la columna A, la salida JSON debe incluir el código necesario de pandas "
                      f"sin declaraciones de impresión, así: dict('code': 'código de pandas aquí'). Si no se genera código, devuelve un objeto JSON dict('answer': 'respuesta generada','code':''). Utiliza Plotly para cualquier "
                      f"visualización y asígnalo a fig. Todos los gráficos deben mostrarse en pestañas de streamlit sin necesidad de configurar páginas ni barras laterales."
                      f"No es necesario incluir lecturas de datos de archivos ya que los datos están disponibles como df."
                      f"Asegúrate de que el código funcione correctamente")
            response = model.generate_content(prompt,
                                              generation_config=genai.GenerationConfig(
                                                  response_mime_type="application/json",
                                                  temperature=0.3,
                                              ),
                                              safety_settings={
                                                  'HATE': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
                                                  'HARASSMENT': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
                                                  'SEXUAL': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED',
                                                  'DANGEROUS': 'HARM_BLOCK_THRESHOLD_UNSPECIFIED'
                                              }
                                              )

            try:
                answer = json.loads(response.text)["answer"]
                code = json.loads(response.text)['code']
                if answer:
                    st.chat_message("asistente").write(answer)
                    st.session_state["messages"].append({"role": "asistente", "content": answer})
                if code:
                    st.code(code)
                    try:
                        exec(code)
                    except:
                        st.empty()
                if not answer and not code:
                    try:
                        search_string = '{"answer": "'
                        start_index = response.text.find(search_string)

                        if start_index != -1:
                            # Extraer la información después de search_string
                            result = response.text[start_index + len(search_string):]
                            st.chat_message("asistente").write(result)
                            st.session_state["messages"].append({"role": "asistente", "content": result})
                    except:
                        st.empty()
            except Exception as e:
                st.error(f"Lo siento, no se generó información. Por favor, inténtalo de nuevo o reformula tu pregunta: {str(e)}")
                st.write(response.candidates[0].safety_ratings)