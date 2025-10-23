import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------
# 🌿 CONFIGURACIÓN GENERAL
# ----------------------------------------------------------
st.set_page_config(page_title="Motor de Búsqueda CNCR", layout="centered")

# Estilos personalizados
st.markdown("""
    <style>
    body {
        background-color: #d8ecf3; /* celeste pastel */
        color: #2b2b2b;
        font-family: 'Georgia', serif;
    }
    h1, h2, h3, h4 {
        font-family: 'Georgia', cursive;
        color: #2b2b2b;
    }
    .stTextInput input {
        border: 1px solid #a7c7d9;
        border-radius: 10px;
        background-color: #f4fbfd;
        color: #2b2b2b;
    }
    .stButton button {
        background-color: #8abbd9;
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        font-family: 'Georgia', cursive;
    }
    .stButton button:hover {
        background-color: #5a99b8;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# 🖋️ TÍTULO Y DESCRIPCIÓN
# ----------------------------------------------------------
st.title("Motor de búsqueda de restauración y conservación")
st.write("""
Este motor permite explorar casos documentados de restauración del CNCR.  
Escribe palabras clave (por ejemplo: *óleo*, *salida 1986*, *pastel sobre tela*, *Santiago*)  
y el sistema te mostrará los casos más relacionados.
""")

# ----------------------------------------------------------
# 📁 DOCUMENTOS
# ----------------------------------------------------------
documents = [
    {
        "titulo": "Nuevo Mapa de Chile – Código: 051-2",
        "descripcion": "Libro de ingreso 1 del año 1983. Impresión del año 1878 proveniente de la biblioteca de Santiago. Salida del centro en 2005. No confirmada presencia de foto. Todo documento relacionado se encuentra en el cuerpo E librero 3 estante b carpeta 6.",
        "ruta_archivos": []
    },
    {
        "titulo": "Sra. Josefina Lira – Código: 053-2",
        "descripcion": "Pastel sobre tela de fines del siglo XIX, procedente del Museo de Bellas Artes. Ingreso en 1983, sin fecha de salida. Caso importante por conectividad con otros documentos asociados. Todo documento relacionado se encuentra en el cuerpo E librero 3 estante b carpeta 5.",
        "ruta_archivos": [
            {
                "nombre": "Documento PDF del caso",
                "url": "https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"
            }
        ]
    },
    {
        "titulo": "Carta de José Miguel Carrera – Código: 058-4",
        "descripcion": "Ingreso en 1985. Incluye información de salida y nombres de restauradores. 'Historia': fue escrita por José Miguel Carrera en Mendoza antes de morir y enviada a Santiago en una caja de fósforos. Fecha de la carta: 1821. Todo documento relacionado se encuentra en el cuerpo E librero 3 estante b carpeta 1.",
        "ruta_archivos": []
    },
    {
        "titulo": "Litografía Lago Vichuquén de Llico – Código: 059-4",
        "descripcion": "Detalle en secciones de autor y técnica, incluye descripción de color. Nombre de la restauradora registrado. Salida el 12 de mayo de 1986. Código LP: 108. Posee fotos digitalizadas. Todo documento relacionado se encuentra en el cuerpo E librero 3 estante b carpeta 9.",
        "ruta_archivos": []
    },
    {
        "titulo": "Desnudo por Jean Jacques Henner – Código: 003-14",
        "descripcion": "Categoría 'Número inventario museo'. Ingreso el 20 de abril de 1995 y salida el 16 de noviembre del mismo año. Fotos no digitales. UPGD:1004 LP:46. Todo documento relacionado se encuentra en el cuerpo E librero 2 estante d carpeta 6.",
        "ruta_archivos": []
    },
    {
        "titulo": "Naturaleza muerta por Harnett – Código: 012-14",
        "descripcion": "Restauradora distinta a las anteriores. Ingreso el 2 de junio de 1995 y salida el 17 de julio de 1995, permaneció 1 mes y 15 días. Código LP:10. Todo documento relacionado se encuentra en el cuerpo E librero 8 estante a carpeta 2.",
        "ruta_archivos": []
    },
    {
        "titulo": "Globo terráqueo – Código: 024-14",
        "descripcion": "Técnicas: varillas de madera, papel maché, yeso, papel impreso y protección. Estancia de 4 meses y 3 días. Código LP:43. Todo documento relacionado se encuentra en el cuerpo E librero 3 estante b carpeta 2.",
        "ruta_archivos": []
    }
]

# ----------------------------------------------------------
# 🧠 CONFIGURAR VECTOR DE BÚSQUEDA TF-IDF
# (Incluye título y descripción)
# ----------------------------------------------------------
texts = [doc["titulo"] + " " + doc["descripcion"] for doc in documents]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# ----------------------------------------------------------
# 🔍 BÚSQUEDA
# ----------------------------------------------------------
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

if st.session_state.selected_doc is None:
    query = st.text_input("🔎 Escribe una palabra clave:", "")

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
                if st.button(f"📄 {doc['titulo']}"):
                    st.session_state.selected_doc = doc
                    st.rerun()
        if not found:
            st.warning("No se encontraron resultados relevantes.")
    else:
        st.info("Escribe una palabra clave para comenzar la búsqueda.")
else:
    # Vista detallada del documento
    doc = st.session_state.selected_doc
    st.markdown("---")
    st.header(doc["titulo"])
    st.write(doc["descripcion"])

    if doc["ruta_archivos"]:
        st.subheader("📎 Documentos adjuntos:")
        for file in doc["ruta_archivos"]:
            st.markdown(f"- [{file['nombre']}]({file['url']})", unsafe_allow_html=True)
    else:
        st.info("Este caso no tiene documentos adjuntos.")

    if st.button("🔙 Volver a los resultados"):
        st.session_state.selected_doc = None
        st.rerun()
