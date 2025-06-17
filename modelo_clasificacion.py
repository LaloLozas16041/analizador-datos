import streamlit as st
import pandas as pd
from pycaret.classification import setup, compare_models, predict_model, pull, plot_model,create_model,ensemble_model,blend_models,stack_models,tune_model,save_model


metrics_dict = {
    "�rea bajo la curva": 'auc',
    "Umbral de discriminaci�n": 'umbral',
    "Curva de recuperaci�n de precisi�n": 'pr',
    "Matriz de confusi�n": 'confusion_matrix',
    "Error de predicci�n de clase": 'error',
    "Informe de clasificaci�n": 'class_report',
    "L�mite de decisi�n": 'l�mite',
    "Selecci�n de funciones recursivas": 'rfe',
    "Curva de aprendizaje": 'aprendizaje',
    "Aprendizaje m�ltiple": 'm�ltiple',
    "Curva de calibraci�n": 'calibraci�n',
    "Curva de validaci�n": 'vc',
    "Aprendizaje de dimensiones": 'dimensi�n',
    "Importancia de las funciones (Top 10)": 'funci�n',
    "Importancia de la caracter�stica (todas)": 'feature_all',
    "Curva de elevaci�n": 'elevaci�n',
    "Curva de ganancia": 'ganancia',
    "Gr�fico estad�stico de KS": 'ks'
}

fig_kwargs = {
                    "renderer": "png",
                    "width": 1000,
                    "height": 400,
                }


