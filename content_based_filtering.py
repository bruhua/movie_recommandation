import streamlit as st
import pandas as pd
import plotly.express as px
# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image

import time

import demographic_filtering
import content_based_filtering_v2
import presentation



def app(df_graph, final_film, df_exemple,df_overview,df_meta):
    st.title("3 . Content Based Filtering")

    st.subheader("Qu'est ce que c'est ? ")
    st.markdown("""
                Ce système de recommandation est plus élaboré que le Demographic Filtering : le moteur va chercher des films similaires à ce que vous avez déjà 
                 regardé. Il peut se baser sur le résumé du film, les acteurs, le réalisateur, le genre... """)

    st.subheader("Démonstration d'un système basé uniquement sur le résumé des films")


    st.markdown("""
                - le résumé de chaque film :  """)

    st.write(df_overview[['title','overview']].head())


    st.markdown("""
                -  ce que le moteur de recommandation propose :  """)


    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')
    # Replace NaN with an empty string
    df2=df_overview.copy()
    df2['overview'] = df2['overview'].fillna('')
    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(df2['overview'])
    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # Construct a reverse map of indices and movie titles
    indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

    # Function that takes in movie title as input and outputs most similar movies
    def get_recommandations(title, cosine_sim=cosine_sim):
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
        film_reco = pd.DataFrame(df2['title'].iloc[movie_indices]).reset_index()
        film_reco = film_reco.drop('index', axis=1)
        pct_reco = pd.DataFrame(sim_scores)
        pct_reco.rename(columns={0: 'index',
                                 1: 'result'}, inplace=True)
        pct_reco = pct_reco.drop('index', axis=1)
        pct_reco['% de reco'] = round(pct_reco['result'] * 100, 2)
        pct_reco = pct_reco.drop('result', axis=1)

        final_reco = pd.concat([film_reco, pct_reco], axis=1)

        # Return the top 10 most similar movies
        return final_reco

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
    df_overview['title2'] = df_overview['title'].apply(title_scrap)

        # Fonction qui chercher les affiches des films recommandés
    def find_image(film):
        try : 
            url = 'https://www.themoviedb.org/search?language=en&query='
            prefix_url = 'https://www.themoviedb.org'
            name = df_meta.loc[df_meta['title'] == film]['title2'].values
            final_url = url + name
            page_LC = urlopen(final_url[0])
            soup = BeautifulSoup(page_LC, 'html.parser')
            # Récupération de l'affiche du film
            image_tags = soup.find_all('img', class_='poster')
            links = []
            for image_tag in image_tags:
                links.append(image_tag['src'])
            suffixe_url = links[0]
            urllib.request.urlretrieve(prefix_url + suffixe_url, ".jpg")
            # Affichage
            dimensions = (5000, 2000)
            i = Image.open('.jpg')
            i.thumbnail(dimensions)
            st.image(i,width=130  )
        except (IndexError,KeyError) :
            print("le film {} n'a pas l'air d'avoir d'affiche disponible sur le site TMDB!")



    # Interactivité : calcul des recommandations + affichages des affiches
    listing_selectionnable2 = df_overview.sort_values(by='popularity', ascending=False).head(100)['title']
    film_selectionne = st.selectbox('Choisir un film parmi les 100 films les plus populaires', listing_selectionnable2)

    if st.button('Montre-moi les recommandations !'):

        with st.spinner(text="Work in progress...") :
            st.write("**Film choisi :** ")
            find_image(film_selectionne)

            st.write("")
            st.write("**Les films recommandés :** ")

            # affichage en colonnes
            col1, col2, col3 = st.columns(3)
            title1 = get_recommandations(film_selectionne, cosine_sim).head(1)['title'].values[0]
            title2 = get_recommandations(film_selectionne, cosine_sim).head(2).tail(1)['title'].values[0]
            title3 = get_recommandations(film_selectionne, cosine_sim).head(3).tail(1)['title'].values[0]
            title4 = get_recommandations(film_selectionne, cosine_sim).head(4).tail(1)['title'].values[0]
            title5 = get_recommandations(film_selectionne, cosine_sim).head(5).tail(1)['title'].values[0]
            title6 = get_recommandations(film_selectionne, cosine_sim).head(6).tail(1)['title'].values[0]

            with col1 :
                st.write(title1, "- Taux de recommandation :", get_recommandations(film_selectionne, cosine_sim).head(1)['% de reco'].values[0])
                find_image(title1)

                st.write(title4, "- Taux de recommandation :", get_recommandations(film_selectionne, cosine_sim).loc[get_recommandations(film_selectionne, cosine_sim)['title']==title4]['% de reco'].values[0])
                find_image(title4)

            with col2 :
                st.write(title2, "- Taux de recommandation :", get_recommandations(film_selectionne, cosine_sim).loc[get_recommandations(film_selectionne, cosine_sim)['title']==title2]['% de reco'].values[0])
                find_image(title2)

                st.write(title5, "- Taux de recommandation :", get_recommandations(film_selectionne, cosine_sim).loc[get_recommandations(film_selectionne, cosine_sim)['title']==title5]['% de reco'].values[0])
                find_image(title5)


            with col3 :
                st.write(title3, "- Taux de recommandation :", get_recommandations(film_selectionne, cosine_sim).loc[get_recommandations(film_selectionne, cosine_sim)['title']==title3]['% de reco'].values[0])
                find_image(title3)

                st.write(title6, "- Taux de recommandation :", get_recommandations(film_selectionne, cosine_sim).loc[get_recommandations(film_selectionne, cosine_sim)['title']==title6]['% de reco'].values[0])
                find_image(title6)
        st.success('Done!')

    st.subheader("Est-ce que ça fonctionne ? ")


    st.markdown("""
                En se basant uniquement sur le résumé, certains résultats sont cohérents tandis que d'autres sont assez étranges...""")
    st.markdown("""
                Ci-dessous les recommandations avec le film Jurassic World en entrée. """)
    st.markdown("""
                Le système nous propose d'autres films type "Jurassic" ce qui parait cohérent mais avec des taux de recommandations assez faibles. 
                Les films suivants sont à priori loin de l'univers des dinosaures et les taux de recommandations proposés ne sont pas beaucoup 
                plus faibles que ceux proposés pour les films "Jurassic". """)

    st.write(get_recommandations("Jurassic World"))

    st.markdown(""" **Le prochain modèle [Content based filtering amélioré](content_based_filtering_v2) va pousser plus loin cette démarche !** """)
