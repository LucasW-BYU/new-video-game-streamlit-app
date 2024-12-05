import streamlit as st
import pandas as pd
import plotly.express as px

# Function to consolidate genres into broader categories
def consolidate_genres(df):
    genre_mapping = {
        'Simulator': 'Simulation',
        'Strategy': 'Strategy',
        "Hack and slash/Beat 'em up": 'Action',
        'Indie': 'Indie',
        'Role-playing (RPG)': 'RPG',
        'Sport': 'Sports & Racing',
        'Platform': 'Adventure',
        'Adventure': 'Adventure',
        'Shooter': 'Action',
        'Racing': 'Sports & Racing',
        'Card & Board Game': 'Puzzle & Casual',
        'Point-and-click': 'Adventure',
        'Puzzle': 'Puzzle & Casual',
        'Real Time Strategy (RTS)': 'Strategy',
        'Tactical': 'Action',
        'Visual Novel': 'RPG',
        'Quiz/Trivia': 'Puzzle & Casual',
        'Arcade': 'Arcade',
        'Turn-based strategy (TBS)': 'Strategy',
        'Music': 'Arcade',
        'Fighting': 'Action',
        'Pinball': 'Simulation',
        'MOBA': 'RPG',
    }
    def map_genres(genre_str):
        subgenres = genre_str.split(', ')
        mapped_genres = [genre_mapping.get(subgenre, subgenre) for subgenre in subgenres]
        return ', '.join(set(mapped_genres))  # Unique categories only
    df['genres'] = df['genres'].apply(map_genres)
    return df

@st.cache_data
def load_data():
    file_path = 'igdb_games_clean_data_sorted (1).csv' 
    data = pd.read_csv(file_path)
    data['release_date'] = pd.to_datetime(data['release_date'])
    data['year'] = data['release_date'].dt.year
    data = consolidate_genres(data)  
    return data

data = load_data()

broad_genres = sorted(set(genre for genres in data['genres'] for genre in genres.split(', ')))

st.title("Game Insights App")
st.write("Explore key insights from a dataset of video games, including ratings, genres, platforms, and release trends.")

st.sidebar.header("Filters")
selected_genre = st.sidebar.selectbox("Select Genre", options=broad_genres, index=0)
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(data['year'].min()),
    max_value=int(data['year'].max()),
    value=(2000, 2020)
)

tab1, tab2 = st.tabs(["Top-Rated Games by Genre", "Platform Popularity Over Time"])

with tab1:
    st.subheader("Top-Rated Games by Genre")
    genre_data = data[data['genres'].str.contains(selected_genre, case=False, na=False)]
    
    if genre_data.empty:
        st.warning(f"No data available for the selected genre: {selected_genre}")
    else:
        top_rated_games = genre_data.nlargest(10, 'rating')[['name', 'rating', 'platforms']]
        st.write(f"Top 10 Rated Games in Genre: {selected_genre}")
        st.dataframe(top_rated_games)

        fig1 = px.bar(
            top_rated_games,
            x='name',
            y='rating',
            title=f"Top 10 Rated Games in Genre: {selected_genre}",
            labels={'name': 'Game Name', 'rating': 'Rating'},
            text='rating'
        )
        fig1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig1)

with tab2:
    st.subheader("Platform Popularity Over Time")
    filtered_data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])].copy()
    
    if filtered_data.empty:
        st.warning(f"No data available for the selected year range: {year_range[0]} to {year_range[1]}")
    else:
        platform_mapping = {
            '64DD': 'Nintendo 64',
            'Game Boy Advance': 'Nintendo',
            'Nintendo 64': 'Nintendo 64',
            'Nintendo 3DS': 'Nintendo',
            'Nintendo Switch': 'Nintendo Switch',
            'PlayStation 2': 'PlayStation 2',
            'PlayStation 3': 'PlayStation 3',
            'PlayStation 4': 'PlayStation 4',
            'PlayStation 5': 'PlayStation 5',
            'PC (Microsoft Windows)': 'PC',
            'Linux': 'PC',
            'Mac': 'PC',
            'Android': 'Mobile',
            'iOS': 'Mobile',
            'Arcade': 'Arcade',
            'DVD Player': 'Other',
            'Neo Geo AES': 'Other',
            'Neo Geo MVS': 'Other',
            'Dreamcast': 'Other',
        }
        
        filtered_data['platforms'] = filtered_data['platforms'].apply(
            lambda x: ', '.join({platform_mapping.get(platform.strip(), platform.strip()) for platform in x.split(', ')})
        )

        platform_counts = filtered_data.explode('platforms')['platforms'].value_counts()

        top_platforms = platform_counts.head(10).index

        filtered_data = filtered_data[filtered_data['platforms'].apply(
            lambda x: any(platform in top_platforms for platform in x.split(', '))
        )]

        platform_counts = (
            filtered_data.explode('platforms')
            .groupby(['year', 'platforms'])
            .size()
            .reset_index(name='count')
        )

        fig2 = px.line(
            platform_counts,
            x='year',
            y='count',
            color='platforms',
            title=f"Platform Popularity from {year_range[0]} to {year_range[1]}",
            labels={'year': 'Year', 'count': 'Number of Games Released', 'platforms': 'Platform'}
        )
        st.plotly_chart(fig2)

st.sidebar.header("Explore Dataset")
st.write("Explore the full dataset:")
st.dataframe(data)

csv_data = data.to_csv(index=False)
st.sidebar.download_button(
    label="Download Dataset as CSV",
    data=csv_data,
    file_name='game_dataset.csv',
    mime='text/csv'
)
