import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------------------------------------
# 🪶 CONFIGURACIÓN BÁSICA DE LA APP
# ----------------------------------------------------------
st.set_page_config(page_title="Motor de búsqueda de restauración", page_icon="🔍")

st.title("🔍 Motor de búsqueda de restauración y conservación")
st.write("""
Esta es una versión de prueba de un motor de búsqueda para documentos y casos de restauración.  
Escribe palabras clave (por ejemplo: *Virgen del Carmen*, *ataque biológico*, *madera*, *dorado*)  
y el sistema te mostrará los casos más relacionados.
""")

# ----------------------------------------------------------
# 📄 DOCUMENTOS DE EJEMPLO
# (luego puedes reemplazar estos textos por tus fichas reales)
# ----------------------------------------------------------
documents = [
    {
        "titulo": "Virgen del Carmen",
        "descripcion": "Escultura en madera policromada restaurada en 2019. Presentaba grietas y pérdida de dorado.",
        "anio": "2019"
    },
    {
        "titulo": "San José",
        "descripcion": "Escultura en madera atacada por xilófagos. Tratamiento de consolidación estructural en 2020.",
        "anio": "2020"
    },
    {
        "titulo": "Retablo colonial",
        "descripcion": "Reintegración cromática de secciones doradas. Intervención realizada en 2021.",
        "anio": "2021"
    },
    {
        "titulo": "Lienzo de la Inmaculada Concepción",
        "descripcion": "Pintura al óleo sobre lienzo. Limpieza superficial y eliminación de barniz oxidado.",
        "anio": "2018"
    }
]

# ----------------------------------------------------------
# 🧠 CONFIGURAR VECTOR DE BÚSQUEDA TF-IDF
# ----------------------------------------------------------
texts = [doc["descripcion"] for doc in documents]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)

# ----------------------------------------------------------
# 🔎 CAMPO DE BÚSQUEDA
# ----------------------------------------------------------
query = st.text_input("Escribe tu búsqueda:", "")

if query:
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)[0]
    sorted_indices = similarities.argsort()[::-1]

    st.subheader(f"Resultados para: '{query}'")

    found = False
    for i in sorted_indices:
        if similarities[i] > 0:
            found = True
            doc = documents[i]
            st.markdown(f"""
            ### 🖼️ {doc['titulo']}
            **Año:** {doc['anio']}  
            **Descripción:** {doc['descripcion']}  
            **Similitud:** `{similarities[i]:.2f}`
            ---
            """)
    if not found:
        st.warning("No se encontraron resultados relevantes.")
else:
    st.info("Escribe una palabra clave para comenzar la búsqueda.")
