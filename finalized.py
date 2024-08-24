import streamlit as st
import streamlit.components.v1 as components
import csv
from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json
import pandas as pd

st.set_page_config(
    page_title="moodmix",
    page_icon="🎶",
    layout="wide"
)

# CSS styles
css = """
<style>
body {
  margin: 0;
  padding: 0;
  text-align: left;
  min-height: 100vh;
  background-image: linear-gradient(80deg, rgb(5, 124, 172), rgb(199, 10, 114));
  overflow: hidden;
}

h1 {
    margin-top: 0;
    margin-bottom: 0;
    padding: 0;
}

p {
    margin-top: 0;
    margin-bottom: 0;
    padding: 0;
}

#up {
    position: absolute; 
    height: 800px;
    width: 800px;
    border-radius: 50%;
    background-image: linear-gradient(80deg, rgb(5, 124, 172), rgb(43, 247, 202, 0.5));
    filter: blur(80px);
    animation: down 40s infinite;
}
#down {
    position: absolute; 
    right: 0;
    height: 500px;
    width: 500px;
    border-radius: 50%;
    background-image: linear-gradient(80deg, rgba(245, 207, 82, 0.8), rgba(199, 10, 114))
    filter: blur(80px);
    animation: up 30s infinite;
}

#left {
    position: absolute;
    height: 500px;
    width: 500px;
    border-radius: 50%;
    background-image: linear-gradient(80deg, rgb(199, 10, 160), rgba(183, 253, 52, 0.8));
    filter: blur(80px);
    animation: left 40s 1s infinite;
}

#right {
    position: absolute;
    height: 500px;
    width: 500px;
    border-radius: 50%;
    background-image: linear-gradient(80deg, rgba(26, 248, 18, 0.6), rgba(199, 10, 52, 0.8));
    filter: blur(80px);
    animation: right 30s .5s infinite;
}

@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
@keyframes floating {
    0% { transform: translateY(0px); }
    50% { transform: translateY(5px); }
    100% { transform: translateY(0px); }
}

@keyframes down {
    0%, 100%{
        top: -100px;
    }
    70%{
        top: 700px;
    }
}

@keyframes up {
    0%, 100%{
        bottom: -100px;
    }
    70%{
        bottom: 700px;
    }
}
@keyframes left {
    0%, 100%{
        left: -100px;
    }
    70%{
        left: 1000px;
    }
}

@keyframes right {
    0%, 100%{
        right: -100px;
    }
    70%{
        right: 1000px;
    }
}

a:hover {
    color: black;
}
a:hover button {
    background-color: white !important;
    color: black !important;
}
</style>
"""

# HTML content
html = """
<section id="up"></section>
<section id="down"></section>
<section id="left"></section>
<section id="right"></section>
"""

st.markdown(css, unsafe_allow_html=True)
st.markdown(html, unsafe_allow_html=True)

st.markdown("<h1 style='color: white; opacity: 0; animation: fadeIn 5s ease forwards, floating 2s ease infinite;'>"
            "<span style='font-weight:bold; font-family: serif; font-size: 70px;'>moodmix.</span>"
            "</h1>", unsafe_allow_html=True)
st.markdown("<p>______________________________________</p>", unsafe_allow_html=True)

# EXIT STYLING
# --------------------------------------------------------
load_dotenv()

# CONSTANTS
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

GENRES = [
    "acoustic",
    "afrobeat",
    "alt-rock",
    "alternative",
    "ambient",
    "anime",
    "black-metal",
    "bluegrass",
    "blues",
    "bossanova",
    "brazil",
    "breakbeat",
    "british",
    "cantopop",
    "chicago-house",
    "children",
    "chill",
    "classical",
    "club",
    "comedy",
    "country",
    "dance",
    "dancehall",
    "death-metal",
    "deep-house",
    "detroit-techno",
    "disco",
    "disney",
    "drum-and-bass",
    "dub",
    "dubstep",
    "edm",
    "electro",
    "electronic",
    "emo",
    "folk",
    "forro",
    "french",
    "funk",
    "garage",
    "german",
    "gospel",
    "goth",
    "grindcore",
    "groove",
    "grunge",
    "guitar",
    "happy",
    "hard-rock",
    "hardcore",
    "hardstyle",
    "heavy-metal",
    "hip-hop",
    "holidays",
    "honky-tonk",
    "house",
    "idm",
    "indian",
    "indie",
    "indie-pop",
    "industrial",
    "iranian",
    "j-dance",
    "j-idol",
    "j-pop",
    "j-rock",
    "jazz",
    "k-pop",
    "kids",
    "latin",
    "latino",
    "malay",
    "mandopop",
    "metal",
    "metal-misc",
    "metalcore",
    "minimal-techno",
    "movies",
    "mpb",
    "new-age",
    "new-release",
    "opera",
    "pagode",
    "party",
    "philippines-opm",
    "piano",
    "pop",
    "pop-film",
    "post-dubstep",
    "power-pop",
    "progressive-house",
    "psych-rock",
    "punk",
    "punk-rock",
    "r-n-b",
    "rainy-day",
    "reggae",
    "reggaeton",
    "road-trip",
    "rock",
    "rock-n-roll",
    "rockabilly",
    "romance",
    "sad",
    "salsa",
    "samba",
    "sertanejo",
    "show-tunes",
    "singer-songwriter",
    "ska",
    "sleep",
    "songwriter",
    "soul",
    "soundtracks",
    "spanish",
    "study",
    "summer",
    "swedish",
    "synth-pop",
    "tango",
    "techno",
    "trance",
    "trip-hop",
    "turkish",
    "work-out",
    "world-music"
]

