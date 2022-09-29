import streamlit as st
import plotly.express as px


import demographic_filtering
import content_based_filtering
import content_based_filtering_v2
import presentation



def app(df_graph, final_film, df_exemple,df_overview,df_meta):

        
    st.title("Système de recommandations de films /   1. Présentation du sujet")

    st.subheader("Contexte")

    st.markdown("""
                E-commerce, musique, films ou séries en streaming... les systèmes de recommandations de produits ou de 
                contenus sont partout sans même d'ailleurs qu'on s'en rende compte ! """)
    st.markdown("""
                Ils permettent entre autres de générer des ventes additionnelles ou de fidéliser un prospect. 
                Dans cette app, nous nous pencherons sur une base de données fournie par TMDB et contenant près de 5000 films. 
                Parmi les informations disponibles sur ces films, nous avons le titre du film, l'année de sortie, le casting, le réalisateur, 
                la note moyenne du public...
                
                """)

    st.subheader("Objectif du projet")

    st.markdown("""
                Réussir à construire un système de recommandation efficace et pertinent. 
                Pour cela, 3 modèles sont proposés : 
                - le modèle Demographic Filtering 
                - le modèle Content based Filtering
                - le même modèle Content Based Filtering en version améliorée
                """)
    
    
    st.markdown(""" _Vous êtes sur mobile ? Le menu de navigation se trouve au niveau de la flèche en haut en gauche_""") 
    
    



