import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px

import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)


def getData():
    res = requests.get('http://127.0.0.1:5000/meteorite/get_data')
    if res.status_code == 200:
        return res.json()
    else:
        print('Error')
        return None


myData = getData()
df = pd.DataFrame(myData['content'])
if len(df) == 0:
    st.title("Aucune données retrouvées.")
else:

    st.title("Etude des météorites dans le monde")

    st.title("Données sur les météorites provenant de la NASA")
    st.write(df)

    # Graphique pour la distributions des météorites en fonction de leurs masses
    st.title('Distribution des masses des météorites')
    bins = [100, 1000, 10000, 100000, 1000000]
    plt.figure(figsize=(10, 6))
    plt.hist(df['mass'], bins=bins, color='skyblue', edgecolor='black')
    plt.xscale('log')
    plt.xlabel('Masse (g)')
    plt.ylabel('Nombre de météorites')
    plt.title('Distribution des masses des météorites')
    st.pyplot(plt)

    # Relation entre le type de météorite et sa masse
    st.title("Relation entre le type et la masse de la météorite")
    grouped_data = df.groupby('recclass')
    min_mass_per_class = grouped_data['mass'].min()
    max_mass_per_class = grouped_data['mass'].max()
    min_max_mass_per_class = pd.DataFrame(
        {'Min Mass': min_mass_per_class, 'Max Mass': max_mass_per_class})
    min_max_mass_per_class_sorted = min_max_mass_per_class.sort_values(
        by='Max Mass', ascending=False)
    top_10_classes_min_max = min_max_mass_per_class_sorted.head(10)
    plt.figure(figsize=(12, 8))
    sns.heatmap(top_10_classes_min_max, annot=True, cmap='YlGnBu', fmt='.0f')
    plt.xlabel('Type de météorite')
    plt.ylabel('Masse (g)')
    plt.title(
        'Valeur minimale et maximale de la masse par type de météorite (Top 10)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

    # Graphique pour la récurrence des types de météorites
    st.title('Graphique pour la récurrence des types de météorites.')
    df_most_recurrent_meteorite = df
    type_counts = df_most_recurrent_meteorite['recclass'].value_counts().head()
    fig, ax_meteorite = plt.subplots(figsize=(10, 6))
    ax_meteorite.barh(type_counts.index, type_counts.values,
                      align='edge', color='#007acc', zorder=3)
    for index, value in enumerate(type_counts.values):
        ax_meteorite.text(
            value + 0.5, index, f"{value}", color='#222222', ha='left', va='center', fontsize=12)
    ax_meteorite.set_xlabel('Nombre d\'occurrences',
                            fontsize=14, color='#222222')
    ax_meteorite.set_ylabel('Type de météorite', fontsize=14, color='#222222')
    ax_meteorite.set_title('Types de météorites les plus récurrents',
                           fontsize=16, color='#222222', pad=20)
    ax_meteorite.tick_params(axis='both', which='major',
                             labelsize=12, colors='#222222')
    ax_meteorite.xaxis.grid(True, linestyle='--', color='#dddddd', zorder=0)
    ax_meteorite.spines['top'].set_visible(False)
    ax_meteorite.spines['right'].set_visible(False)
    ax_meteorite.spines['left'].set_color('#222222')
    ax_meteorite.spines['bottom'].set_color('#222222')
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    st.pyplot(fig)

    # Analyse des météorites par classification
    top_classes = df['recclass'].value_counts().head(5)
    st.title("Analyse des 5 catégories de météorites avec le nombre de recensement")
    plt.figure(figsize=(10, 6))
    top_classes.plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Répartition des 5 premiers types de météorites par classification')
    plt.ylabel('')
    st.pyplot(plt)

    # Comparaison des chutes de météorite par pays
    st.title('Comparaison des chutes de météorite par pays :')
    df_found_meteorites = df.loc[df['fall'] == 'Found'].copy()
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf = gpd.GeoDataFrame(df_found_meteorites, geometry=gpd.points_from_xy(
        df_found_meteorites.reclong, df_found_meteorites.reclat))
    fig2, ax = plt.subplots(figsize=(12, 8))
    world.plot(ax=ax, color='#F0F0F0', edgecolor='black')
    gdf.plot(ax=ax, color='#FF5733', markersize=7,
             alpha=0.7, marker='o', label='Météorites')
    ax.legend()
    ax.set_title('Carte des emplacements des météorites', fontsize=18)
    ax.axis('off')
    ax.annotate("Source : Données provenant d'un dataset de la NASA", xy=(0.1, .08), xycoords='figure fraction',
                horizontalalignment='left', verticalalignment='top', fontsize=10, color='#555555')
    plt.tight_layout()
    st.pyplot(fig2)

    # Nombre de météorites par siècles
    st.title("Nombre de météorites par siècles")
    df['century'] = ((df['year'] - 1) // 100) + 1
    meteorites_per_century = df['century'].value_counts(
    ).sort_index().reset_index()
    meteorites_per_century.columns = ['century', 'count']
    fig3 = px.bar(meteorites_per_century, x='century', y='count', labels={
        'century': 'Siècle', 'count': 'Nombre de météorites'}, title='Nombre de météorites par siècle')
    fig3.update_traces(
        text=meteorites_per_century['count'], textposition='outside')
    # Augmenter de 10% pour permettre une meilleure visualisation
    fig3.update_yaxes(range=[0, meteorites_per_century['count'].max() * 1.1])
    st.plotly_chart(fig3)

    # Nombre de météorites par échelle de 10 ans durant le 20ème siècle
    st.title("Nombre de météorites par échelle de 10 ans durant le 20ème siècle")
    most_meteorites_century = meteorites_per_century.loc[meteorites_per_century['count'].idxmax(
    ), 'century']
    df_most_meteorites_century = df[df['century'] == most_meteorites_century]
    df_most_meteorites_century['decade'] = (
        (df_most_meteorites_century['year'] - 1) // 10) * 10
    meteorites_per_decade = df_most_meteorites_century['decade'].value_counts(
    ).sort_index().reset_index()
    meteorites_per_decade.columns = ['decade', 'count']
    fig4 = px.bar(meteorites_per_decade, x='decade', y='count', labels={
        'decade': 'Décennie', 'count': 'Nombre de météorites'}, title=f'Répartition des météorites par décennie ({most_meteorites_century}e siècle)')
    fig4.update_traces(
        text=meteorites_per_decade['count'], textposition='outside')
    st.plotly_chart(fig4)

    # Répartition des météorites tombées pendant le 20ème siècle
    st.title("Répartition des météorites tombées pendant le 20ème siècle")
    df_20th_century = df[(df['year'] >= 1901) & (df['year'] <= 2000)]
    gdf = gpd.GeoDataFrame(df_20th_century, geometry=gpd.points_from_xy(
        df_20th_century.reclong, df_20th_century.reclat))
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    fig5, ax = plt.subplots(figsize=(12, 8))
    world.plot(ax=ax, color='#f0f0f0', edgecolor='#bfbfbf')
    gdf.plot(ax=ax, color='#e31a1c', markersize=8,
             marker='o', label='Météorites')
    plt.title('Répartition des météorites durant le 20ème siècle',
              fontsize=18, fontweight='bold', pad=20)
    plt.legend(markerscale=2, fontsize=12)
    plt.xlabel('Longitude', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.grid(color='#d9d9d9', linestyle='--')
    st.pyplot(fig5)
