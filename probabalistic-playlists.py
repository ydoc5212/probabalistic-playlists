import os
import random
import queue

# prev_playlists and next_playlists are dicts of spotify URLs and weights attached to the graphs
class Playlist:
    def __init__(self, songs={}, prev_playlists={}, next_playlists={}):
        self.songs = songs
        self.prev_playlists = prev_playlists
        self.next_playlists = next_playlists

# next_songs is a dict with keys as titles and values as song objects
# special case: a song with an empty URL can be used as a probability branching node
class Song:
    def __init__(self, url=None, next_songs={}):
        self.url = url
        self.next_songs = next_songs

class Playhead:
    def __init__(self, head, history=queue.LifoQueue()):
        self.head = head  # stores current song
        self.history = history  # stores a linear track history in a LIFO queue

    # uses playhead to play song
    # TODO playlist navigation integration, go forward once song is done
    def play(self):
        # if the playhead is on an empty node, check for non-empty nodes then go to it
        # note: may loop forever (see: halting problem)
        if get_curr_song().url is None:
            self.next()  # recursion until suitable song found
        # only put non-empty node in history; the history is a linear collapse of nonlinear exploration
        self.history.put(self.head)
        play_song(self.head)

        # some amount of time passes, somehow check whether song is done
        # play_next(playlist, playlist_head)

    # moves playhead back and plays
    def prev(self):
        print("Rewinding...")
        if self.history.qsize() > 1:
            self.history.get()  # trash current song
            # play playlist from prev song
            print(f"Previous History: {self.history.queue} ")
            self.head = self.history.get()
            self.play()
        else:
            print(f"No previous history.")
            self.play()

    # moves playhead forward and plays
    def next(self):
        print(f"Skipping {self.head}...")
        self.head = self.pick_next_song()
        self.play()

    def pick_next_song(self):
        next_songs = get_curr_song().next_songs
        curr_bucket = 0
        rand_choice = random.uniform(0, 1)
        print(f"Choosing what to play from the following probabilities: {next_songs}")
        # choose next song according to their probabilities
        for song_key in next_songs:
            curr_probability = next_songs[song_key]
            curr_bucket += curr_probability
            # if the rand probability falls into this bucket, choose the song.
            if rand_choice <= curr_bucket:
                return song_key

    # restarts from the beginning of your history
    def restart(self):
        if self.history.qsize == 0:
            self.play()
        else:
            # empty all but first song
            while(self.history.qsize() > 1):
                self.history.get()
            self.head = self.history.get()
            self.play()


music_path = 'C:\\Users\\Cody-DellXPS\\My Drive\\Music\\'
song1_path = music_path + 'Father Stretch My Hands.mp3'
song2_path = music_path + 'Get Free.mp3'
song3_path = music_path + 'In For the Kill (Skrillex Remix).mp3'

songs_to_play = {
    "Father Stretch My Hands": Song(song1_path, {"Get Free": 0.5, "In For the Kill": 0.5}),
    "Get Free": Song(song2_path, {"In For the Kill": 0.5, "Father Stretch My Hands": 0.5}),
    "In For the Kill": Song(song3_path, {"In For the Kill": 1})
}

playlist = Playlist(songs=songs_to_play)
# start playing here
playhead = Playhead("Father Stretch My Hands")

# plays the sound file the playhead is on, with default program
def play_song():
    song_obj = get_curr_song()
    url = song_obj.url
    print(f"Now playing from {url}")
    os.startfile(url)

# TODO
def add_song(title, url=None, next_songs={}, prev_songs={}):
    # make file paths a little bit easier
    if(url is not None):
        url = music_path + url
    new_song = Song(url, next_songs)
    playlist["title": new_song]

def get_curr_song():
    return playlist.songs[playhead.head]

# def get_song_from_title(title):
#     return playlist.songs[title]

    # update previous songs to connect to this song
    # TODO

# TODO add connect_songs func which alters probabilities and runs normalization sanity check upon alteration
# def connect_songs(prev, next, probability=0):
#     if probability == 0:
#         # normalize probabilities
#         probability_sum = 0
#         for key in song1.next_songs:
#             probability_sum += key.value()
#     prev.next_songs[next.title] = {next: probability}