# files
expanded_word_data = "word_data_with_colors.csv"

# emotion AV ranges
SAD_VALENCE = [0.98, 4.5]
SAD_AROUSAL = [2.099, 6.824]

CALM_VALENCE = [4, 7.983]
CALM_AROUSAL = [1.904, 6.358]

HAPPY_VALENCE = [6.419, 9.653]
HAPPY_AROUSAL = [3.621, 8.869]

ENERGETIC_VALENCE = [4.775, 8.165]
ENERGETIC_AROUSAL = [3.106, 8.09]

# emotion audio feature value ranges
ENERGETIC_AUDIO_FT = [
    {"danceability": [0.19, 0.81], "energy": [0.67, 1.07], "loudness": [-10.49, -0.41], 
     "speechiness": [-0.10, 0.3], "acousticness": [-0.16, 0.23], "instrumentalness": [-0.41, 0.76], 
     "liveness": [-0.13, 0.61], "valence": [0.01, 0.8], "tempo": [77.44, 190.56]}]

HAPPY_AUDIO_FT = [
    {"danceability": [0.42, 0.93], "energy": [0.40, 0.98], "loudness": [-12.72, -1.78], 
     "speechiness": [-0.13, 0.35], "acousticness": [-0.21, 0.63], "instrumentalness": [-0.42, 0.65], 
     "liveness": [-0.13, 0.52], "valence": [0.2, 0.9], "tempo": [68.30, 174.07]}]

SAD_AUDIO_FT = [
    {"danceability": [0.19, 0.82], "energy": [0.02, 0.78], "loudness": [-20.96, -2.27], 
     "speechiness": [-0.17, 0.3], "acousticness": [-0.02, 1.19], "instrumentalness": [-0.39, 0.70], 
     "liveness": [-0.12, 0.48], "valence": [0.1, 0.4], "tempo": [55.50, 174.10]}]

CALM_AUDIO_FT = [
    {"danceability": [-0.01, 0.79], "energy": [-0.16, 0.52], "loudness": [-35.95, -7.48], 
     "speechiness": [-0.06, 0.17], "acousticness": [0.36, 1.32], "instrumentalness": [0.70, 1.07], 
     "liveness": [-0.10, 0.38], "valence": [0.0, 0.3], "tempo": [41.20, 171.33]}]

# Function to request access token
def get_access_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer "+token}

