import streamlit as st
import plotly.express as px


import demographic_filtering
import content_based_filtering
import content_based_filtering_v2
import presentation

# Pages
PAGES = {
    "Présentation du sujet" : presentation,
    "Demographic filtering": demographic_filtering,
    "Content based filtering" : content_based_filtering,
    "Content based filtering amélioré" :content_based_filtering_v2
}


def app(df_graph, final_film, df_exemple,df_overview,df_meta):
    st.title("1 . Présentation du sujet")

    st.subheader("Contexte")

    st.markdown("""
                E-commerce, musique, films ou séries en streaming... les systèmes de recommandations de produits ou de 
                contenus sont partout sans même d'ailleurs qu'on s'en rende compte ! """)
    st.markdown("""
                Ils permettent entre autres de générer des ventes additionnelles ou de fidéliser un prospect. 
                Dans cette app, nous nous pencherons sur une base de données fournie par TMDB et contenant près de 5000 films. 
                Parmis les informations disponibles sur ces films, nous avons le titre du film, l'année de sortie, le casting, le réalisateur, 
                la note moyenne du public...
                
                """)

    st.subheader("Objectif du projet")

    st.markdown("""
                Réussir à construire un système de recommandation efficace et pertinent. 
                Pour cela, 3 modèles sont proposés : 
                - le modèle [Demographic Filtering](demographic_filtering) """)
                if st.button("Demographic Filtering") : 
                    PAGES.keys(3)
     st.markdown("""
                - [Content based Filtering](content_based_filtering)
                - [Content Based Filtering v2](content_based_filtering_v2)
                """)
