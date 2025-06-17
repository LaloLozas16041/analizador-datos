import streamlit as st
import pandas as pd
from pycaret.regression import setup, compare_models, predict_model, pull, plot_model, create_model, ensemble_model, blend_models, stack_models, tune_model, save_model




# Dictionary of metrics
metrics_dict_reg = {
 "Gráfico de residuos": 'residuales',
    "Gráfico de error de predicción": 'error',
    "Trama de distancia de cocineros": 'cocineros',
    "Selección de funciones recursivas": 'rfe',
    "Curva de aprendizaje": 'aprendizaje',
    "Curva de validación": 'vc',
    "Aprendizaje múltiple": 'múltiple',
    "Importancia de las funciones (Top 10)": 'función',
    "Importancia de la característica (todas)": 'feature_all',

}

def regresion():
    if 'begin_reg' not in st.session_state:
        st.session_state.begin_reg = False

    if not st.session_state.begin_reg:
        if st.button("Iniciar"):
            st.session_state.begin_reg = True
            st.session_state.button_clicked_reg = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
    else:
        st.info("Para reiniciar selecciona: Reiniciar.")
        if st.button("Reiniciar"):
            st.session_state.begin_reg = True
            st.session_state.button_clicked_reg = False
            st.session_state.form_submitted = False
            st.session_state.model_saved = False
        if 'page' not in st.session_state:
            st.session_state.page = "Home"
        if 'df' not in st.session_state:
            st.session_state.df = pd.DataFrame()
        dataset = st.session_state.df
        option_reg = None
        model_reg = None
        uploaded_file_test_reg = None
        tune_YN_reg = None
        final_model_reg = None

        if len(dataset) > 0:

            st.subheader("Datos:")
            st.write(dataset)
            st.subheader("Configuración de los datos:")

            col1,col2 = st.columns(2)
            # col1.header('Seleccionar columna destino')
            target_reg = col1.selectbox("Selecciona la columna de destino:", dataset.columns, index=None,
                            placeholder="Selecciona la columna de destino...")
            if target_reg:
                feature_list_reg = dataset.columns.tolist()
                feature_list_reg.remove(target_reg)
                # col2.header('Seleccionar características')
                features_reg = col2.multiselect("Selecciona características a incluir:", feature_list_reg)

                train_size = col1.slider("Define el tamaño de los datos de entrenamiento:", 0.1, 0.9, 0.8)
                validation_size = col2.slider("Define el tamaño de los datos de validación:", 0.1, 0.9 - train_size, 0.1)
                test_size = 1 - train_size - validation_size
                features_reg.append(target_reg)
                data_reg = dataset[features_reg].sample(frac=train_size, random_state=786).reset_index(drop=True)
                data_unseen_reg = dataset[features_reg].drop(data_reg.index).reset_index(drop=True)

                if "button_clicked_reg" not in st.session_state:
                    st.session_state.button_clicked_reg = False
                if 'form_submitted' not in st.session_state:
                    st.session_state.form_submitted = False
                if 'model_saved' not in st.session_state:
                    st.session_state.model_saved = False
                # submit_button_reg = False

                # Outer button
                outer_button_clicked_reg = st.button("Enviar")

                if outer_button_clicked_reg:
                    if len(features_reg) <= 1:  # Se incluye el objetivo, verifique si hay más de una característica seleccionada.
                        st.warning("Selecciona características a incluir.")
                    else:
                        st.session_state.button_clicked_reg = True

            else:
                if "button_clicked_cls" not in st.session_state:
                    st.session_state.button_clicked_reg = False
                else:
                    st.session_state.button_clicked_reg = False


            if st.session_state.button_clicked_reg :
                # con st.spinner("Cargando..."):
                try:
                    s_reg = setup(data_reg, target=target_reg, session_id=123)
                except Exception as e:
                    st.error(str(e))
                st.markdown('<p style="color:#0166FF">Configuración completada exitosamente!</p>', unsafe_allow_html=True)
                st.dataframe(pull())
                with st.spinner("Cargando..."):
                  
                    # Obtener el mejor modelo
                    best_reg = compare_models()
                    
                    # Obtener la tabla de puntuación
                    results_reg = pull()
                    try:
                        st.subheader("Mejor modelo: ", results_reg['Model'].iloc[0])
                    except Exception as e:
                        st.error("Algo parecer estar incorrecto. Asegúrate que las columnas y funciones de destino se seleccionaron correctamente.")
                    # st.subheader("Mejor modelo: ", results_reg['Model'].iloc[0])
                    st.write('**Comparación entre todos los modelos.**')
                    model_df_reg = st.dataframe(pull())

          
                st.subheader("Selección y configuración del modelo:")
                with st.form(key='model_form_reg'):
                    option_reg = st.selectbox("Selecciona una opción de modelo:",
                                              ["Mejor modelo", "Modelo específico", "Modelo de conjunto", "Mezcla", "Apilamiento"])
                    st.markdown('<p style="color:#3355FF">Elija una opción de modelo y haga clic en el botón a continuación para confirmar.</p>',unsafe_allow_html=True)



                    change_reg = st.form_submit_button("Confirmar")
                    model_name_reg = None
                    if option_reg == "Modelo especéfico":
                        model_name_reg = st.selectbox("Selecciona el nombre del modelo:", results_reg['Model'].to_list())
                    elif option_reg == "Modelo de conjunto":
                        model_name_reg = st.selectbox("Selecciona el modelo a combinar:", results_reg['Model'].to_list())
                        method_reg = st.selectbox("Selecciona el método de mezcla. ",['Bagging','Boosting'])
                    elif option_reg == "Mezcla":
                        blend_models_list = st.multiselect("Selecciona los modelos para mezclar:", results_reg['Model'].to_list())
                        # method = st.selectbox("Selecciona el método de mezcla: ",['soft','hard'])
                    elif option_reg == "Apilamiento":
                        stack_models_list_reg = st.multiselect("Selecciona modelos para apilar:", results_reg['Model'].to_list())

                    tune_YN_reg = st.checkbox ("Necesitas ajustar el modelo?")

                    selected_metrics_reg = st.multiselect("Seleccionar métricas de regresión para evaluar:",options=list(metrics_dict_reg.keys()))
                    uploaded_file_test_reg = st.file_uploader("Si desea cargar un conjunto de datos de prueba, cargue un archivo de prueba CSV o Excel (opcional):",
                                                          type=["csv", "xlsx"], key='test')

                    submit_button_reg = st.form_submit_button(label='Enviar')
                    if submit_button_reg:
                        st.session_state.form_submitted = True


            # Mostrar los elementos seleccionados si se envía el formulario.
            if st.session_state.form_submitted and st.session_state.begin_reg:
                st.write("Seleccionaste el modelo:",option_reg)

                if option_reg == "Mejor modelo":
                    model_reg = best_reg
                    model_name_reg = results_reg['Model'].iloc[0]
                    save_model(best_reg,"best")

                elif option_reg == "Modelo específico":
                    m_name_reg = results_reg[results_reg['Model'] == model_name_reg].index[0]
                    model_reg = create_model(m_name_reg)
                    st.subheader("Modelo: ", model_name_reg)
                    st.dataframe(pull())
                    save_model(model_reg,"specific_model")

                elif option_reg == "Modelo de conjunto":
                    if model_name_reg is not None:
                        m_name_reg = results_reg[results_reg['Model'] == model_name_reg].index[0]
                        model_reg = create_model(m_name_reg)
                        model_reg = ensemble_model(model_reg, method =method_reg)
                        st.subheader("Modelo: ", model_name_reg, "method: ", method_reg)
                        st.dataframe(pull())
                        save_model(model_reg, "ensemble_model")
                    else:
                        st.warning("Selecciona los modelos para el conjunto.")

                elif option_reg == "Mezcla":
                    if blend_models_list is not None:
                        model_list_reg = []
                        blend_models_name_reg = "Mezcla: "
                        for i in blend_models_list:
                            m_name_reg = results_reg[results_reg['Model'] == i].index[0]
                            model_list_reg.append(create_model(m_name_reg, verbose=False))
                            blend_models_name_reg = blend_models_name_reg+", "+i
                        model_name_reg = blend_models_name_reg
                        try:
                            model_reg = blend_models(estimator_list=model_list_reg)
                            save_model(model_reg, "blending_model")

                        except TypeError as e:
                            st.error(str(e))
                            st.error("Por favor, prueba otros modelos.")
                        except:
                            st.error("Algo anda mal, prueba con otros modelos.")
                    else:
                        st.warning("Selecciona los modelos para mezclar.")

                elif option_reg == "Apilamiento":
                    if stack_models_list_reg is not None:
                        model_list_reg = []
                        stacking_models_reg = "Apilamiento: "
                        for i in stack_models_list_reg:
                            m_name_reg = results_reg[results_reg['Model'] == i].index[0]
                            model_list_reg.append(create_model(m_name_reg, verbose=False))
                            stacking_models_reg = stacking_models_reg+", "+i
                        model_name_reg = stacking_models_reg

                        try:
                            model_reg = stack_models(model_list_reg)
                            save_model(model_reg, "stacking_model")
                        except TypeError as e:
                            st.error(str(e))
                            st.info("Por favor, prueba otros modelos.")
                        except:
                            st.error("Algo anda mal, prueba con otros modelos.")
                    else:
                        st.warning("Selecciona los modelos para apilar.")

                if model_reg:
                    if tune_YN_reg:
                        try:
                            final_model_reg = tune_model(model_reg)
                            st.subheader("Modelo ajustado: ", model_name_reg)
                            st.dataframe(pull())
                            save_model(final_model_reg, "tuned_model")
                        except Exception as e:

                            st.error(str(e))
                            st.info("Por favor, prueba con otros modelos.")
                        except:
                            st.error("Algo anda mal, prueba con otros modelos.")

                    else:
                        final_model_reg = model_reg

                    if len(selected_metrics_reg) >= 1 and final_model_reg :
                        tabs_reg = st.tabs(selected_metrics_reg)

                        for metric, tab in zip(selected_metrics_reg, tabs_reg):
                            with tab:
                                try:
                                    img = plot_model(final_model_reg, plot=metrics_dict_reg[metric], display_format='streamlit', save=True)
                                    st.image(img)
                                except:
                                    try:
                                        plot_model(final_model_reg, plot=metrics_dict_reg[metric], display_format='streamlit')
                                       
                                    except:
                                        st.write( "Los datos no están disponibles. Considere utilizar métricas de evaluación alternativas.")
                                    
                    try:
                        # Predicción 
                        pred_holdout_reg = predict_model(final_model_reg)
                        st.subheader('Predicciones del conjunto de validación:')
                        st.dataframe(pred_holdout_reg)
                    except Exception as e:
                        st.error(str(e))

                else:
                    st.warning("Selecciona los modelos")
                st.session_state.model_saved = True

                if uploaded_file_test_reg and final_model_reg:
                    st.subheader('Datos de prueba:')
                    # test_dataset_reg = pd.read_csv(uploaded_file_test_reg)
                    # st.dataframe(test_dataset_reg)
                    if uploaded_file_test_reg.name.endswith('.csv'):
                        test_dataset_reg = pd.read_csv(uploaded_file_test_reg)
                    elif uploaded_file_test_reg.name.endswith(('.xlsx', '.xls')):
                        test_dataset_reg = pd.read_excel(uploaded_file_test_reg)
                    st.subheader("Datos de prueba:")
                    st.dataframe(test_dataset_reg)

                    try:

                        if target_reg in test_dataset_reg.columns:
                            # st.write(test_dataset.columns)
                            test_dataset_reg = test_dataset_reg[features_reg]
                            test_dataset_reg = test_dataset_reg.drop(target_reg, axis=1)
                            test_pred_reg = predict_model(final_model_reg, test_dataset_reg)
                            st.subheader("Predicción")
                            st.dataframe(test_pred_reg)
                        else:
                            # st.write(test_dataset.columns)
                            features_reg.pop()
                            test_dataset = test_dataset_reg[features_reg]
                            # st.dataframe(test_dataset)
                            test_pred = predict_model(best_reg, test_dataset)
                            st.subheader("Predicción")
                            st.dataframe(test_pred)
                    except Exception as e:
                        st.error(str(e))
                    # except:
                    #     st.error("Algo anda mal, prueba con otros modelos.")

            # Mostrar el botón de descarga si se guarda el modelo
            if st.session_state.model_saved:
                if option_reg == "Best Model":
                    with open('best.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar mejor modelo",
                            data=f,
                            file_name='best_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Specific Model":
                    with open('specific_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo específico",
                            data=f,
                            file_name='specific_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Ensemble Model":
                    with open('ensemble_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo de conjunto",
                            data=f,
                            file_name='ensemble_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Mezcla":
                    with open('blending_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo mezclado",
                            data=f,
                            file_name='blending_model.pkl',
                            mime='application/octet-stream'
                        )
                elif option_reg == "Apilamiento":
                    with open('stacking_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo apilado",
                            data=f,
                            file_name='stacking_model.pkl',
                            mime='application/octet-stream'
                        )
                if tune_YN_reg:
                    with open('tuned_model.pkl', 'rb') as f:
                        st.download_button(
                            label="Descargar modelo ajustado",
                            data=f,
                            file_name='tuned_model.pkl',
                            mime='application/octet-stream'
                        )

        else:
            st.warning("Por favor, para continuar carga un archivo de datos.")