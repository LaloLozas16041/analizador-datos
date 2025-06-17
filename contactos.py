import streamlit as st
import yagmail
import re

def send_email(name, sender_email, message):
    # Configura los detalles del servidor SMTP usando yagmail
    yag = yagmail.SMTP('lozas2605@gmail.com', 'cnpl stzm fksu ixpj')
    subject = 'Mensaje desde la aplicación de contacto'
    body = f'Nombre: {name}\nCorreo electrónico: {sender_email}\nMensaje:\n{message}'
    receiver_email = 'lozas2605@gmail.com'

    try:
        yag.send(to=receiver_email, subject=subject, contents=body)
        return True
    except Exception as e:
        st.error(f'Ocurrió un error al enviar el correo: {e}')
        return False

def validate_email(email):
    # Validación de formato de correo electrónico usando una expresión regular
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_name(name):
    # Validación básica de nombre: no debe estar vacío y no debe contener caracteres especiales ni números
    return bool(re.match(r'^[a-zA-Z������������\s]+$', name))

def validate_message(message):
    # Validación básica de mensaje: no debe estar vacío
    return bool(message.strip())

def contacto():
    st.write("<h1 style='text-align: center; color: #0166FF;'>Contacto</h1>", unsafe_allow_html=True)

    # Inicializar el estado de la sesi�n para los campos del formulario
    if 'name' not in st.session_state:
        st.session_state.name = ''
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'message' not in st.session_state:
        st.session_state.message = ''

    # Dise�o en columnas para ajustar el ancho del formulario
    col1, col2, col3 = st.columns([1, 2, 1])

    # Formulario de contacto en la segunda columna
    with col2:
        st.markdown('**Si tiene alguna consulta complete este formulario y nos comunicaremos lo antes posible con usted.**')
        name = st.text_input('Nombre *', value=st.session_state.name)
        email = st.text_input('Correo electrónico *', value=st.session_state.email)
        message = st.text_area('Mensaje *', value=st.session_state.message)

        if st.button('Enviar'):
            if not validate_name(name):
                st.error('Por favor ingrese un nombre válido (solo letras y espacios).')
            elif not validate_email(email):
                st.error('Por favor ingrese un correo electrónico válido.')
            elif not validate_message(message):
                st.error('Por favor ingrese un mensaje.')
            else:
                if send_email(name, email, message):
                    st.success('El correo ha sido enviado exitosamente.')
                    st.info(f'Nos pondremos en contacto contigo pronto, {name}!')
                    # Limpiar campos despu�s de enviar
                    st.session_state.name = ''
                    st.session_state.email = ''
                    st.session_state.message = ''
                else:
                    st.error('No se pudo enviar el correo. Por favor inténtelo nuevamente.')

if __name__ == '__main__':
    contacto()