import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------
# 🌿 CONFIGURACIÓN GENERAL
# ----------------------------------------------------------
st.set_page_config(page_title="Motor de Búsqueda CNCR", page_icon=None, layout="centered")

# Colores y estilo
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
        background-color: #9bbcc0; /* azul pastel */
        color: #fff;
    }
    a {
        color: #3a2e2e;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# 🖋️ TÍTULO Y DESCRIPCIÓN
# ----------------------------------------------------------
st.title("Motor de búsqueda de restauración y conservación")
st.write("""
Explora casos documentados de restauración del CNCR.  
Escribe palabras clave (por ejemplo: *óleo*, *1986*, *pastel sobre tela*, *Santiago*)  
y el sistema te mostrará los casos más relacionados.
""")

# ----------------------------------------------------------
# 📁 DOCUMENTOS
# ----------------------------------------------------------
documents = [
    {
        "titulo": "Nuevo Mapa de Chile – Código: 051-2",
        "descripcion": "Libro de ingreso 1 del año 1983. Impresión del año 1878 proveniente de la biblioteca de Santiago. Salida del centro en 2005. No se confirma presencia de foto. Ubicación: cuerpo E librero 3 estante b carpeta 6.",
        "adjuntos": ["docs/mapa1878.pdf", "docs/foto_mapa.tif"]
    },
    {
        "titulo": "Sra. Josefina Lira – Código: 053-2",
        "descripcion": "Pastel sobre tela de fines del siglo XIX, procedente del Museo de Bellas Artes. Ingreso en 1983, sin fecha de salida. Importancia por conectividad con otros documentos. Ubicación: cuerpo E librero 3 estante b carpeta 5.",
        "adjuntos": ["docs/pastel_lira.pdf", "docs/foto_lira.jpg"]
    },
    {
        "titulo": "Carta de José Miguel Carrera – Código: 058-4",
        "descripcion": "Ingreso en 1985, incluye información de salida y restauradores. Historia: escrita por José Miguel Carrera en Mendoza antes de morir, enviada a Santiago en caja de fósforos. Fecha de la carta: 1821. Ubicación: cuerpo E librero 3 estante b carpeta 1.",
        "adjuntos": ["docs/carta1821.pdf"]
    },
    {
        "titulo": "Litografía Lago Vichuquen de Llico – Código: 059-4",
        "descripcion": "Detalle de autor y técnica, descripción de color. Restauradora registrada. Salida 12 de mayo de 1986. Código LP:108. Fotos digitalizadas. Ubicación: cuerpo E librero 3 estante b carpeta 9.",
        "adjuntos": ["docs/litografia_llico.pdf", "docs/foto_llico.jpg"]
    },
    {
        "titulo": "Desnudo por Jean Jacques Henner – Código: 003-14",
        "descripcion": "Número inventario museo. Ingreso 20 de abril de 1995, salida 16 de noviembre de 1995. Fotos no digitales. UPGD:1004 LP:46. Ubicación: cuerpo E librero 2 estante d carpeta 6.",
        "adjuntos": ["docs/henner_desnudo.pdf", "docs/foto_henner.tif"]
    },
    {
        "titulo": "Naturaleza muerta por Harnett – Código: 012-14",
        "descripcion": "Restauradora distinta. Ingreso 2 de junio de 1995, salida 17 de julio de 1995 (1 mes 15 días). Código LP:10. Ubicación: cuerpo E librero 8 estante a carpeta 2.",
        "adjuntos": ["docs/harnett_naturaleza.pdf", "docs/foto_harnett.jpg"]
    },
    {
        "titulo": "Globo terráqueo – Código: 024-14",
        "descripcion": "Técnicas: varillas de madera, papel maché, yeso, papel impreso y protección. Estadía de 4 meses y 3 días. Código LP:43. Ubicación: cuerpo E librero 3 estante b carpeta 2.",
        "adjuntos": ["docs/globo_terráqueo.pdf", "docs/foto_globo.jpg"]
    }
]

# ----------------------------------------------------------
# 🧠 VECTOR DE BÚSQUEDA TF-IDF (título + descripción)
# ----------------------------------------------------------
texts = [doc["titulo"] + " " + doc["descripcion"] for doc in documents]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# ----------------------------------------------------------
# 🔍 CAMPO DE BÚSQUEDA
# ----------------------------------------------------------
query = st.text_input("🔎 Escribe una palabra clave:", "")

# Inicializar estado para documento seleccionado
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# Vista de resultados
if st.session_state.selected_doc is None:
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
                if st.button(doc['titulo'], key=i):
                    st.session_state.selected_doc = i

        if not found:
            st.warning("No se encontraron resultados relevantes.")
    else:
        st.info("Escribe una palabra clave para comenzar la búsqueda.")

# Vista de documento seleccionado
else:
    doc = documents[st.session_state.selected_doc]
    st.markdown("---")
    st.subheader(f"📄 {doc['titulo']}")
    st.write(doc['descripcion'])
    st.write("Adjuntos disponibles:")
    for file in doc['adjuntos']:
        st.markdown(f"- <a href='{file}' target='_blank'>{file.split('/')[-1]}</a>", unsafe_allow_html=True)

    if st.button("🔙 Volver a resultados"):
        st.session_state.selected_doc = None

