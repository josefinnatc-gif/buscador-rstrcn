import streamlit as st

# ---------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------
st.set_page_config(page_title="Buscador RSTRCN", page_icon="📜", layout="centered")

st.title("📚 Buscador de Casos RSTRCN")
st.write("Busca documentos o casos históricos del repositorio digital.")

# ---------------------------
# BASE DE DATOS SIMULADA
# ---------------------------
documentos = [
    {
        "titulo": "Nuevo Mapa de Chile – Código: 051-2",
        "descripcion": "Este caso se encuentra en el libro de ingreso 1, del año 83. Es una impresión del año 1878 que procede de la biblioteca de Santiago.",
        "ruta_archivos": []
    },
    {
        "titulo": "Sra. Josefina Lira – Código: 053-2",
        "descripcion": "Este es un pastel sobre tela de fines del siglo XIX, tiene procedencia del Museo Nacional de Bellas Artes.",
        "ruta_archivos": [
            {
                "nombre": "Documento PDF del caso Josefina Lira",
                "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"
            }
        ]
    },
]

# ---------------------------
# FUNCIÓN DE BÚSQUEDA
# ---------------------------
def buscar_documentos(query):
    resultados = []
    for doc in documentos:
        if query.lower() in doc["titulo"].lower() or query.lower() in doc["descripcion"].lower():
            resultados.append(doc)
    return resultados

# ---------------------------
# MANEJO DE ESTADO
# ---------------------------
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# ---------------------------
# INTERFAZ PRINCIPAL
# ---------------------------
if st.session_state.selected_doc is None:
    query = st.text_input("🔍 Escribe una palabra clave para buscar:")
    if query:
        resultados = buscar_documentos(query)
        if resultados:
            st.subheader("Resultados encontrados:")
            for i, doc in enumerate(resultados):
                if st.button(doc["titulo"], key=i):
                    st.session_state.selected_doc = doc
                    st.experimental_rerun()
        else:
            st.warning("No se encontraron resultados para esa búsqueda.")
else:
    # Mostrar detalle del documento seleccionado
    doc = st.session_state.selected_doc
    st.header(doc["titulo"])
    st.write(doc["descripcion"])

    # Mostrar archivos adjuntos
    if doc["ruta_archivos"]:
        st.subheader("📎 Documentos adjuntos:")
        for archivo in doc["ruta_archivos"]:
            st.markdown(
                f"- [{archivo['nombre']}]({archivo['url']})  ⤴️",
                unsafe_allow_html=True
            )
    else:
        st.info("No hay archivos adjuntos para este caso.")

    if st.button("🔙 Volver a resultados"):
        st.session_state.selected_doc = None
        st.experimental_rerun()

