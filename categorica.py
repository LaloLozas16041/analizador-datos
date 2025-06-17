import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import category_encoders as ce
from category_encoders import TargetEncoder

def one_hot_encoding(data):
    one_hot_encoder = OneHotEncoder(drop='first', sparse=False)
    encoded_data = one_hot_encoder.fit_transform(data)
    feature_names = one_hot_encoder.get_feature_names_out(data.columns)
    encoded_df = pd.DataFrame(encoded_data, columns=feature_names)
    return encoded_df

def label_encoding(data):
    label_encoder = LabelEncoder()
    encoded_data = data.copy()
    for col in data.columns:
        encoded_data[col] = label_encoder.fit_transform(data[col])
    return encoded_data

def ordinal_encoding(data, ordering):
    encoder = OrdinalEncoder(categories=ordering)
    encoded_data = encoder.fit_transform(data)
    encoded_data = pd.DataFrame(encoded_data, columns=data.columns)
    return encoded_data

def target_encoding(data, target):
    target_encoder = TargetEncoder()
    encoded_data = data.copy()
    encoded_data = target_encoder.fit_transform(data, target)
    return encoded_data

def frequency_encoding(data):
    encoded_data = data.copy()
    for col in data.columns:
        freq = data[col].value_counts(normalize=True)
        encoded_data[col] = data[col].map(freq)
    return encoded_data

def encode_data(data, column, technique, n_features, target, ordered_list):
    encoded_data = data.copy()
    if technique == "Label Encoding":
        encoded_data = label_encoding(data[column])
    elif technique == "One-Hot Encoding":
        encoded_data  = one_hot_encoding(data[column])
    elif technique == "Ordinal Encoding":
        encoded_data = ordinal_encoding(data[column], ordered_list)
    elif technique == "Binary Encoding":
        encoder = ce.BinaryEncoder()
        encoded_data = encoder.fit_transform(data[column])
    elif technique == "Target Encoding":
        encoded_data = target_encoding(data[column], data[target])
    elif technique == "Frequency Encoding":
        encoded_data = frequency_encoding(data[column])
    return encoded_data

def codificacion_categorica():
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state:
        st.session_state.df = None

    datos = st.session_state.df
    lista_ordenada = []

    st.write("**Datos:**")
    st.write(datos)

    tecnica_codificacion = st.selectbox('Selecciona la técnica de codificación:',
                                        ["One-Hot Encoding", "Label Encoding", "Ordinal Encoding", "Binary Encoding",
                                         "Target Encoding", "Frequency Encoding"])

    n_caracteristicas = 1
    objetivo = 0
    if tecnica_codificacion == "Target Encoding":
        objetivo = st.selectbox('Selecciona la columna objetivo:', datos.select_dtypes(include='number').columns)

    columna_seleccionada = st.multiselect('Selecciona la columna categórica:', datos.select_dtypes(include='object').columns)

    if tecnica_codificacion == "Ordinal Encoding":
        valores_unicos = []
        lista_ordenada = []
        st.write("Selecciona el orden de las columnas")
        for col in columna_seleccionada:
            valores_unicos.append(datos[col].unique())

        num_filas = -(-len(valores_unicos) // 3)

        for fila in range(num_filas):
            columnas = st.columns(3)
            indice_inicio = fila * 3

            for i in range(3):
                indice_columna = indice_inicio + i
                if indice_columna < len(valores_unicos):
                    with columnas[i]:
                        st.write("Columna:", columna_seleccionada[indice_columna])
                        try:
                            lista_nombres = sorted(valores_unicos[indice_columna])
                        except Exception as e:
                            st.error(str(e))
                            st.info("Asegúrate de que tus datos no contengan valores nulos.")

                        selectores = {}
                        for j in range(len(lista_nombres)):
                            clave = f'Seleccionar_{indice_columna}_{j + 1}_{fila}'
                            if clave not in selectores:
                                selectores[clave] = st.selectbox(f'Seleccionar orden {j + 1}:', lista_nombres, key=clave)

                            lista_nombres = [nombre for nombre in lista_nombres if nombre != selectores[clave]]
                        valores_ordenados = list(selectores.values())
                        lista_ordenada.append(valores_ordenados)

            st.write(lista_ordenada)

    if st.button("Codificar"):
        try:
            datos_codificados = encode_data(datos, columna_seleccionada, tecnica_codificacion, n_caracteristicas, objetivo, lista_ordenada)
        except Exception as e:
            st.error(str(e))
            st.info("Aseg�rate de que tus datos no contengan valores nulos.")

        st.write('Datos Codificados:')
        st.write(datos_codificados)
        if tecnica_codificacion in ["One-Hot Encoding", "Binary Encoding", "Hashing Encoder"]:
            datos_codificados_finales = pd.concat([datos, datos_codificados], axis=1)
            datos_codificados_finales.drop(columns=columna_seleccionada, inplace=True, axis=1)
        else:
            datos.drop(columns=columna_seleccionada, inplace=True, axis=1)
            datos_codificados_finales = pd.concat([datos, datos_codificados], axis=1)
        st.dataframe(datos_codificados_finales)
        st.session_state.df = datos_codificados_finales