# Function to get Spotify recommendations based on audio feature ranges
def get_spotify_recommendations(num_songs, audio_ft_ranges, selected_genre, access_token):

    endpoint_url = "https://api.spotify.com/v1/recommendations?"
    headers = get_auth_header(access_token)
    
    query = f'limit={num_songs}&seed_genres={selected_genre}'
    query += f'&min_acousticness={audio_ft_ranges[0]["acousticness"][0]}'
    query += f'&max_acousticness={audio_ft_ranges[0]["acousticness"][1]}'
    query += f'&min_danceability={audio_ft_ranges[0]["danceability"][0]}'
    query += f'&max_danceability={audio_ft_ranges[0]["danceability"][1]}'
    query += f'&min_energy={audio_ft_ranges[0]["energy"][0]}'
    query += f'&max_energy={audio_ft_ranges[0]["energy"][1]}'
    query += f'&min_instrumentalness={audio_ft_ranges[0]["instrumentalness"][0]}'
    query += f'&max_instrumentalness={audio_ft_ranges[0]["instrumentalness"][1]}'
    query += f'&min_liveness={audio_ft_ranges[0]["liveness"][0]}'
    query += f'&max_liveness={audio_ft_ranges[0]["liveness"][1]}'
    query += f'&min_loudness={audio_ft_ranges[0]["loudness"][0]}'
    query += f'&max_loudness={audio_ft_ranges[0]["loudness"][1]}'
    query += f'&min_speechiness={audio_ft_ranges[0]["speechiness"][0]}'
    query += f'&max_speechiness={audio_ft_ranges[0]["speechiness"][1]}'
    query += f'&min_tempo={audio_ft_ranges[0]["tempo"][0]}'
    query += f'&max_tempo={audio_ft_ranges[0]["tempo"][1]}'
    query += f'&min_valence={audio_ft_ranges[0]["valence"][0]}'
    query += f'&max_valence={audio_ft_ranges[0]["valence"][1]}'

    query_url = endpoint_url + query

    print(query_url)

    result = get(query_url, headers=headers)
    if result.status_code == 429: # too many requests
        return "429"

    json_result = json.loads(result.content)

    results_html = ""
    for i in json_result['tracks']:
        results_html += format_song(i['name'], i['artists'][0]['name'], i['album']['images'][0]['url'], i['id'])
        print(f"\"{i['name']}\" by {i['artists'][0]['name']}, spotify id is {i['id']}")
    
    return results_html
    
# format the display of each individual song
def format_song(song_name, artist_name, album_cover_url, song_id):
    song_html = f"""<a href='https://open.spotify.com/track/{song_id}' target='_blank' style='text-decoration: none;'><div id='my-song'><img src='{album_cover_url}' width='auto' height='50' style='border-radius: 10px; margin-right: 10px;'><div style='display: flex; flex-direction: column;'><span style='color: white; text-decoration: none; margin-bottom: 5px; font-size: 14px;'>{song_name}</span><span style='color: gray; font-size: 14px;'>{artist_name}</span></div></div></a>"""

    # Add CSS style for hover and active effect
    song_html += """<style>#my-song {background-color:black; color:white; padding:10px; border-radius:20px; margin-bottom:10px; display: flex; align-items: center; transition: background-color 0.3s; cursor: pointer;}
    #my-song:hover {background-color: #222;}
    #my-song:active {background-color: ##5a5a5a;}
    </style>"""

    return song_html


