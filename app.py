import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Motor de Búsqueda CNCR", page_icon=None, layout="centered")

st.markdown("""
    <style>
    body { background-color: #cce7ff; color: #3a2e2e; font-family: 'Georgia', serif; }
    h1,h2,h3,h4 { font-family: 'Georgia', cursive; color: #2b2b2b; }
    .stTextInput input { border:1px solid #bfa98a; border-radius:10px; background-color:#fcfaf7; color:#3a2e2e;}
    .stButton button { background-color:#c8b6a6; color:white; border-radius:10px; border:none; font-size:16px; font-family:'Georgia', cursive;}
    .stButton button:hover { background-color:#9bbcc0; color:#fff;}
    </style>
""", unsafe_allow_html=True)

st.title("Motor de búsqueda de restauración y conservación")
st.write("Explora casos documentados del CNCR. Escribe palabras clave para buscar.")

# Documentos
documents = [
    {"titulo": "Nuevo Mapa de Chile – Código: 051-2",
     "descripcion": "Libro de ingreso 1 del año 1983. Impresión 1878. Ubicación: cuerpo E librero 3 estante b carpeta 6.",
     "adjuntos": [{"nombre":"PDF Mapa","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]},
    {"titulo": "Sra. Josefina Lira – Código: 053-2",
     "descripcion": "Pastel sobre tela fines XIX. Ingreso 1983. Ubicación: cuerpo E librero 3 estante b carpeta 5.",
     "adjuntos": [{"nombre":"PDF Josefina Lira","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]},
    {"titulo": "Carta de José Miguel Carrera – Código: 058-4",
     "descripcion": "Ingreso 1985. Historia: escrita por José Miguel Carrera. Fecha carta 1821. Ubicación: cuerpo E librero 3 estante b carpeta 1.",
     "adjuntos": [{"nombre":"Carta PDF","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]},
    {"titulo": "Litografía Lago Vichuquén de Llico – Código: 059-4",
     "descripcion": "Detalle de autor y técnica, salida 12 mayo 1986. Fotos digitalizadas. Ubicación: cuerpo E librero 3 estante b carpeta 9.",
     "adjuntos": [{"nombre":"PDF Litografía","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]},
    {"titulo": "Desnudo por Jean Jacques Henner – Código: 003-14",
     "descripcion": "Ingreso 20 abril 1995, salida 16 noviembre 1995. Fotos no digitales. Ubicación: cuerpo E librero 2 estante d carpeta 6.",
     "adjuntos": [{"nombre":"PDF Henner","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]},
    {"titulo": "Naturaleza muerta por Harnett – Código: 012-14",
     "descripcion": "Ingreso 2 junio 1995, salida 17 julio 1995. Ubicación: cuerpo E librero 8 estante a carpeta 2.",
     "adjuntos": [{"nombre":"PDF Harnett","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]},
    {"titulo": "Globo terráqueo – Código: 024-14",
     "descripcion": "Técnicas variadas. Estadía 4 meses 3 días. Código LP:43. Ubicación: cuerpo E librero 3 estante b carpeta 2.",
     "adjuntos": [{"nombre":"PDF Globo","url":"https://raw.githubusercontent.com/josefinnatc-gif/buscador-rstrcn/main/docs/ejemplo.pdf"}]}
]

# TF-IDF
texts = [d["titulo"] + " " + d["descripcion"] for d in documents]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# Estado
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# Vista principal o documento seleccionado
if st.session_state.selected_doc is None:
    query = st.text_input("🔎 Palabra clave:", key="input_query")
    if query:
        sims = cosine_similarity(vectorizer.transform([query]), tfidf_matrix)[0]
        sorted_idx = sims.argsort()[::-1]
        st.markdown("---")
        st.subheader(f"Resultados para: *{query}*")
        found = False
        for i in sorted_idx:
            if sims[i] > 0:
                found = True
                doc = documents[i]
                if st.button(doc["titulo"], key=f"btn_{i}"):
                    st.session_state.selected_doc = i
        if not found:
            st.warning("No se encontraron resultados.")
    else:
        st.info("Escribe algo para buscar.")

else:
    doc = documents[st.session_state.selected_doc]
    st.markdown("---")
    st.subheader(f"📄 {doc['titulo']}")
    st.write(doc["descripcion"])

    st.subheader("Adjuntos:")
    for idx, archivo in enumerate(doc.get("adjuntos", [])):
        st.markdown(f"- [{archivo['nombre']}]({archivo['url']}) ⤴️", unsafe_allow_html=True)

    if st.button("🔙 Volver a resultados", key="volver_resultados"):
        st.session_state.selected_doc = None
