import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------
st.set_page_config(page_title="Motor de Búsqueda CNCR", page_icon=None, layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #cce7ff; /* celeste pastel ligero */
        color: #3a2e2e;
        font-family: 'Georgia', serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Georgia', cursive;
        color: #2b2b2b;
    }
    .stTextInput input {
        border: 1px solid #bfa98a;
        border-radius: 10px;
        background-color: #fcfaf7;
        color: #3a2e2e;
    }
    .stButton button {
        background-color: #c8b6a6;
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        font-family: 'Georgia', cursive;
    }
    .stButton button:hover {
        background-color: #9bbcc0;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Motor de búsqueda de restauración y conservación")
st.write("""
Explora casos documentados de restauración del CNCR.  
Escribe palabras clave (por ejemplo: *óleo*, *1986*, *pastel sobre tela*, *Santiago*)  
y el sistema te mostrará los casos más relacionados.
""")

# ---------------------------
# DOCUMENTOS COMPLETOS
# ---------------------------
documents = [
    {
        "titulo": "Nuevo Mapa de Chile – Código: 051-2",
        "descripcion": "Libro de ingreso 1 del año 1983. Impresión del año 1878 proveniente de la biblioteca de Santiago. Salida del centro en 2005. Ubicación: cuerpo E librero 3 estante b carpeta 6.",
        "adjuntos": [
            {"nombre": "PDF del mapa", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    },
    {
        "titulo": "Sra. Josefina Lira – Código: 053-2",
        "descripcion": "Pastel sobre tela de fines del siglo XIX, procedente del Museo de Bellas Artes. Ingreso en 1983. Ubicación: cuerpo E librero 3 estante b carpeta 5.",
        "adjuntos": [
            {"nombre": "PDF del caso Josefina Lira", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    },
    {
        "titulo": "Carta de José Miguel Carrera – Código: 058-4",
        "descripcion": "Ingreso en 1985. Historia: escrita por José Miguel Carrera en Mendoza antes de morir. Fecha de la carta: 1821. Ubicación: cuerpo E librero 3 estante b carpeta 1.",
        "adjuntos": [
            {"nombre": "Carta 1821 PDF", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    },
    {
        "titulo": "Litografía Lago Vichuquén de Llico – Código: 059-4",
        "descripcion": "Detalle de autor y técnica, descripción de color. Salida 12 de mayo de 1986. Fotos digitalizadas. Ubicación: cuerpo E librero 3 estante b carpeta 9.",
        "adjuntos": [
            {"nombre": "PDF litografía Llico", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    },
    {
        "titulo": "Desnudo por Jean Jacques Henner – Código: 003-14",
        "descripcion": "Ingreso 20 de abril de 1995, salida 16 de noviembre 1995. Fotos no digitales. Ubicación: cuerpo E librero 2 estante d carpeta 6.",
        "adjuntos": [
            {"nombre": "PDF Desnudo Henner", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    },
    {
        "titulo": "Naturaleza muerta por Harnett – Código: 012-14",
        "descripcion": "Ingreso 2 de junio de 1995, salida 17 de julio de 1995. Ubicación: cuerpo E librero 8 estante a carpeta 2.",
        "adjuntos": [
            {"nombre": "PDF Naturaleza Harnett", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    },
    {
        "titulo": "Globo terráqueo – Código: 024-14",
        "descripcion": "Técnicas: varillas de madera, papel maché, yeso, papel impreso y protección. Estadía 4 meses 3 días. Código LP:43. Ubicación: cuerpo E librero 3 estante b carpeta 2.",
        "adjuntos": [
            {"nombre": "PDF Globo Terráqueo", "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}
        ]
    }
]

# ---------------------------
# CONFIGURAR TF-IDF
# ---------------------------
texts = [doc["titulo"] + " " + doc["descripcion"] for doc in documents]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# ---------------------------
# ESTADO DE SESIÓN
# ---------------------------
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# ---------------------------
# BUSQUEDA Y RESULTADOS
# ---------------------------
if st.session_state.selected_doc is None:
    query = st.text_input("🔎 Escribe una palabra clave:", key="input_query")
    if query:
        query_vector = vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, tfidf_matrix)[0]
        sorted_indices = similarities.argsort()[::-1]

        st.markdown("---")
        st.subheader(f"Resultados para: *{query}*")
        found = False
        for i in sorted_indices:
            if similarities[i] > 0:
                found = True
                doc = documents[i]
                if st.button(doc["titulo"], key=f"resultado_{i}"):
                    st.session_state.selected_doc = i
                    st.experimental_rerun()
        if not found:
            st.warning("No se encontraron resultados relevantes.")
    else:
        st.info("Escribe una palabra clave para comenzar la búsqueda.")

# ---------------------------
# DETALLE DOCUMENTO SELECCIONADO
# ---------------------------
if st.session_state.selected_doc is not None:
    doc = documents[st.session_state.selected_doc]
    st.markdown("---")
    st.subheader(f"📄 {doc['titulo']}")
    st.write(doc['descripcion'])

    if "adjuntos" in doc and doc["adjuntos"]:
        st.subheader("📎 Documentos adjuntos:")
        for idx, archivo in enumerate(doc["adjuntos"]):
            st.markdown(f"- [{archivo['nombre']}]({archivo['url']}) ⤴️", unsafe_allow_html=True)
    else:
        st.info("No hay archivos adjuntos para este caso.")

    if st.button("🔙 Volver a resultados", key="volver_resultados"):
        st.session_state.selected_doc = None
        st.experimental_rerun()