# searches for user inputted word in expanded word data, and return the valence and arousal
def search_word(word): 
    with open(expanded_word_data, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            anew_word = row['word'].lower()

            if anew_word == word:
                return float(row['valence']), float(row['arousal'])
            
            if ' ' in word: 
                if word.replace(' ', '-') == anew_word:
                    return float(row['valence']), float(row['arousal'])
                if word.replace(' ', '_') == anew_word:
                    return float(row['valence']), float(row['arousal'])
            
            if '-' in word: 
                if word.replace('-', ' ') == anew_word:
                    return float(row['valence']), float(row['arousal'])
                if word.replace('-', '_') == anew_word:
                    return float(row['valence']), float(row['arousal'])
    
    return None, None

# determime the average AV values of the user inputted phrase
def find_avg_av(words): 
    valence_sum = 0
    arousal_sum = 0
    count = 0

    for word in words: 
        valence, arousal = search_word(word.lower())
        if valence is not None and arousal is not None: 
            print(word)
            print("valence for {word}: ", valence)
            print("arousal for {word}: ", arousal)
            valence_sum += valence
            arousal_sum += arousal
            count += 1
    
    if count == 0:
        return None, None
    
    avg_valence = valence_sum / count
    avg_arousal = arousal_sum / count
    print("avg valence: ", avg_valence)
    print("avg_arousal: ",avg_arousal)
    return avg_valence, avg_arousal

# given the average_av values, characterize the emotion(s) of the user input
def categorize_emotion(words): 
    emotions = []
    avg_valence, avg_arousal = find_avg_av(words)
    if avg_valence is None or avg_arousal is None:
        print("No valid words found in the input.")
        return emotions
    
    if avg_valence >= SAD_VALENCE[0] and avg_valence <= SAD_VALENCE[1] and avg_arousal >= SAD_AROUSAL[0] and avg_arousal <= SAD_AROUSAL[1]: 
        emotions.append("sad")
    if avg_valence >= CALM_VALENCE[0] and avg_valence <= CALM_VALENCE[1] and avg_arousal >= CALM_AROUSAL[0] and avg_arousal <= CALM_AROUSAL[1]:
        emotions.append("calm")
    if avg_valence >= ENERGETIC_VALENCE[0] and avg_valence <= ENERGETIC_VALENCE[1] and avg_arousal >= ENERGETIC_AROUSAL[0] and avg_arousal <= ENERGETIC_AROUSAL[1]:
        emotions.append("energetic")
    if avg_valence >= HAPPY_VALENCE[0] and avg_valence <= HAPPY_VALENCE[1] and avg_arousal >= HAPPY_AROUSAL[0] and avg_arousal <= HAPPY_AROUSAL[1]:
        emotions.append("happy")
    
    if len(emotions) == 0:
        print("No emotions detected.")
    
    return emotions

# given the emotion, return the audio ranges 
def get_audio_ft_range(emotion):
    if not emotion:
        print("No emotions detected.")
        return None

    if emotion == "sad":
        print("sad:")
        print(SAD_AUDIO_FT)
        print()
        return SAD_AUDIO_FT
    if emotion == "happy":
        print("happy:")
        print(HAPPY_AUDIO_FT)
        print()
        return HAPPY_AUDIO_FT
    if emotion == "calm":
        print("calm:")
        print(CALM_AUDIO_FT)
        print()
        return CALM_AUDIO_FT
    if emotion == "energetic":
        print("energetic:")
        print(ENERGETIC_AUDIO_FT)
        print()
        return ENERGETIC_AUDIO_FT


# user front end stuff
def main():

    words = []
    inputs_count = 0

    tabs_font_css = """
    <style>
    div[class*="stTextArea"] label p {
    font-size: 15px;
    }

    div[class*="stTextInput"] label p {
    font-size: 18px;
    margin-top: 0;
    }

    div[class*="stNumberInput"] label p {
    font-size: 10px;
    }

    div[class*="stMultiSelect"] label p {
    font-size: 18px;
    }

    div[class*="stButton"] label p {
    font-size: 17px;
    }

    h2 {
        display: inline-block;
        margin-top: 0;
        margin-bottom: 0;
        padding: 0;
        font-size: 33px;
        font-weight: bold;
        animation: fadeIn 5s ease forwards;
    }
    
    </style>
    """
    st.write(tabs_font_css, unsafe_allow_html=True)

    css2 = """
    html, body {
        padding: 0;
        margin-top: 0;
        margin-bottom: 0;
        background-color: transparent;
        font-weight: 100;
        color: white;
    }

    .container {
        display: flex;
        align-items: center; 
        justify-content: flex-start; 
        margin-top: 0;
        margin-bottom: 0px;
        margin-left: 10px;
        padding: 0;
        gap: 0;
        font-weight: 100;
    }

    h3 {
        font-weight: 100;
        font-size: 23px;
        font-family: sans-serif; 
        color: white;
        margin-top: 0;
        margin-bottom: 0;
        padding: 0;
    }

    }
    .typewriter {
        font-size: 35px;
        font-weight: 100;
    }

    .blink {
        animation: blink 0.5s infinite;
    }
    @keyframes blink{
        to { opacity: .0; }
    }
    """
    
    js2 = """
    const words = ['warm romantic golden orange sunset',
            'blue hour twilight tranquil morning',
            'lonely dark rainy crying night'];
    let i = 0;
    let timer;

    function typingEffect() {
        let word = words[i].split("");
        var loopTyping = function() {
            if (word.length > 0) {
                document.getElementById('word').innerHTML += word.shift();
            } else {
                deletingEffect();
                return false;
            };
            timer = setTimeout(loopTyping, 130);
        };
        loopTyping();
    };

    function deletingEffect() {
        let word = words[i].split("");
        var loopDeleting = function() {
            if (word.length > 0) {
                word.pop();
                document.getElementById('word').innerHTML = word.join("");
            } else {
                if (words.length > (i + 1)) {
                    i++;
                } else {
                    i = 0;
                };
                typingEffect();
                return false;
            };
            timer = setTimeout(loopDeleting, 200);
        };
        loopDeleting();
    };
    typingEffect();
    
    """

    container_html = """
    <div class='container'>
        <h3 class='typewriter' id='word'></h3><h3 class='typewriter blink'>|</h3>
    </div>
    """

    # Combine HTML, CSS, and JavaScript code into a single string
    html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <!-- CSS -->
            <style>
            {css2}
            </style>
        </head>
        <body>
            <!-- HTML -->
            {container_html}

            <!-- JavaScript -->
            <script>
            {js2}
            </script>
        </body>
        </html>
    """
    
    htmll = """<h2>what are you feeling?</h2>"""
    st.markdown(htmll, unsafe_allow_html=True)
    st.markdown("""<style>iframe {background-color: transparent;}</style>""", unsafe_allow_html=True)
    st.components.v1.html(html_code, height=50, scrolling=False)



    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: 
        input1 = st.text_input("**input your words:**", key=f"user_input_words_{1}").strip().lower()
        words.append(input1)
        if input1: 
            st.markdown(f'<div style="background-color:#FFFFFF; color:#000000; padding:10px; border-radius:10px; width:100px; text-align:center;"><b>{input1}</b></div>', unsafe_allow_html=True)
    
    with col2: 
        input2 = st.text_input(" ", key=f"user_input_words_{2}").strip().lower()
        words.append(input2)
        if input2: 
            st.markdown(f'<div style="background-color:#FFFFFF; color:#000000; padding:10px; border-radius:10px; width:100px; text-align:center;"><b>{input2}</b></div>', unsafe_allow_html=True)

    with col3: 
        input3 = st.text_input(" ", key=f"user_input_words_{3}").strip().lower()
        words.append(input3)
        if input3: 
            st.markdown(f'<div style="background-color:#FFFFFF; color:#000000; padding:10px; border-radius:10px; width:100px; text-align:center;"><b>{input3}</b></div>', unsafe_allow_html=True)
    
    with col4: 
        input4 = st.text_input(" ", key=f"user_input_words_{4}").strip().lower()
        words.append(input4)
        if input4: 
            st.markdown(f'<div style="background-color:#FFFFFF; color:#000000; padding:10px; border-radius:10px; width:100px; text-align:center;"><b>{input4}</b></div>', unsafe_allow_html=True)

    with col5: 
        input5 = st.text_input(" ", key=f"user_input_words_{5}").strip().lower()
        words.append(input5)
        if input5: 
            st.markdown(f'<div style="background-color:#FFFFFF; color:#000000; padding:10px; border-radius:10px; width:100px; text-align:center;"><b>{input5}</b></div>', unsafe_allow_html=True)


    # determine the emotion(s) of the user input
    emotions = categorize_emotion(words)
    access_token = get_access_token()
    # Prompt the user for genre selection
    # Create a dropdown menu with multiple selection enabled
    st.text("")
    selected_genres = st.multiselect("**select genres (max 5):**", GENRES)
    print(selected_genres)

    # Convert the list of selected genres to a single string with "%2C" in between each genre
    selected_genres_str = "%2C".join(selected_genres)

    # Button to generate songs
    st.text("")
    generate_button_clicked = st.button(" generate songs ")
    st.text("")

    # Check if the button is clicked
    results = ""
    if generate_button_clicked:
        num_songs = 10
        access_token = get_access_token()
        emotions = categorize_emotion(words)
        st.write("**the emotion(s) associated with your input:** ")
        st.markdown(
            "<div style='display: flex;'>"
            + "".join([
                f"<div style='background-color:#FFFFFF; color:#000000; padding:10px; border-radius:10px; margin-right:10px;'>"
                f"<span style='font-weight:bold;'>{emotion}</span>"
                "</div>"
                for emotion in emotions
            ])
            + "</div>",
            unsafe_allow_html=True
        )

        st.text("")
        st.write("<div style='text-align:center; font-weight:bold; font-size:20px;'>generating your songs...</div>", unsafe_allow_html=True)
        st.text("")

        single_result = ""
        for emotion in emotions:
            audio_ft_ranges = get_audio_ft_range(emotion)
            single_result = get_spotify_recommendations(num_songs, audio_ft_ranges, selected_genres_str, access_token)
            if single_result == "429": 
                results = "429"
                break
            results += single_result
        
        print(results)

        if results == "429":
            st.markdown(
            f"<div style='background-color:#FFFFFF; color:black; padding:10px; border-radius:20px; font-weight:bold;'>"
            f"Woo there is too much traffic at the moment 🥹... Come back and try again later!🫶"
            f"</div>", 
            unsafe_allow_html=True
            )
        else: 
            st.write("<div style='text-align:center; font-weight:bold; font-size:14px;'>click on a song to listen on spotify:</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='background-color:#FFFFFF; color:black; padding:10px; border-radius:20px; font-weight:bold;'>"
                f"{results}"
                f"</div>", 
                unsafe_allow_html=True
            )




if __name__ == "__main__":
    main()



