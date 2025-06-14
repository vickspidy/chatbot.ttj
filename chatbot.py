import streamlit as st
import groq

#TENER NUESTROS MODELOS DE IA
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768'] 

#CONFIGURAR LA PAGINA
def configurar_pagina():
    st.set_page_config(page_title="MI PRIMER CHATBOT CON PYTHON", page_icon="😝") #cambia nombre de la ventana del navegador
    st.title("Bienvenidos al Súper Chatbot")

#MOSTRAR EL SIDEBAR CON LOS MODELOS
def mostrar_sidebar():
    st.sidebar.title("ELEGÍ TU MODELO DE IA")
    modelo = st.sidebar.selectbox("Elijo...", MODELOS, index=0)
    st.write(f"**SE ELIGIÓ EL MODELO:** {modelo}")
    return modelo

#INICIALIZAR EL ESTADO DEL CHAT
def inicializacion_estado_chat():
    if "mensajes"  not in st.session_state:
        st.session_state.mensajes = [] #lista

#UN CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"] #almacena la api key de groq
    cliente = groq.Client(api_key=groq_api_key)
    return groq.Groq(api_key=groq_api_key)

#INICIALIZAR EL ESTADO DEL MENSAJE 
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#HISTORIAL DEL CHAT
def mostrar_historial_chat():
    for mensajes in st.session_state.mensajes:
        with st.chat_message(mensajes["role"]): #context manager
            st.markdown(mensajes["content"])

#OBTENER MENSAJE DE USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Manda tu mensaje")

#GUARDAR LOS MENSAJES
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

#AGREGAR LOS MENSAJES AL ESTADO
def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role":role, "content":content})

#MOSTRAR LOS MENSAJES EN PANTALLA
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)


#LLAMAR AL MODELO GROQ
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes, 
        stream=False
    )
    return respuesta.choices[0].message.content


#FLUJO DE LA APP

def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()

    inicializacion_estado_chat()
    mostrar_historial_chat()

    mensaje_usuario = obtener_mensaje_usuario()

    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)
        
        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensaje_al_historial("assistant", mensaje_modelo,)
        mostrar_mensaje("assistant", mensaje_modelo)



if __name__ == '__main__': #si este archivo es el principal, entonces ejecuta
    ejecutar_app()