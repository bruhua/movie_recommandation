import streamlit as st
import os
import pandas as pd

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



# Gestion des chemins

# Récupération du dossier courant
#current_folder = os.path.dirname(__file__)
# Récupération du dossier der données (dataset, images, ...)
# data_path = os.path.join(current_folder, "Dataframe")


# Fonction pour charger les données
@st.cache()
def load_data1():
    df_graph = pd.read_csv('https://raw.githubusercontent.com/bruhua/movie_recommandation/main/Dataframe/df_graph.csv')
    return df_graph

@st.cache()
def load_data2():
    final_film = pd.read_csv('https://raw.githubusercontent.com/bruhua/movie_recommandation/main/Dataframe/Final%20film.csv')
    return final_film

@st.cache()
def load_data3():
    df_exemple = pd.read_csv('https://raw.githubusercontent.com/bruhua/movie_recommandation/main/Dataframe/df_exemple.csv')
    return df_exemple

@st.cache()
def load_data4():
    df_overview = pd.read_csv('https://raw.githubusercontent.com/bruhua/movie_recommandation/main/Dataframe/df_overview.csv')
    return df_overview

@st.cache()
def load_data5():
    df_meta = pd.read_csv('https://raw.githubusercontent.com/bruhua/movie_recommandation/main/Dataframe/df_meta.csv')
    return df_meta


# Chargement des données
df_graph = load_data1()
final_film = load_data2()
df_exemple = load_data3()
df_overview = load_data4()
df_meta = load_data5()


# Sidebar


st.sidebar.title("Système de recommandations de films")

# Choix de la page
selection = st.sidebar.radio("", list(PAGES.keys()),key=range(0,3) )
page = PAGES[selection]
page.app(df_graph, final_film, df_exemple,df_overview,df_meta)

# PROFIL LINKEDIN
st.sidebar.markdown("""<hr style="height:2px;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.sidebar.markdown("**Profil Linkedin** :")
st.sidebar.markdown("[Bruno Huart](https://www.linkedin.com/in/bruno-huart-051459107/) ")
st.sidebar.markdown("""<hr style="height:2px;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

