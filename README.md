# MoodMix: Mapping Words to Audio Features for Music Recommendation
Traditional music recommendation systems require the user to have specific information in mind: genres, artists, album, etc. Users do not always have this information in mind; sometimes the music they want can only be described. \
I introduce MoodMix, a web application that enables users to input words characterizing the desired mood or atmosphere of songs they would like to listen to, and recommend music based on that. \
Arousal and valence values of English words were used from the ANEW dataset. After expanding with WordNet and thesaurus.com, the newly expanded dataset consisted of over 10,000 words. Audio feature value data for 297,000 songs from Spotify were taken from the Moodify dataset, each song labeled by one of four emotions: calm, energetic, happy, or sad. Synthesizing data from the two datasets, MoodMix aims to create a mapping between user input and emotions to audio feature values. \
Utilizing these audio feature values, music will be retrieved using the recommendation endpoint from the API of Spotify, an online streaming service with extensive music libraries. After evaluation by 42 users, MoodMix is deemed an overall successful application, with 76.2% of users rating it 7 or above out 10 for effectiveness.

Completed for my Princeton Computer Science Junior Independent Work