def clasificacion():
    if 'begin_cls' not in st.session_state:
        st.session_state.begin_cls = False

    if not st.session_state.begin_cls:
        if st.button("Iniciar"):
            st.session_state.begin_cls = True
            st.session_state.button_clicked_cls = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("Para comenzar nuevamente seleccionar el botón reiniciar.")
        if st.button("Reiniciar"):
            st.session_state.begin_cls = True
            st.session_state.button_clicked_cls = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()
        dataset = st.session_state.df
        option = None
        model_cls = None
        uploaded_file_test = None
        tune_YN = None

        if len(dataset) > 0:
            st.subheader("Datos:")
            st.write(dataset)
            st.subheader("Configuración de los datos:")

            col1,col2 = st.columns(2)
            # col1.header('Select Target Column')
            target = col1.selectbox("Selecciona la columna de destino:", dataset.columns, index=None,
                        placeholder="Selecciona la columna destino...")
            if target:
                feature_list = dataset.columns.tolist()
                feature_list.remove(target)
                features = col2.multiselect("Selecciona características a incluir:", feature_list)
                train_size = col1.slider("Establece el tamaño de los datos de entrenamiento:", 0.1, 0.9, 0.8)
                validation_size = col2.slider("Establece el tamaño de los datos de validación:", 0.1, 0.9 - train_size, 0.1)
                test_size = 1 - train_size - validation_size
                features.append(target)
                data = dataset[features].sample(frac=train_size, random_state=786).reset_index(drop=True)
                data_unseen = dataset[features].drop(data.index).reset_index(drop=True)
                results = pd.DataFrame()

                if "button_clicked_cls" not in st.session_state:
                    st.session_state.button_clicked_cls = False
                if 'form_submitted' not in st.session_state:
                    st.session_state.form_submitted = False
                if 'model_saved' not in st.session_state:
                    st.session_state.model_saved = False

                # Outer button
                outer_button_clicked_cls = st.button("Enviar")


                if outer_button_clicked_cls:
                    # st.write(len(features))
                    if len(features) < 2:  # Verificar si hay m�s de una caracter�stica seleccionada
                        st.warning("Selecciona características a incluir:")
                        st.session_state.button_clicked_cls = False
                    else:
                        st.session_state.button_clicked_cls = True

            else:
                if "button_clicked_cls" not in st.session_state:
                    st.session_state.button_clicked_cls = False
                else:
                    st.session_state.button_clicked_cls = False

            if st.session_state.button_clicked_cls:
                try:
                    s = setup(data, target=target, session_id=123)
                except Exception as e:
                    st.error(str(e))
                st.markdown('<p style="color:#0166FF"">�Configuración completada exitosamente!</p>', unsafe_allow_html=True)
                st.dataframe(pull())
                best = compare_models()
                results = pull()
                st.subheader("Mejor modelo: ", results['Model'].iloc[0])
                st.write('**Comparación entre todos los modelos.**')
                model_df = st.dataframe(pull())
               
                model_name = None
                tune_YN = None
                st.subheader("Selección y configuración del modelo:")
                with st.form(key='model_form'):
                    option = st.selectbox("Selecciona el modelo:",
                                              ["Mejor modelo", "Modelo específico", "Modelo de conjunto", "Mezcla", "Apilamiento"])

                    change = st.form_submit_button("Confirmar")
                    if change:
                        st.session_state.form_submitted = False
                        st.session_state.model_saved = False

                    if option == "Modelo espec�fico":
                        model_name = st.selectbox("Selecciona el nombre del modelo:", results['Model'].to_list())
                    elif option == "Modelo de conjunto":
                        model_name = st.selectbox("Selecciona el modelo a combinar:", results['Model'].to_list())
                        method = st.selectbox("Selecciona el método de combinación: ",['Bagging','Boosting'])
                    elif option == "Mezcla":
                        blend_models_list = st.multiselect("Selecciona los modelos a mezclar:", results['Model'].to_list())
                        method = st.selectbox("Selecciona el método de mezcla: ",['suave','fuerte'])
                    elif option == "Apilamiento":
                        stack_models_list = st.multiselect("Selecciona los modelos a apilar:", results['Model'].to_list())

                    tune_YN = st.checkbox ("Necesitas ajustar el modelo?")

                    selected_metrics = st.multiselect("Selecciona las métricas de clasificación para evaluar:",options=list(metrics_dict.keys()))
                    uploaded_file_test = st.file_uploader("Si desea cargar un conjunto de datos de prueba, cargue un archivo de prueba CSV o Excel (opcional):",
                                                          type=["csv", "xlsx"], key='test')

                    submit_button = st.form_submit_button(label='Cargar')
                    if submit_button:
                        st.session_state.form_submitted = True


            # Mostrar los elementos seleccionados si se env�a el formulario
            if st.session_state.form_submitted and st.session_state.begin_cls:
                st.write("Seleccionaste el modelo:",option)

                if option == "Mejor modelo":
                    model_cls = best
                    model_name = results['Model'].iloc[0]
                    save_model(model_cls, "best")

                elif option == "Modelo específico":
                    m_name = results[results['Model'] == model_name].index[0]
                    model_cls = create_model(m_name)
                    st.subheader("Modelo: ", model_name)
                    st.dataframe(pull())
                    save_model(model_cls,"specific_model")

                elif option == "Modelo de conjunto":
                    if model_name is not None:
                        m_name = results[results['Model'] == model_name].index[0]
                        try:
                            model_cls = create_model(m_name)
                            model = ensemble_model(model_cls, method =method)
                        except TypeError as e:
                            st.error(str(e))
                        st.subheader("Modelo: ", model_name, "method: ", method)
                        st.dataframe(pull())
                        save_model(model, "ensemble_model")

                    else:
                        st.warning("Elige los modelos para el conjunto.")

                elif option == "Mezcla":
                    if blend_models_list is not None:
                        model_list = []
                        blend_models_name= "Blending: "
                        for i in blend_models_list:
                            m_name = results[results['Model'] == i].index[0]
                            model_list.append(create_model(m_name, verbose=False))
                            blend_models_name = blend_models_name+", "+i
                        model_name = blend_models_name
                        try:
                            model_cls = blend_models(estimator_list=model_list, method=method)
                            save_model(model_cls, "blending_model")
                        except TypeError as e:
                            st.error(f"Error: {e}")
                        except:
                            st.error("Algo anda mal, prueba con otros modelos.")
                    else:
                        st.warning("Selecciona los modelos a mezclar.")

                elif option == "Apilamiento":
                    if stack_models_list is not None:
                        model_list = []
                        stacking_models = "Stacking: "
                        for i in stack_models_list:
                            m_name = results[results['Model'] == i].index[0]
                            model_list.append(create_model(m_name, verbose=False))
                            stacking_models = stacking_models+", "+i
                        model_name = stacking_models

                        try:
                            model_cls = stack_models(model_list)
                            save_model(model_cls, "stacking_model")
                        except TypeError as e:
                            st.write(f"Error: {e}")
                        except:
                            st.error("Algo anda mal, prueba con otros modelos.")
                    else:
                        st.warning("Selecciona los modelos a apilar.")
                st.session_state.model_saved = True

                if model_cls:
                    if tune_YN:
                        try:

                            final_model = tune_model(model_cls)
                            save_model(final_model, "tuned_model")
                            st.subheader("Modelo ajustado: ", model_name)
                            st.dataframe(pull())
                        except TypeError as e:
                            st.write("Error: ", str(e))
                        except:
                            st.error("Algo anda mal, prueba con otros modelos.")
                    else:
                        final_model = model_cls

                    if len(selected_metrics) >= 1 :
                        tabs = st.tabs(selected_metrics)

                        for metric, tab in zip(selected_metrics, tabs):
                            with tab:
                                try:
                                    img = plot_model(final_model, plot=metrics_dict[metric], display_format='streamlit', save=True)
                                    st.image(img)
                                except:
                                    try:
                                        plot_model(final_model, plot=metrics_dict[metric], display_format='streamlit')
                                      
                                    except:
                                        st.write( "Los datos no están disponibles. Considera utilizar métricas de evaluación alternativas.")
                                    
                    
                    # Predicci�n
                    try:
                        pred_holdout = predict_model(final_model)
                        st.subheader('Predicciones del conjunto de validación:')
                        st.dataframe(pred_holdout)
                    except:
                        st.error("Algo anda mal, prueba con otros modelos.")
                else:
                    st.warning("Selecciona los modelos.")

                if uploaded_file_test:
                    st.subheader('Datos de prueba:')
                    if uploaded_file_test.name.endswith('.csv'):
                        test_dataset = pd.read_csv(uploaded_file_test)
                    elif uploaded_file_test.name.endswith(('.xlsx', '.xls')):
                        test_dataset = pd.read_excel(uploaded_file_test)
                    st.subheader("Datos:")
                    st.dataframe(test_dataset)
                    

                    try:
                        if target in test_dataset.columns:
                            test_dataset = test_dataset[features]
                            test_dataset = test_dataset.drop(target, axis=1)
                            test_pred = predict_model(final_model, test_dataset)
                            st.subheader("Predicción:")
                            st.dataframe(test_pred)
                        else:
                            features.pop()
                            test_dataset = test_dataset[features]
                            test_pred = predict_model(best, test_dataset)
                            st.subheader("Predicción:")
                            st.dataframe(test_pred)
                    except KeyError as e:
                        st.error(str(e))
                    except:
                        st.error("Algo anda mal, prueba con otros modelos.")
           
           
            # Mostrar el bot�n de descarga si se guarda el modelo
            if st.session_state.model_saved:
                if option == "Mejor modelo":
                    with open('best.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar mejor modelo",
                            data=f,
                            file_name='best_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Modelo específico":
                    with open('specific_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo espec�fico",
                            data=f,
                            file_name='specific_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Modelo de conjunto":
                    with open('ensemble_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo de conjunto",
                            data=f,
                            file_name='ensemble_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Mezcla":
                    with open('blending_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo mezcla",
                            data=f,
                            file_name='blending_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option == "Apilamiento":
                    with open('stacking_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo apilamiento",
                            data=f,
                            file_name='stacking_model.pkl',
                            mime='application/octet-stream'
                        )
                if tune_YN:
                    with open('tuned_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo ajustado",
                            data=f,
                            file_name='tuned_model.pkl',
                            mime='application/octet-stream'
                        )
        else:
            st.warning("Por favor, carga un archivo de datos.")