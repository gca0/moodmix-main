import streamlit as st
import csv
from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json
import pandas as pd

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
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica",
    "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas (the)",
    "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan",
    "Bolivia (Plurinational State of)", "Bonaire, Sint Eustatius and Saba", "Bosnia and Herzegovina", "Botswana",
    "Bouvet Island", "Brazil", "British Indian Ocean Territory (the)", "Brunei Darussalam", "Bulgaria", "Burkina Faso",
    "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Cayman Islands (the)", "Central African Republic (the)",
    "Chad", "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands (the)", "Colombia", "Comoros (the)",
    "Congo (the Democratic Republic of the)", "Congo (the)", "Cook Islands (the)", "Costa Rica", "Croatia", "Cuba",
    "Curaçao", "Cyprus", "Czechia", "Côte d'Ivoire", "Denmark", "Djibouti", "Dominica", "Dominican Republic (the)",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
    "Falkland Islands (the) [Malvinas]", "Faroe Islands (the)", "Fiji", "Finland", "France", "French Guiana",
    "French Polynesia", "French Southern Territories (the)", "Gabon", "Gambia (the)", "Georgia", "Germany", "Ghana",
    "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Heard Island and McDonald Islands", "Holy See (the)", "Honduras", "Hong Kong",
    "Hungary", "Iceland", "India", "Indonesia", "Iran (Islamic Republic of)", "Iraq", "Ireland", "Isle of Man", "Israel",
    "Italy", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea (the Democratic People's Republic of)",
    "Korea (the Republic of)", "Kuwait", "Kyrgyzstan", "Lao People's Democratic Republic (the)", "Latvia", "Lebanon", "Lesotho",
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macao", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Marshall Islands (the)", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia (Federated States of)",
    "Moldova (the Republic of)", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia",
    "Nauru", "Nepal", "Netherlands (the)", "New Caledonia", "New Zealand", "Nicaragua", "Niger (the)", "Nigeria", "Niue",
    "Norfolk Island", "Northern Mariana Islands (the)", "Norway", "Oman", "Pakistan", "Palau", "Palestine, State of", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines (the)", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar",
    "Republic of North Macedonia", "Romania", "Russian Federation (the)", "Rwanda", "Réunion", "Saint Barthélemy",
    "Saint Helena, Ascension and Tristan da Cunha", "Saint Kitts and Nevis", "Saint Lucia", "Saint Martin (French part)",
    "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Sint Maarten (Dutch part)", "Slovakia",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "South Sudan",
    "Spain", "Sri Lanka", "Sudan (the)", "Suriname", "Svalbard and Jan Mayen", "Sweden", "Switzerland", "Syrian Arab Republic",
    "Taiwan (Province of China)", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Timor-Leste", "Togo", "Tokelau",
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Turks and Caicos Islands (the)", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates (the)", "United Kingdom of Great Britain and Northern Ireland (the)",
    "United States Minor Outlying Islands (the)", "United States of America (the)", "Uruguay", "Uzbekistan", "Vanuatu",
    "Venezuela (Bolivarian Republic of)", "Viet Nam", "Virgin Islands (British)", "Virgin Islands (U.S.)", "Wallis and Futuna",
    "Western Sahara", "Yemen", "Zambia", "Zimbabwe", "Åland Islands"
]

# files
expanded_word_data = "word_data_with_colors.csv"
iso_countries = "country_iso_codes.xlsx"
# Load the Excel file into a pandas DataFrame
df = pd.read_excel(iso_countries)

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
    
    query = f'limit={num_songs}&market=US&seed_genres={selected_genre}'
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
    json_result = json.loads(result.content)

    for i in json_result['tracks']:
        st.write(f"\"{i['name']}\" by {i['artists'][0]['name']}")
        print(f"\"{i['name']}\" by {i['artists'][0]['name']}")

# Function to get country code based on country name
def get_country_code(country_name):
    try:
        code = df.loc[df['Country'].str.lower() == country_name.lower(), 'Alpha-2 code'].iloc[0]
        return code
    except IndexError:
        return "Country not found"

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
    
    # # Function to generate HTML for removing a tag
    # def remove_tag_js(tag):
    #     return f"""<script>
    #                 document.getElementById('{tag}').remove();
    #             </script>"""
    
    # Streamlit UI components for user input
    st.title("MoodMix")

    words = []
    inputs_count = 0

    # # 5 input components for user input (words)
    # words.append(st.text_input("Enter a word or phrase: ", key=f'user_input_1').strip().lower())
    # words.append(st.text_input("Enter a word or phrase: ", key=f'user_input_2').strip().lower())
    # words.append(st.text_input("Enter a word or phrase: ", key=f'user_input_3').strip().lower())
    # words.append(st.text_input("Enter a word or phrase: ", key=f'user_input_4').strip().lower())
    # words.append(st.text_input("Enter a word or phrase: ", key=f'user_input_5').strip().lower())

    # add new rows
    # if 'count' not in st.session_state:
    #     st.session_state.count = 0

    # def add_new_row():
    #     st.text_input("Please input something",key=random.choice(string.ascii_uppercase)+str(random.randint(0,999999)))

    # if st.button("Add new row"):
    #     st.session_state.count += 1
    #     add_new_row()
    #     if st.session_state.count>1:
    #         for i in range(st.session_state.count-1):
    #             add_new_row()

    # Main loop to handle user input
    while len(words) < 5:
        input_word = st.text_input("Enter a noun or verb: ", key=f"user_input_words_{inputs_count}").strip().lower()
        words.append(input_word)
        inputs_count += 1
        st.write(input_word)
    
    # add_fields_button_clicked = st.button("Add word (Max 8)")
    # if add_fields_button_clicked: 
    #     input_word = st.text_input("Enter a word or phrase: ", key=f"user_input_words_{inputs_count}").strip().lower()
    #     words.append(input_word)
    #     inputs_count += 1
    #     st.write(input_word)

        # if inputs_count >= 5:
        #     choice = st.radio("You've entered at least 5 words. Do you want to add more?", ('Yes', 'No'), key=f"ask_user_if_more_words_{inputs_count}")
        #     if choice != 'No':
        #         break
        
        # if len(words) >= 8:
        #     st.write("You've entered 8 words. We'll stop adding more words.")
        #     break

    # determine the emotion(s) of the user input
    emotions = categorize_emotion(words)
    access_token = get_access_token()
    # Prompt the user for genre selection
    # Create a dropdown menu with multiple selection enabled
    selected_genres = st.multiselect("Select Genres", GENRES)
    print(selected_genres)

    # Convert the list of selected genres to a single string with "%2C" in between each genre
    selected_genres_str = "%2C".join(selected_genres)

    # Display the selected genres
    st.write("Selected Genres:", selected_genres)

    # # prompt user for markets 
    # market_input = st.multiselect("Select country of origin (max 5):", COUNTRIES)

    # selected_markets = []
    # for market in market_input: 
    #     selected_markets.append(get_country_code(market))

    # selected_markets = "%2C".join(selected_markets)
    # st.write("Selected Markets:", market_input)

    # Button to generate songs
    generate_button_clicked = st.button("Generate Songs")

    # Check if the button is clicked
    if generate_button_clicked:
        num_songs = 10
        access_token = get_access_token()
        emotions = categorize_emotion(words)
        st.write("the emotion(s) associated with your input: ", emotions)
        if emotions:
            for emotion in emotions:
                audio_ft_ranges = get_audio_ft_range(emotion)
                get_spotify_recommendations(num_songs, audio_ft_ranges, selected_genres_str, access_token)



if __name__ == "__main__":
    main()