import pickle
from flask import Flask, render_template, request, redirect, url_for, flash, session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong secret key for session management

# Spotify API credentials
CLIENT_ID = "ac8afe9644914ec88d0b4d9f3ca5b8ba"
CLIENT_SECRET = "b753f9dc265a440fa75e29a709565021"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the saved data
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Database configuration
db_config = {
    'user': 'root',
    'password': 'user',
    'host': 'localhost',
    'database': 'user'  # Ensure you set the correct database name
}

# Function to get song album cover
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Default image

# Recommendation function
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:  # Get top 5 recommendations (excluding the input song)
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names, recommended_music_posters

# Flask routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    connection = None
    cursor = None

    # Connect to the database and check if the user exists
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM history WHERE user_id = %s", (user_id,))
        user = cursor.fetchall()  # Ensure all results are read

        if user:
            session['user_id'] = user_id  # Store user_id in session
            return redirect(url_for('music_list'))
        else:
            flash('User ID not found. Please try again.', 'danger')
            return redirect(url_for('home'))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash('Database connection error.', 'danger')
        return redirect(url_for('home'))

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
@app.route('/logout', methods=['POST'])  # This route should handle POST requests
def logout():
    session.pop('user_id', None)  # Clear the user session
    return redirect(url_for('home'))  # Redirect to the login page

# Function to get user history
def get_user_history(user_id):
    connection = None
    cursor = None
    history = []
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT search_query FROM history WHERE user_id = %s", (user_id,))
        history = cursor.fetchall()  # Fetch all user history entries
    except mysql.connector.Error as err:
        print(f"Error fetching user history: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return [h[0] for h in history]  # Extract search queries from the tuples

@app.route('/music_list')
def music_list():
    user_id = session.get('user_id')
    music_list = music['song'].values
    user_history = get_user_history(user_id) if user_id else []
    return render_template('index.html', music_list=music_list, user_history=user_history)

@app.route('/recommend', methods=['POST'])
def show_recommendation():
    selected_song = request.form['selected_song']
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    user_id = session.get('user_id')  # Get user ID from the session
    user_history = get_user_history(user_id) if user_id else []

    # Store the search history in the database
    if user_id:
        connection = None
        cursor = None
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO history (user_id, search_query) VALUES (%s, %s)", (user_id, selected_song))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting search history: {err}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # Zip the recommended music names and posters together
    recommended_music = list(zip(recommended_music_names, recommended_music_posters))

    return render_template('recommend.html', recommended_music=recommended_music, user_history=user_history)

if __name__ == '__main__':
    app.run(debug=True)
