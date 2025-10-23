import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------
# 🌿 CONFIGURACIÓN GENERAL
# ----------------------------------------------------------
st.set_page_config(page_title="Motor de Búsqueda CNCR", page_icon="📜", layout="centered")

# Colores y estilo
st.markdown("""
    <style>
    body {
        background-color: #f5f1e8; /* beige suave */
        color: #3a2e2e; /* marrón oscuro */
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
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# 🖋️ TÍTULO Y DESCRIPCIÓN
# ----------------------------------------------------------
st.title("📜 Motor de búsqueda de restauración y conservación")
st.write("""
Este motor permite explorar casos documentados de restauración del CNCR.  
Escribe palabras clave (por ejemplo: *óleo*, *salida 1986*, *pastel sobre tela*, *Santiago*)  
y el sistema te mostrará los casos más relacionados.
""")

# ----------------------------------------------------------
# 📁 DOCUMENTOS REALES
# ----------------------------------------------------------
documents = [
    {
        "titulo": "Nuevo Mapa de Chile – Código: 051-2",
        "descripcion": "Libro de ingreso 1 del año 1983. Impresión del año 1878 proveniente de la biblioteca de Santiago. Salida del centro en 2005. No confirmada presencia de foto, requiere búsqueda análoga. ORGANIZAR FECHA."
    },
    {
        "titulo": "Sra. Josefina Lira – Código: 053-2",
        "descripcion": "Pastel sobre tela de fines del siglo XIX, procedente del Museo de Bellas Artes. Ingreso en 1983, sin fecha de salida. Caso importante por conectividad con otros documentos asociados."
    },
    {
        "titulo": "Carta de José Miguel Carrera – Código: 058-4",
        "descripcion": "Ingreso en 1985. Cuenta con información de salida y nombres de restauradores. Sección 'historia': fue escrita por José Miguel Carrera en Mendoza antes de morir y enviada a Santiago en una caja de fósforos. Fecha de la carta: 1821."
    },
    {
        "titulo": "Litografía Lago Vichuquén de Llico – Código: 059-4",
        "descripcion": "Detalle en secciones de autor y técnica, incluye descripción de color. Nombre de la restauradora registrado. Salida el 12 de mayo de 1986. Código LP: 108. Posee fotos digitalizadas."
    },
    {
        "titulo": "Desnudo por Jean Jacques Henner – Código: 003-14",
        "descripcion": "Incluye categoría 'Número inventario museo'. Ingreso el 20 de abril de 1995 y salida el 16 de noviembre del mismo año. Fotos no digitales. UPGD:1004 LP:46."
    },
    {
        "titulo": "Naturaleza muerta por Harnett – Código: 012-14",
        "descripcion": "Restauradora distinta a las anteriores. Ingreso el 2 de junio de 1995 y salida el 17 de julio de 1995, permaneció 1 mes y 15 días. Código LP:10."
    },
    {
        "titulo": "Globo terráqueo – Código: 024-14",
        "descripcion": "Técnicas: varillas de madera, papel maché, yeso, papel impreso y protección. Estancia de 4 meses y 3 días. Código LP:43."
    }
]

# ----------------------------------------------------------
# 🧠 CONFIGURAR VECTOR DE BÚSQUEDA TF-IDF
# ----------------------------------------------------------
texts = [doc["descripcion"] for doc in documents]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# ----------------------------------------------------------
# 🔍 CAMPO DE BÚSQUEDA
# ----------------------------------------------------------
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
            st.markdown(f"""
            <div style='background-color:#faf6f0;padding:15px;border-radius:12px;margin-bottom:10px;'>
                <h4 style='color:#3a2e2e;'>{doc['titulo']}</h4>
                <p style='font-size:15px;color:#3a2e2e;'>{doc['descripcion']}</p>
                <p style='color:#7d7063;'><em>Similitud: {similarities[i]:.2f}</em></p>
            </div>
            """, unsafe_allow_html=True)
    if not found:
        st.warning("No se encontraron resultados relevantes.")
else:
    st.info("Escribe una palabra clave para comenzar la búsqueda.")

