import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.write("This section highlights the top-rated games in the selected genre based on ratings.")
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
    st.write("This chart shows the number of games released on each platform over the selected time period.")
    
    # Filter data based on the selected year range
    filtered_data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])].copy()
    
    if filtered_data.empty:
        st.warning(f"No data available for the selected year range: {year_range[0]} to {year_range[1]}")
    else:
        platform_mapping = {
            'Nintendo Switch': 'Nintendo',
            'Nintendo 64': 'Nintendo',
            'Nintendo 3DS': 'Nintendo',
            'New Nintendo 3DS': 'Nintendo',
            'Nintendo DS': 'Nintendo',
            'Nintendo DSi': 'Nintendo',
            'Game Boy': 'Nintendo',
            'Game Boy Advance': 'Nintendo',
            'Game Boy Color': 'Nintendo',
            'Nintendo Entertainment System': 'Nintendo',
            'Super Nintendo Entertainment System': 'Nintendo',
            'Nintendo GameCube': 'Nintendo',
            'Family Computer': 'Nintendo',
            'Family Computer Disk System': 'Nintendo',
            'Satellaview': 'Nintendo',
            
            'PlayStation': 'PlayStation',
            'PlayStation 2': 'PlayStation',
            'PlayStation 3': 'PlayStation',
            'PlayStation 4': 'PlayStation',
            'PlayStation 5': 'PlayStation',
            'PlayStation Portable': 'PlayStation',
            'PlayStation Vita': 'PlayStation',
            'PlayStation VR': 'PlayStation',
            'PlayStation VR2': 'PlayStation',
            
            'Xbox': 'Xbox',
            'Xbox 360': 'Xbox',
            'Xbox One': 'Xbox',
            'Xbox Series X|S': 'Xbox',
            
            'PC (Microsoft Windows)': 'PC',
            'Linux': 'PC',
            'Mac': 'PC',
            'SteamVR': 'PC',
            'Windows Mixed Reality': 'PC',
            
            'Android': 'Mobile',
            'iOS': 'Mobile',
            'Windows Phone': 'Mobile',
            'Windows Mobile': 'Mobile',
            'Palm OS': 'Mobile',
            'Meta Quest 2': 'Mobile',
            'Meta Quest 3': 'Mobile',
            'Oculus Go': 'Mobile',
            'Oculus Quest': 'Mobile',
            'Oculus Rift': 'Mobile',
            'Daydream': 'Mobile',
            'BlackBerry OS': 'Mobile',
            'Legacy Mobile Device': 'Mobile',
            
            'Arcade': 'Arcade',
            'Neo Geo AES': 'Arcade',
            'Neo Geo CD': 'Arcade',
            'Neo Geo MVS': 'Arcade',
            'SG-1000': 'Arcade',
            
            'Dreamcast': 'Other',
            'Sega Game Gear': 'Other',
            'Sega Mega Drive/Genesis': 'Other',
            'Sega Master System/Mark III': 'Other',
            'Sega Saturn': 'Other',
            'Sega CD': 'Other',
            'Sega 32X': 'Other',
            'TurboGrafx-16/PC Engine': 'Other',
            'TurboGrafx-16/PC Engine CD': 'Other',
            'Vectrex': 'Other',
            'Zeebo': 'Other',
            'Philips CD-i': 'Other',
            'DVD Player': 'Other',
            'Blu-ray Player': 'Other',
            '3DO Interactive Multiplayer': 'Other',
            'ColecoVision': 'Other',
            'Atari 2600': 'Other',
            'Atari 5200': 'Other',
            'Atari 7800': 'Other',
            'Atari Jaguar': 'Other',
            'Atari Jaguar CD': 'Other',
            'Atari Lynx': 'Other',
            'Commodore C64/128/MAX': 'Other',
            'Commodore Amiga': 'Other',
            'Commodore PET': 'Other',
            'Commodore VIC-20': 'Other',
            'MSX': 'Other',
            'MSX2': 'Other',
            'FM Towns': 'Other',
            'Acorn Archimedes': 'Other',
            'ZX Spectrum': 'Other',
            'Sharp X68000': 'Other',
        }
        
        filtered_data['platforms'] = filtered_data['platforms'].apply(
            lambda x: ', '.join({platform_mapping.get(platform.strip(), platform.strip()) for platform in x.split(', ')})
        )

        filtered_data['platforms'] = filtered_data['platforms'].str.split(', ')
        filtered_data = filtered_data.explode('platforms')
        filtered_data['platforms'] = filtered_data['platforms'].str.strip()

        platform_counts = (
            filtered_data.groupby(['year', 'platforms'])
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
