import streamlit as st
import plotly.express as px


import content_based_filtering
import content_based_filtering_v2
import presentation

def app(df_graph, final_film, df_exemple,df_overview,df_meta):
    st.title("2 . Demographic Filtering")

    st.subheader("Qu'est ce que c'est ? ")
    st.markdown("""
                Derrière ce nom obscur se cache en fait le système de recommandation le plus simple possible : l'idée sous-jacente 
                est que les films les plus populaires ou ayant les meilleures critiques devraient plaire au plus grand nombre. """)

    st.markdown("""
                **Le système les recommande donc à tout le monde !** 
                    """)


    st.markdown("""
                Il y a quand même une petite subtilité visible sur les 2 graphiques ci-dessous : 
                    """)


    # FIlm les plus populaires (popularity)
    x = df_graph.sort_values(by='popularity', ascending=False).head(10)['title']
    y = df_graph.sort_values(by='popularity', ascending=False).head(10)['popularity']
    fig = px.bar(df_graph,
                 x=x
                 , y=y,
                 title="TOP 10 des films les plus populaires",
                 template='seaborn')
    fig.update_xaxes(title=' ')
    fig.update_yaxes(title='Popularité du film')

    st.plotly_chart(fig)

    st.markdown("""
                ==> Les films les plus populaires sont bien connus de tous :Deadpool, les Minions ...
                    """)

    # FIlm avec les meilleures notes (vote_average)
    x = df_graph.sort_values(by='vote_average', ascending=False).head(10)['title']
    y = df_graph.sort_values(by='vote_average', ascending=False).head(10)['vote_average']
    fig = px.bar(df_graph,
                 x=x
                 , y=y,
                 title="TOP 10 des films les mieux notés",
                 template='seaborn')  # color = CO2_emission_per_country.index,)
    fig.update_xaxes(title=' ')
    fig.update_yaxes(title='Note moyenne')
    st.plotly_chart(fig)

    st.markdown("""
                ==> ... par contre les films les mieux notés peuvent être complètement inconnus ! (exemeple : un film avec une note moyenne de 10 et 3 votants)
                    """)


    st.subheader("La solution des systèmes de recommandations")


    st.markdown("""
                Les systèmes de recommandations vont prendre alors en compte quelques indicateurs pour créer une note plus fiable : 
                    """)
    st.markdown(""" - La note moyenne obtenue par un film (ex : "Le Parrain" a une note moyenne de 8.4 sur 10)""")
    st.markdown(""" - Le nombre de votants pour ce même film (toujours "Le Parrain", 5893 votants )""")
    st.markdown(""" - La note moyenne obtenue sur l'ensemble des films (dans notre base, la note moyenne globale est de 6)""")

    st.markdown(""" **==> Les films avec trop peu de votants sont exclus du calcul de cette nouvelle note.**""")
    st.markdown(""" **==> Dans notre cas, nous gardons uniquement les films avec au moins 730 votants (3e quartile)** """)

    st.markdown("""""")
    st.markdown(""" Le TOP 10 des meilleurs films devient ainsi :  """)


    # Film avec le meilleur score basé sur la note calculé
    x = final_film.sort_values(by='score', ascending=False).head(10)['title']
    y = final_film.sort_values(by='score', ascending=False).head(10)['score']
    fig = px.bar(final_film,
                 x=x
                 , y=y,
                 title="TOP 10 des films avec les meilleurs scores",
                 template='seaborn')  # color = CO2_emission_per_country.index,)
    fig.update_xaxes(title=' ')
    fig.update_yaxes(title='Score')
    st.plotly_chart(fig)

    st.markdown(""" **Ces films sont tous bien notés et très connus !** """)
    st.markdown(""" **Ainsi quelque soit vos préférences ou votre historique de visionnage, 
        ces films vous seront recommandés tout simplement car ils sont bien 
            notés et populaires.** """)


    st.subheader("Et ensuite ? ")

    st.markdown(""" Ce 1er système de recommandation est assez basique et surtout il ne propose aucune 
     personnalisation. Peu importe vos préférences ou votre historique de visionnage, il propose la même chose à tout le monde.""")
    st.markdown(""" **Le prochain modèle [Content based filtering](content_based_filtering) devrait commencer à améliorer nos recommandations !** """)
