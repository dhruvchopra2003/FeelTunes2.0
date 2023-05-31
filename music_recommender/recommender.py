import pandas as pd
import json
import webbrowser
import spotipy

username = 'dc'
clientID = 'c864248e70f64c5babd0dfcee327b6c8'
clientSecret = 'f671d302d7524ab980d22ddfe087df54'
redirect_url = 'http://google.com/callback/'

oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_url)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']

spotifyObject = spotipy.Spotify(auth=token)
user_name = spotifyObject.current_user()

# to print response in usable format
print(json.dumps(user_name, sort_keys=True, indent=4))

# Making song recommendations based on predicted class


def recommend_songs(pred_class, df):
    play = None
    if pred_class == 'Disgust':
        play = df[df['mood'] == 'Sad']
        play = play.sort_values(by=['popularity', 'history'], ascending=[False, True])
        #         play = play[:5].reset_index(drop=True)
        play = play.reset_index(drop=True)

    if pred_class == 'Happy' or pred_class == 'Sad':
        play = df[df['mood'] == 'Happy']
        play = play.sort_values(by=['popularity', 'history'], ascending=[False, True])
        #         play = play[:5].reset_index(drop=True)
        play = play.reset_index(drop=True)
    #         display(play)

    if pred_class == 'Fear' or pred_class == 'Angry':
        play = df[df['mood'] == 'Calm']
        play = play.sort_values(by=['popularity', 'history'], ascending=[False, True])
        #         play = play[:5].reset_index(drop=True)
        play = play.reset_index(drop=True)
    #         display(play)

    if pred_class == 'Surprise' or pred_class == 'Neutral':
        play = df[df['mood'] == 'Energetic']
        play = play.sort_values(by=['popularity', 'history'], ascending=[False, True])
        #         play = play[:5].reset_index(drop=True)
        play = play.reset_index(drop=True)
    #         display(play)
    print(type(play))
    return play


def recommend(emotion, path):
    df = pd.read_csv(path)

    df = df[['name', 'album', 'popularity', 'mood', 'id']]
    df['history'] = 0
    detect_emotion = emotion  # get it from the model
    playlist = recommend_songs(detect_emotion, df)
    i = 0

    while True:
        print("Hello " + user_name['display_name'])
        print("0 - to exit console")
        print("1 - Get recommendation for song")
        print("2 - Play a song autonomously")
        user_input = int(input("\nEnter choice: "))
        # _______________________________________________________________________________________________________________

        if user_input == 0:
            print("\nThank you!!")
            break

        elif user_input == 1:
            playlist = playlist.sort_values(by=['history', 'popularity'], ascending=[True, False])
            print(playlist[['name', 'history', 'mood']][:5])
            inp = int(input("\nEnter song index: "))
            song = playlist.loc[inp]['name']
            playlist = playlist.reset_index(drop=True)

        elif user_input == 2:
            playlist = playlist.sort_values(by=['history', 'popularity'], ascending=[True, False])
            song = playlist.loc[i][0]
            playlist = playlist.reset_index(drop=True)

        elif user_input not in [0, 1, 2]:
            print("\nEnter valid input plz: \n")
            continue

        search_song = song
        print(f"\nPlaying {song} ....\n")
        playlist.loc[playlist['name'] == song, 'history'] += 1

        results = spotifyObject.search(search_song, 1, 0, "track")
        songs_dict = results["tracks"]
        song_items = songs_dict['items']
        i += 1

        song = song_items[0]['external_urls']['spotify']
        webbrowser.open(song)
        print("\nSong has opened in the browser\n")


# recommend("Surprise", "data/data_moods.csv")
