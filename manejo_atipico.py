import streamlit as st
import numpy as np
from scipy.stats import zscore, iqr, boxcox
from sklearn.covariance import EllipticEnvelope
from statsmodels.robust import mad
from sklearn.cluster import DBSCAN
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from streamlit_option_menu import option_menu
from scipy.stats.mstats import winsorize


def zscore_outliers(data):
    try:
        z_scores = np.abs(zscore(data))
        return np.where(z_scores > 3)[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo Z-Score,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def iqr_outliers(data):
    try:
        q1, q3 = np.percentile(data, [25, 75])
        iqr_val = q3 - q1
        lower_bound, upper_bound = q1 - 1.5 * iqr_val, q3 + 1.5 * iqr_val
        return np.where((data < lower_bound) | (data > upper_bound))[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo IQR,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def mahalanobis_outliers(data):
    try:
        clf = EllipticEnvelope(contamination=0.1)
        outliers = clf.fit_predict(data)
        return np.where(outliers == -1)[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo de Mahalanobis,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def mad_outliers(data):
    try:
        median = np.median(data)
        mad_value = mad(data)
        threshold = 3 * mad_value
        return np.where(np.abs(data - median) > threshold)[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo MAD,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def knn_outliers(data):
    try:
        clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        outliers = clf.fit_predict(data)
        return np.where(outliers == -1)[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo KNN,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def isolation_forest_outliers(data):
    try:
        clf = IsolationForest(contamination=0.1)
        outliers = clf.fit_predict(data)
        return np.where(outliers == -1)[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo de Isolation Forest,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def dbscan_outliers(data):
    try:
        dbscan = DBSCAN(eps=0.5, min_samples=5)
        data['cluster'] = dbscan.fit_predict(data.values)
        return np.where(data['cluster'] == -1)[0]
    except ValueError as e:
        msg = "Se produjo un error al aplicar el mtodo DBSCAN,\n ERROR: " + str(e)
        st.error(msg)
        st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def outlier_detection():
   
    if st.session_state.df is not None:
        cols = st.columns(2)
        outlier_method = cols[1].selectbox(
            "Selecciona el Mtodo de Deteccin de Valores Atpicos",
            ["Z-Score", "IQR", "Mahalanobis", "MAD", "DBSCAN", "KNN", "Isolation Forest"]
        )

        column_selector = cols[0].multiselect(
            "Selecciona la Columna para Deteccin de Valores Atpicos",
            st.session_state.df.select_dtypes(include=np.number).columns
        )
        st.session_state.column_selector = column_selector

        # Verifica si al menos una columna est seleccionada
        if not column_selector:
            st.info("Por favor, asegrate de seleccionar al menos una columna")
            return
        outliers = None
        error_msg = None

        if outlier_method == "Z-Score":
            outliers = zscore_outliers(st.session_state.df[column_selector])
        elif outlier_method == "IQR":
            outliers = iqr_outliers(st.session_state.df[column_selector])
        elif outlier_method == "Mahalanobis":
            outliers = mahalanobis_outliers(st.session_state.df[column_selector])
        elif outlier_method == "MAD":
            outliers = mad_outliers(st.session_state.df[column_selector])
        elif outlier_method == "DBSCAN":
            outliers = dbscan_outliers(st.session_state.df[column_selector])
        elif outlier_method == "KNN":
            outliers = knn_outliers(st.session_state.df[column_selector])
        elif outlier_method == "Isolation Forest":
            outliers = isolation_forest_outliers(st.session_state.df[column_selector])

        st.session_state.outliers = outliers

        # Muestra los valores atpicos con las columnas resaltadas
        st.subheader(f"Valores Atpicos usando {outlier_method} para {column_selector}:")
        try:
            st.write("Nmero de valores atpicos: ", len(st.session_state.outliers))

            st.dataframe(st.session_state.df.loc[outliers].style.set_properties(**{'background-color': '#00FFF6'},
                                                                                subset=column_selector))
            st.subheader("El color verde claro resalta los datos con valores atpicos.")
            st.dataframe(
                st.session_state.df.style.applymap(
                    lambda _: "background-color: #00FFF6;", subset=(outliers, slice(None))
                )
            )
        except Exception as e:
            msg = "Se produjo un error al aplicar el mtodo "+ outlier_method + ",\n ERROR: " + str(e)
            st.error(msg)
            st.info("Por favor, verifica tus datos o prueba con otro mtodo de deteccin de valores atpicos.")


def handle_outliers_tech(data, method, column_selector, outliers, min_max_list, bounds, imputation_value):
    if method == "Transformacin Logartmica":
        for column in column_selector:
            data[column], _ = boxcox(data[column])
    elif method == "Transformacin Box-Cox":
        for column in column_selector:
            data[column], fitted_lambda = boxcox(data[column])
            st.write(f"Valor de lambda utilizado para la transformacin de {column}: ", fitted_lambda)
    elif method == "Truncamiento o Capping":
        i = 0
        for column in column_selector:
            data[column] = np.clip(data[column], a_min=min_max_list[i][0], a_max=min_max_list[i][1])
            i += 1
    elif method == "Winsorizing":
        i = 0
        for column in column_selector:
            data[column] = winsorize(data[column], limits=(bounds[i][0], bounds[i][1]))
            i += 1
    elif method == "Imputacin":
        i = 0
        for col in column_selector:
            data.loc[outliers, col] = np.nan
            data[col] = data[col].fillna(imputation_value[i])
            i += 1
    elif method == "Eliminar Valores Atpicos":
        data = data.drop(outliers, axis=0).reset_index(drop=True)
    return data


def outlier_handling():
   
    if st.session_state.df is not None:
        cols = st.columns(2)
        handle_option = cols[0].selectbox("Selecciona la Tcnica de Manejo de Valores Atpicos",
                                          ["Ninguno", "Transformacin Logartmica", "Transformacin Box-Cox",
                                           "Truncamiento o Capping", "Winsorizing", "Imputacin",
                                           "Eliminar Valores Atpicos"])
        if handle_option is None:
            st.warning("Por favor, asegrate de seleccionar al menos una tcnica")

        if handle_option != "Eliminar Valores Atpicos":
            column_selector_handle = cols[1].multiselect("Selecciona la Columna para Manejo de Valores Atpicos",
                                                         st.session_state.column_selector)
        else:
            column_selector_handle = st.session_state.column_selector
        imputation_value = []
        bounds = []
        min_max_list = []
        if handle_option == "Imputacin":
            for col in column_selector_handle:
                msg = col + ": Ingresa el valor de imputacin:"
                imputation_value.append(st.number_input(msg, min_value=-1.7976931348623157e+308,
                                                        max_value=1.7976931348623157e+308))
        elif handle_option == "Truncamiento o Capping":
            for column in column_selector_handle:
                min_max = []
                min_max.append(st.number_input(f"Ingresar valor mnimo para {column}:", min_value=0.0))
                min_max.append(st.number_input(f"Ingresar valor mximo para {column}:", min_value=0.0))
                min_max_list.append(min_max)

        elif handle_option == "Winsorizing":
            for column in column_selector_handle:
                lower_upper = []
                lower_upper.append(st.number_input(f"Ingresar lmite inferior para {column}:", min_value=0.0, max_value=1.0,
                                                   key=f"Winsorizing_lower_{column}"))
                lower_upper.append(st.number_input(f"Ingresar lmite superior para {column}:", min_value=0.0, max_value=1.0,
                                                   key=f"Winsorizing_upper_{column}"))
                bounds.append(lower_upper)

        if handle_option != "Ninguno":

            if st.button("Manejar Valores Atpicos"):
                try:
                    st.session_state.df = handle_outliers_tech(st.session_state.df, handle_option,
                                                               column_selector_handle, st.session_state.outliers,
                                                               min_max_list, bounds, imputation_value)
                    outlierfix = list(set(st.session_state.outliers).intersection(st.session_state.df.index))
                    st.dataframe(
                        st.session_state.df.style.applymap(
                            lambda _: "background-color: #00FFF6;", subset=(outlierfix, slice(None))
                        )
                    )
                except Exception as e:
                    st.error(str(e))


def outlier_detection_handling():
    if 'page' not in st.session_state:
        st.session_state.page = "Inicio"
    if 'df' not in st.session_state:
        st.session_state.df = None

    # Definir navegacin entre pginas
    pages = ["Deteccin de Valores Atpicos", "Manejo de Valores Atpicos"]

    nav_tab_op = option_menu(
        menu_title="",
        options=pages,
        orientation='horizontal',
    )

    if nav_tab_op == "Deteccin de Valores Atpicos":
        outlier_detection()
    elif nav_tab_op == "Manejo de Valores Atpicos":
        outlier_handling()
