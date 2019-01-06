from kivy.app import App
from kivy.lang import Builder
from songlist import SongList
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from song import Song
from kivy.uix.button import Button


class SongsToLearnApp(App):
    message = StringProperty()
    message2 = StringProperty()
    current_sort = StringProperty()
    sort_choices = ListProperty()

    def __init__(self, **kwargs):

        super(SongsToLearnApp, self).__init__(**kwargs)
        self.song_list = SongList()
        self.sort_choices = ["title", "artist", "year", "is_required"]
        self.current_sort = self.sort_choices[0]
        self.song_list.load_songs()

    def build(self):

        self.learn___ = "Songs to learn 2.0 by Fei"
        self.title = self.learn___
        self.root = Builder.load_file('app.kv')
        self.create_widgets()
        return self.root

    def change_sort(self, sorting_choice):

        self.message = "song have been sorted by: {}".format(sorting_choice)
        self.song_list.sort(sorting_choice)
        self.root.ids.entriesBox.clear_widgets()
        self.create_widgets()
        sort_index = self.sort_choices.index(sorting_choice)
        self.current_sort = self.sort_choices[sort_index]

    def blank(self):
        """
        Clear all inputs after clicking the Clear button
        """
        self.root.ids.song_title.text = ''
        self.root.ids.song_artist.text = ''
        self.root.ids.song_year.text = ''

    def create_widgets(self):
        """
        Create widgets that lists the songs from the csv file
        """
        num_song = len(self.song_list.list_songs)
        learned_song = 0
        for song in self.song_list.list_songs:

            title = song.title
            artist = song.artist
            year = song.year
            learned = song.is_required
            display_text = self.generatedisplaytext(title, artist, year,
                                                    learned)

            if learned == "n":

                learned_song += 1
                button_color = self.getColor(learned)
            else:
                button_color = self.getColor(learned)

            temp_button = Button(text=display_text, id=song.title,
                                 background_color=button_color)
            temp_button.bind(on_release=self.press_entry)

            self.root.ids.entriesBox.add_widget(temp_button)
        self.message = "To learn: {}. Learned: {}".format(num_song - learned_song, learned_song)

    def generatedisplaytext(self, title, artist, year, learned):
        if learned == "n":
            display_text = "{} by {} ({}) (Learned)".format(title, artist, year)
        else:
            display_text = "{} by {} ({})".format(title, artist, year)

        return display_text

    def getColor(self, learned):
        if learned == "n":
            button_color = [0.7, 1, 0, 1]
        else:
            button_color = [0.2, 0, 1, 1]
        return button_color

    def press_entry(self, button):
        buttontext = button.text
        selectedsong = Song()
        for song in self.song_list.list_songs:

            songDisplayText = self.generateDisplayText(song.title, song.artist, song.year, song.is_required)
            if buttontext == songDisplayText:
                selectedsong = song
                break

        selectedsong.mark_learned()
        self.root.ids.entriesBox.clear_widgets()

        self.message2 = "You have learned {}".format(selectedsong.title)  # Display whatever changed in message 2

    def add_songs(self):
        if self.root.ids.song_title.text == "" or self.root.ids.song_artist.text == "" or self.root.ids.song_year.text == "":
            self.root.ids.status2.text = "All fields must be completed"
            return
        try:
            song_title = str(self.root.ids.song_title.text)
            song_artist = str(self.root.ids.song_artist.text)
            song_year = int(self.root.ids.song_year.text)
            is_required = "y"

            self.song_list.add_to_list(song_title, song_artist, song_year, is_required)
            temp_button = Button(
                text=self.generateDisplayText(song_title, song_artist, song_year, is_required))
            temp_button.bind(on_release=self.press_entry)

            temp_button.background_color = self.getColor(is_required)
            self.root.ids.entriesBox.add_widget(temp_button)

            self.root.ids.song_title.text = ""
            self.root.ids.song_artist.text = ""
            self.root.ids.song_year.text = ""

        except ValueError:
            self.message2 = "Please enter a valid year"

    def on_stop(self):
        self.song_list.save_songs()


SongsToLearnApp().run()

SongsToLearnApp().run()