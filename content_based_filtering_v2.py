import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image

import demographic_filtering
import content_based_filtering
import presentation


def app(df_graph, final_film, df_exemple,df_overview,df_meta):

    # PRESENTATION
    st.title("4 . Content Based Filtering amélioré")

    st.subheader("En quoi est-il amélioré ? ")
    st.markdown("""
                On a vu que le système de recommandation basé uniquement sur le résumé des films avait ses limites. 
                Ce nouveau système va se baser désormais sur les informations "annexes" au film : """)
    st.markdown("""
     - le réalisateur """)
    st.markdown("""
     - les acteurs """)
    st.markdown("""
     - le genre""")
    st.markdown("""
     - les mots clés ("spy" ou "secret agent" pour un film James Bond) """)


    st.write(df_exemple[['title', 'cast', 'director', 'keywords', 'genres']].head(3))


    # DEMO
    st.subheader("Démonstration")

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df_meta['metadonnees'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    # Reset index of our main DataFrame and construct reverse mapping as before
    df_meta = df_meta.reset_index()
    indices = pd.Series(df_meta.index, index=df_meta['title'])

    # Fonction de recommandations
    def get_recommandations2(title, cosine_sim=cosine_sim2):
        # Get the index of the movie that matches the title
        idx = indices[title]
        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]
        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
        # Mise en forme d'un df avec nom du film et pct de recommandations
        film_reco = pd.DataFrame(df_meta['title'].iloc[movie_indices]).reset_index()
        film_reco = film_reco.drop('index', axis=1)
        pct_reco = pd.DataFrame(sim_scores)
        pct_reco.rename(columns={0: 'index',
                                 1: 'result'}, inplace=True)
        pct_reco = pct_reco.drop('index', axis=1)
        pct_reco['% de reco'] = round(pct_reco['result'] * 100, 2)
        pct_reco = pct_reco.drop('result', axis=1)
        final_reco2 = pd.concat([film_reco, pct_reco], axis=1)
        # Return the top 10 most similar movies
        return final_reco2

    # Mise au format des titres pour la recherche scrapping
    # ex : The dark knight >> the+dark+knight
    def title_scrap(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "+")) for i in x]
        else:
            # Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", "+"))
            else:
                return ''
    # application de la fonction
    df_meta['title2'] = df_meta['title'].apply(title_scrap)

    # Fonction qui chercher les affiches des films recommandés
    def find_image(film):
        url = 'https://www.themoviedb.org/search?language=en&query='
        prefix_url = 'https://www.themoviedb.org'
        name = df_meta.loc[df_meta['title'] == film]['title2'].values
        final_url = url + name
        page_LC = urlopen(final_url[0])
        soup = BeautifulSoup(page_LC, 'html.parser')
        try:
            # Récupération de l'affiche du film
            image_tags = soup.find_all('img', class_='poster')
            links = []
            for image_tag in image_tags:
                links.append(image_tag['src'])
            suffixe_url = links[0]
            urllib.request.urlretrieve(suffixe_url, ".jpg")
            # Affichage
            dimensions = (5000, 2000)
            i = Image.open('.jpg')
            i.thumbnail(dimensions)
            st.image(i,width=130  )
        except (IndexError,KeyError) :
            st.write(f"le film {film} n'a pas l'air d'avoir d'affiche disponible sur le site TMDB!")

    # Interactivité : calcul des recommandations + affichages des affiches
    listing_selectionnable3 = df_meta.sort_values(by='popularity', ascending=False).head(100)['title']
    film_selectionne = st.selectbox('Choisir un film parmi les 100 films les plus populaires', listing_selectionnable3)


    if st.button('Montre-moi les recommandations !'):
        with st.spinner(text="Work in progress...") :
            st.write("**Film choisi :** ", film_selectionne)
            find_image(film_selectionne)

            st.write("")
            st.write("**Les films recommandés :** ")
            #for title in get_recommandations2(film_selectionne, cosine_sim2)['title'].values:
             #   st.write(title, "- Taux de recommandation :",get_recommandations2(film_selectionne, cosine_sim2).loc[get_recommandations2(film_selectionne, cosine_sim2)['title']==title]['% de reco'].values[0])
             #   find_image(title)
            #st.write(reco2)

            # affichage en colonnes
            col1, col2, col3 = st.columns(3)
            title1 = get_recommandations2(film_selectionne, cosine_sim2).head(1)['title'].values[0]
            title2 = get_recommandations2(film_selectionne, cosine_sim2).head(2).tail(1)['title'].values[0]
            title3 = get_recommandations2(film_selectionne, cosine_sim2).head(3).tail(1)['title'].values[0]
            title4 = get_recommandations2(film_selectionne, cosine_sim2).head(4).tail(1)['title'].values[0]
            title5 = get_recommandations2(film_selectionne, cosine_sim2).head(5).tail(1)['title'].values[0]
            title6 = get_recommandations2(film_selectionne, cosine_sim2).head(6).tail(1)['title'].values[0]

            with col1 :
                st.write(title1, "- Taux de recommandation :", get_recommandations2(film_selectionne, cosine_sim2).head(1)['% de reco'].values[0])
                find_image(title1)

                st.write(title4, "- Taux de recommandation :", get_recommandations2(film_selectionne, cosine_sim2).loc[get_recommandations2(film_selectionne, cosine_sim2)['title']==title4]['% de reco'].values[0])
                find_image(title4)

            with col2 :
                st.write(title2, "- Taux de recommandation :", get_recommandations2(film_selectionne, cosine_sim2).loc[get_recommandations2(film_selectionne, cosine_sim2)['title']==title2]['% de reco'].values[0])
                find_image(title2)

                st.write(title5, "- Taux de recommandation :", get_recommandations2(film_selectionne, cosine_sim2).loc[get_recommandations2(film_selectionne, cosine_sim2)['title']==title5]['% de reco'].values[0])
                find_image(title5)


            with col3 :
                st.write(title3, "- Taux de recommandation :", get_recommandations2(film_selectionne, cosine_sim2).loc[get_recommandations2(film_selectionne, cosine_sim2)['title']==title3]['% de reco'].values[0])
                find_image(title3)

                st.write(title6, "- Taux de recommandation :", get_recommandations2(film_selectionne, cosine_sim2).loc[get_recommandations2(film_selectionne, cosine_sim2)['title']==title6]['% de reco'].values[0])
                find_image(title6)
        st.success('Done!')



    st.subheader("Est-ce que ça fonctionne ? ")


    st.markdown("""
                **Pour une majorité de films, les recommandations sont plus pertinentes !**""")
    st.markdown("""
                Le système ressort soit des films du même genre, soit des suites, soit des films avec le même acteur principal ou encore le même réalisateur.""")
    st.markdown("""
                Autre changement : les taux de recommandations sont plus élevés que précédemment. Il y a plus de chances pour que les films 
                proposés nous plaisent !""")
    st.markdown("""
                   **Nous pouvons désormais combiner ce modèle ainsi que le 1er modèle basé sur le score des films pour proposer toujours 
                   davantage de films à nos usagers.** """)

