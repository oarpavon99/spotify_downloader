from tkinter import messagebox, filedialog
from pprint import pprint
import tkinter, requests, os, datetime, pickle, sys, csv


#######################################
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#######################################
class MainApplication(tkinter.Frame):
    def __init__(self, master):
        ######## 0. FRAMES CREATION ###########
        super().__init__()
        self.BG = "SpringGreen2"
        self.main_window = tkinter.Frame(master)
        self.main_window.configure(bg=self.BG)
        self.frame_01 = tkinter.LabelFrame(self.main_window)
        self.frame_02 = tkinter.LabelFrame(self.main_window)
        self.frame_02b = tkinter.Frame(self.frame_02)
        self.frame_02c = tkinter.Frame(self.frame_02b)
        self.frame_03 = tkinter.LabelFrame(self.main_window)
        self.frame_01.configure(bg=self.BG)
        self.frame_02.configure(bg=self.BG)
        self.frame_02b.configure(bg=self.BG)
        self.frame_03.configure(bg=self.BG)
        ###### 0. ELEMENTS CREATION ###########
        self.playlist_choice = tkinter.StringVar(self.main_window)
        self.playlist_choice.set("user")
        #######################################
        self.lbl_titulo = tkinter.Label(
            self.frame_01, text="Spotify playlist downloader.", font="Gotham 20", bg=self.BG
        )
        #######################################
        self.lbl_user = tkinter.Label(self.frame_02, text="User ID", font="Gotham 12", bg=self.BG)
        self.lbl_API_token = tkinter.Label(self.frame_02, text="Spotify Web API Token", font="Gotham 12", bg=self.BG)
        self.lbl_youtube_key = tkinter.Label(self.frame_02, text="Youtube API Key", font="Gotham 12", bg=self.BG)
        self.lbl_playlists = tkinter.Label(
            self.frame_02, text="Available Playlists", font="Gotham 12", bg=self.BG
        )
        self.e_user = tkinter.Entry(self.frame_02, width=20)
        self.e_API_token = tkinter.Entry(self.frame_02, width=20)
        self.e_youtube_key = tkinter.Entry(self.frame_02, width=20)
        #######################################
        self.playlist_scroll_y = tkinter.Scrollbar(self.frame_02c, orient="vertical")
        self.playlist_scroll_x = tkinter.Scrollbar(self.frame_02b, orient="horizontal")
        self.playlist_listbox = tkinter.Listbox(
            self.frame_02c, yscrollcommand=self.playlist_scroll_y.set, xscrollcommand=self.playlist_scroll_x.set
        )
        self.playlist_scroll_y.config(command=self.playlist_listbox.yview)
        self.playlist_scroll_x.config(command=self.playlist_listbox.xview)
        #######################################
        self.rb_all_playlists = tkinter.Radiobutton(
            self.frame_03,
            text="All playlists.",
            font="Gotham 10",
            bg=self.BG,
            variable=self.playlist_choice,
            value="all",
            command=lambda: self.playlist_choice.set("all"),
        )
        self.rb_user_playlists = tkinter.Radiobutton(
            self.frame_03,
            text="User owned only.",
            font="Gotham 10",
            bg=self.BG,
            variable=self.playlist_choice,
            value="user",
            command=lambda: self.playlist_choice.set("user"),
        )
        self.bt_get_playlists_OR_run = tkinter.Button(
            self.frame_03,
            text="Get Playlists",
            font="Consolas 14",
            bd=5,
            bg="DodgerBlue4",
            fg="white",
            command=self.start,
        )
        self.display_gui()

    #######################################
    # This gets the data coming from 'secrets.csv'
    def get_user_data(self):
        def retrieve_data(dict):
            with open("secrets.csv", "rt") as file:
                csv_line_by_line = csv.reader(file)
                for i in csv_line_by_line:
                    if len(i) > 0:
                        try:
                            assert len(i) == 2
                        except AssertionError:
                            messagebox.showerror("Spotify playlist downloader - User secrets file.",
                                                 "There was an error retrieving your: \n\n- Spotify user_id.\n- Spotify Web API token.\n- Youtube Data API token.\n\nPlease check the 'secrets.csv' file and enter the data again!")
                            self.main_window.quit()
                            break
                        else:
                            dict.setdefault(i[0], i[1].strip())
                pprint(dict)
            return dict

        retrieved_data = {}
        try:
            return retrieve_data(retrieved_data)
        except FileNotFoundError:
            with open("secrets.csv", "wt") as file:
                csv_to_write = csv.writer(file)
                csv_to_write.writerow(["Spotify user Id:"])
                csv_to_write.writerow(["Spotify Web API token:"])
                csv_to_write.writerow(["Youtube Data API key:"])
            messagebox.showinfo("Spotify playlist downloader - User secrets file.",
                                "User 'secrets.csv' file has been created, please enter your: \n\n- Spotify user_id.\n- Spotify Web API token.\n- Youtube Data API token.")
            if messagebox.askyesno("Spotify playlist downloader - User secrets file.",
                                   "Have you populated the file with the required information?"):
                return retrieve_data(retrieved_data)
            else:
                messagebox.showerror("Spotify playlist downloader - User secrets file.",
                                     "You must enter your: \n\n- Spotify user_id.\n- Spotify Web API token.\n- Youtube Data API token. \n\nThis will not work otherwise!")
                self.main_window.quit()

    #######################################
    # This will display the GUI
    def display_gui(self):
        ######## 1. FRAMES DISPLAY ############
        self.main_window.grid(row=0, column=0)
        self.frame_01.grid(row=0, column=0, columnspan=3)
        self.frame_02.grid(row=1, column=0)
        self.frame_03.grid(row=1, column=1)
        ###### 1. ELEMENTS DISPLAY ############
        self.lbl_titulo.grid(row=0, column=0)
        self.lbl_user.grid(row=0, column=0)
        self.e_user.grid(row=0, column=1)
        self.lbl_API_token.grid(row=1, column=0)
        self.e_API_token.grid(row=1, column=1)
        self.lbl_youtube_key.grid(row=2, column=0)
        self.e_youtube_key.grid(row=2, column=1)
        self.rb_all_playlists.grid(row=0, column=0, sticky="E")
        self.rb_user_playlists.grid(row=1, column=0)
        self.bt_get_playlists_OR_run.grid(row=3, column=0)
        #######################################
        # STEP 0.1: Retrieve user id, Spotify Web API token and Youtube Data API token
        retrieved_user_data = self.get_user_data()
        self.e_user.insert(0, retrieved_user_data["Spotify user Id:"].strip())
        self.e_API_token.insert(0, retrieved_user_data["Spotify Web API token:"].strip())
        self.e_youtube_key.insert(0, retrieved_user_data["Youtube Data API key:"].strip())

    #######################################
    # This is the function that gets called whenever the start button is pressed
    def start(self):
        def run():
            # Checks if the user chose a playlist:
            try:
                assert len(self.playlist_listbox.get(tkinter.ANCHOR)) > 1
            except AssertionError:
                messagebox.showwarning(
                    "Spotify playlist downloader - No playlist was selected.",
                    "Please select a playlist.",
                )
            else:
                # After the RUN button is pressed, the download sequence happens
                messagebox.showinfo(
                    "Spotify playlist downloader - Choose target directory.",
                    "Please select a folder to download your songs.",
                )
                ruta = filedialog.askdirectory(
                    initialdir="C:/",
                    title="Spotify playlist downloader - Choose target directory.",
                )
                try:
                    assert len(ruta) > 1
                except AssertionError:
                    messagebox.showwarning(
                        "Spotify playlist downloader - No directory was chosen.",
                        "Please select a valid folder.",
                    )
                else:
                    print(ruta)
                    # To increase the readability of the playlists list, numbers were added to the beginning of each one
                    # They are removed in the following instructions
                    playlist = self.playlist_listbox.get(tkinter.ANCHOR)
                    playlist = playlist[5:]
                    print(playlist)
                    #######################################
                    # STEP 2: Get the playlist items
                    cp.get_playlist_items(playlist)
                    #######################################
                    # STEP 3: Get the Youtube URLs for the selected playlist
                    cp.get_urls(ruta)
                    ######################################
                    # STEP 4: Download the Youtube URLs
                    cp.download_youtube_dl(cp.urls_list_to_download, ruta)
                    ######################################
                    messagebox.showinfo(
                        "Spotify playlist downloader.",
                        "The songs in playlist {} have been downloaded to the folder: {}".format(
                            cp.chosen_playlist, ruta
                        ),
                    )
                    # PROGRAM ENDS HERE !
                    self.main_window.quit()
                    #######################################
                    #######################################

        #######################################
        # Create instance of the Playlist class
        cp = CreatePlaylist(self.e_user.get(), self.e_API_token.get(), self.e_youtube_key.get(), self.main_window)
        #######################################
        # STEP 0: Check internet connection
        if cp.check_internet_connection():
            #######################################
            # STEP 1: Get the user's playlists
            cp.get_users_playlists(self.playlist_choice.get())
            if cp.spotify_key_OK:
                #######################################
                # Change GUI appearance and behavior
                self.rb_all_playlists.grid_forget()
                self.rb_user_playlists.grid_forget()
                #######################################
                self.lbl_playlists.grid(row=3, column=0)
                #######################################
                self.frame_02b.grid(row=3, column=1)
                self.frame_02c.pack()
                self.playlist_listbox.pack(side="left")
                self.playlist_scroll_y.pack(side="right", fill="y")
                self.playlist_scroll_x.pack(side="bottom", fill="x")
                #######################################
                self.bt_get_playlists_OR_run.configure(text="Download songs.")
                self.bt_get_playlists_OR_run.configure(command=run)
                #######################################
                # This will display the playlists in the listbox:
                for count, playlist_id in enumerate(cp.playlists.keys()):
                    self.playlist_listbox.insert(
                        tkinter.END,
                        str(count + 1).rjust(3, "0") + ". " + cp.playlists[playlist_id],
                    )


#######################################
class CreatePlaylist:
    def __init__(self, spotify_user_id, spotify_token, youtube_api_key, application_window):
        self.quota_initial_data = {}
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.youtube_api_key = youtube_api_key
        self.spotify_key_OK = True
        self.playlists = {}
        self.tracks_in_playlist = {}
        self.dict_rename = {}
        self.urls_list_to_download = []
        self.count_songs_in_chosen_playlist = 0
        self.count_songs_to_download = 0
        self.chosen_playlist = ""
        self.downloads_txt_file_name = ""
        self.print_to_downloads_txt_file = ""
        self.forbidden_terms = ["vivo", "live", "official", "oficial", "video"]
        self.hoy = datetime.datetime.today().date()
        self.quota_init()
        self.main_window = application_window
        self.YOUTUBE_DATA_API_DAILY_QUOTA = 10000

    # This checks for the existence of the quota file:
    def quota_init(self):
        try:
            with open("quota.pickle", "rb") as file:
                print("FILE EXISTS")
                self.quota_initial_data = pickle.load(file)
        except FileNotFoundError:
            with open("quota.pickle", "wb") as file:
                print("FILE DOES NOT EXIST")
                pickle.dump(self.quota_initial_data, file)
        print("quota.pickle file initialized.\nquota_dictionary = ")
        pprint(self.quota_initial_data)

    # This prints the downloaded songs into a log contained in downloads.txt in the root folder
    def send_to_log_file(self, file_name, content):
        try:
            assert len(file_name) > 1
        except AssertionError:
            pass
        else:
            # 0. Is there a file?
            try:
                with open(file_name, "rt") as file:
                    previous_content = file.read()
            # 1. There is not a file with that name, create it
            except FileNotFoundError:
                with open(file_name, "wt") as file:
                    file.write(content)
            # 2. There is a file. Update it.
            else:
                with open(file_name, "wt") as file:
                    file.write(previous_content + content)
            finally:
                print(f"--------\n****'{file_name}' FILE HAS BEEN UPDATED.")

    # This  removes the special characters from the song original name to avoid errors in the renaming
    def remove_special_characters(self, string):
        for i in string:
            if i not in [" ", "-"]:
                if not i.isalnum():
                    string = string.replace(i, "")
        return string

    # STEP 0: Check internet connection
    def check_internet_connection(self):
        query = "https://www.google.com/"
        try:
            requests.get(query)
        except requests.exceptions.ConnectionError:
            print("No internet connection found.")
            messagebox.showerror("HTTP ERROR.", "No internet connection found.")
            self.main_window.quit()
        else:
            print("Internet connection OK.")
            return True

    # STEP 1: Get the user's playlists
    def get_users_playlists(self, playlist_choice):
        def spotify_http_request_get(query):
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token),
                },
            )
            return response

        def append_playlists(respuesta):
            # This will return the playlist ID for later use
            for i in respuesta["items"]:
                if playlist_choice == "user":
                    if i["owner"]["id"] == self.user_id:
                        self.playlists[i["id"]] = self.remove_special_characters(i["name"])
                elif playlist_choice == "all":
                    self.playlists[i["id"]] = self.remove_special_characters(i["name"])

        # This sends the HTTP request to find the user's playlists
        response = spotify_http_request_get(
            f"https://api.spotify.com/v1/users/{self.user_id}/playlists?limit=50"
        )

        """In case the response status code is "Unauthorized", it's because the Spotify Web API credentials are no longer valid.
        They remain valid for about an hour, and each hour they must be updated."""
        if response.status_code == 401:
            self.spotify_key_OK = False
            messagebox.showerror(
                "HTTP Error.",
                "401 Unauthorized:\n\nThe Spotify credentials are no longer valid. Please get a new API authorization "
                "token in:\n\nhttps://developer.spotify.com/console/get-playlists/",
            )
            self.main_window.quit()
        # If status code = 200 OK, it means the creds are still valid.
        elif response.status_code == 200:
            # This fetches the json response sent back from the API service
            response_json = response.json()

            # Do we need to do another query?
            total = response_json["total"]
            query_no = total // response_json["limit"]

            for m in range(query_no + 1):
                append_playlists(response_json)
                # Do we need to do another query?
                if response_json["next"] is not None:
                    response_json = spotify_http_request_get(
                        response_json["next"]
                    ).json()

            return self.playlists

    # STEP 2: Get the playlist items
    def get_playlist_items(self, chosen_playlist):
        def spotify_http_request_get(query):
            response = requests.get(
                query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token),
                },
            )
            return response

        def append_tracks(respuesta, playlist, songs_dict):
            # Creates the Playlist array of songs inside of the dictionary
            songs_dict.setdefault(playlist, [])
            for item_number, value in enumerate(respuesta["items"]):
                # I don't know why some tracks are 'None'
                if respuesta["items"][item_number]["track"] is not None:
                    # Gets the main artist ONLY
                    artista = self.remove_special_characters(
                        respuesta["items"][item_number]["track"]["artists"][0]["name"]
                    )
                    # Gets the track's name
                    cancion = self.remove_special_characters(
                        respuesta["items"][item_number]["track"]["name"]
                    )
                    name = f"{artista} - {cancion}"
                    if name not in songs_dict[playlist]:
                        # Appends the song to the array
                        songs_dict[playlist].append(name)
                        self.count_songs_in_chosen_playlist += 1

        ##################################
        self.chosen_playlist = chosen_playlist
        ##################################
        # This gets the ID number for the chosen playlist
        playlist_id = ""
        for i in self.playlists.keys():
            print(i)
            if self.playlists[i] == self.chosen_playlist:
                playlist_id = i
                print("The Id for the selected playlist is:", i)
                break
        ##################################
        # This is the HTTP request for the tracks of a playlist (by Playlist ID)
        response_json = spotify_http_request_get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        ).json()
        ##################################

        # Do we need to do another query?
        total = response_json["total"]
        query_no = total // response_json["limit"]
        print(f"query_no = {query_no}")

        # The JSON part of the response with all the items is here
        # For further information regarding the Object Model go to:
        # https://developer.spotify.com/documentation/web-api/reference/#category-playlists
        # The response body contains an array of track objects wrapped in a paging object
        for m in range(query_no + 1):
            append_tracks(response_json, self.chosen_playlist, self.tracks_in_playlist)
            # Do we need to do another query?
            if response_json["next"] is not None:
                response_json = spotify_http_request_get(response_json["next"]).json()

        ##################################
        print(f"self.rolas = {self.count_songs_in_chosen_playlist}")
        print(self.chosen_playlist)
        for i, rol in enumerate(self.tracks_in_playlist[self.chosen_playlist]):
            print(f"{str(i + 1).rjust(2, '0')}. {rol}")

    # STEP 3: Get the Youtube URLs for the selected playlist
    def get_urls(self, ruta):
        """SUB STEP a): Gets the songs in the ruta folder. This is useful for long playlists that may not be
        downloaded in just one shot"""

        def get_songs_in_folder(ruta):
            songs_in_folder = []
            for file_dir in os.listdir(ruta):
                el = os.path.join(ruta, file_dir)
                if os.path.isfile(el) and os.path.splitext(el)[1] == ".mp3":
                    songs_in_folder.append(os.path.splitext(file_dir)[0])
            return songs_in_folder

        # SUB STEP b): Returns the Youtube Data API quota consumption values
        def youtube_quota_update(youtube_key, quota_data, units, hoy):
            quota_data.setdefault(youtube_key, {})
            with open("quota.pickle", "wb") as file:
                quota_data[youtube_key].setdefault(hoy, 0)
                quota_data[youtube_key][hoy] += units
                print(f"REQUEST UNITS = {units}\nquota_dictionary = ")
                pprint(quota_data)
                pickle.dump(quota_data, file)
                return quota_data[youtube_key][hoy]

        # SUB STEP c): This finds the song's youtube ID
        def get_video_url(query_string):
            # This is the query for the HTTP request
            query = "https://youtube.googleapis.com/youtube/v3/search?key={}&q={}&type={}&maxResults={}&part=snippet".format(
                self.youtube_api_key, query_string, "video", 10
            )
            # This is the actual HTTP request
            response = requests.get(query)
            # print("HTTP request STATUS CODE= ", response.status_code)
            if response.status_code == 403:
                messagebox.showerror(
                    "HTTP Error.",
                    "There was a HTTP error - Status code: "
                    + str(response.status_code)
                    + "\nYoutube Data API requests quota exceeded. Try again tomorrow or get another valid Youtube API key in: https://console.cloud.google.com/ ",
                )
                self.main_window.quit()
            # This fetches the json response sent back from the API service
            response_json = response.json()
            resultados = len(response_json["items"])
            id_dicc = {}
            # This gets the videoId's for the passed search term
            if resultados > 0:
                # print(resultados, ' search results were retrieved.')
                for m in range(resultados):
                    id = response_json["items"][m]["id"]["videoId"]
                    nombre = response_json["items"][m]["snippet"]["title"].lower()
                    id_dicc[id] = nombre
                # print(id_dicc)
            # This chooses one of the videos in the dictionary
            valido = False
            for id in id_dicc.keys():
                """This part will choose only the videos that do not have an excluded term
                I chose the official videos to be excluded because, often they have extra speech or undesirable audio elements
                I chose to exclude the live versions because I want the studio versions only."""
                for termino in self.forbidden_terms:
                    if termino not in id_dicc[id]:
                        valido = True
                    else:
                        valido = False
                        break
                if valido:
                    standard = "https://www.youtube.com/watch"
                    http_query_string = "?v=" + id
                    return standard + http_query_string

        # SUB STEP a): Gets the songs in the ruta folder.
        downloaded_songs = get_songs_in_folder(ruta)
        new_download_file = True
        quota = youtube_quota_update(
            self.youtube_api_key, self.quota_initial_data, 0, self.hoy
        )

        # This will search for the song one by one and append the URLs to the list
        for songy in self.tracks_in_playlist[self.chosen_playlist]:
            if songy in downloaded_songs:
                print(f"{songy} is already in: {ruta}. It will not be downloaded.")
                continue
            # If the daily API usage has not been exceeded:
            if quota < self.YOUTUBE_DATA_API_DAILY_QUOTA:
                ############################
                if new_download_file:
                    # Variables used for the download's log
                    self.downloads_txt_file_name = (
                        f"Downloaded Playlist - {self.chosen_playlist}.txt"
                    )
                    self.print_to_downloads_txt_file = (
                        f"\n{self.chosen_playlist} - {datetime.datetime.today()}:"
                    )
                    self.send_to_log_file(
                        self.downloads_txt_file_name, self.print_to_downloads_txt_file
                    )
                    new_download_file = False
                ############################
                # SUB STEP c): This finds the song's youtube ID
                url = get_video_url(songy)
                if url is not None:
                    self.urls_list_to_download.append(url)
                    self.dict_rename[url] = songy
                    self.count_songs_to_download += 1
                    print(f"{songy} : {self.count_songs_to_download}")
                quota = youtube_quota_update(
                    self.youtube_api_key, self.quota_initial_data, 100, self.hoy
                )
            else:
                print(
                    f'"{songy}" in playlist: "{self.chosen_playlist}" will not be downloaded.\nYoutube Data API requests quota exceeded. Try again tomorrow or get another valid Youtube API key in: https://console.cloud.google.com/ ',
                )
                break
        print(self.urls_list_to_download)

    # STEP 4: Download the Youtube URLs
    def download_youtube_dl(self, lista_urls, directory):
        def download_yt(song_url, directory):
            command = "youtube-dl" + " "
            audio_options = "-x --audio-format mp3" + " "
            audio_quality = "--audio-quality 0" + " "
            output_template = (
                    '-o "' + directory + "/%(artist)s-%(title)s.%(ext)s" + '" '
            )
            song = song_url
            instruction = (
                    command + audio_options + audio_quality + output_template + song
            )
            # Youtube DL uses the command line, so that's why this instruction should be employed to pass the instruction
            os.system(instruction)

        ##############################
        # These variables are used for the renaming function
        lista_creacion = []
        last_saved_file = ""

        for count, url_rola in enumerate(lista_urls):
            ##############################
            print(
                f"--------\nDOWNLOADING SONG {count + 1}/{self.count_songs_to_download}"
            )
            download_yt(url_rola, directory)
            ##############################
            # Gets the latest created file to find the path to rename
            for file in os.listdir(directory):
                archivo = os.path.join(directory, file)
                tiempo_creacion = os.path.getctime(archivo)
                lista_creacion.append(tiempo_creacion)
                if tiempo_creacion == max(lista_creacion):
                    last_saved_file = archivo
            """The command line usually has trouble finding a correct interpretation to the special characters.
            This function removes them from the string. So that the renaming can happen without errors."""
            song_name = self.remove_special_characters(self.dict_rename[url_rola])
            ##############################
            to_rename = os.path.join(directory, song_name + ".mp3")
            if song_name + ".mp3" not in os.listdir(directory):
                os.rename(last_saved_file, to_rename)
                ##############################
                self.print_to_downloads_txt_file = f"\nSONG {count + 1}/{self.count_songs_to_download}: {self.dict_rename[url_rola]}"
                self.send_to_log_file(
                    self.downloads_txt_file_name, self.print_to_downloads_txt_file
                )


#######################################


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("Spotify playlist downloader.")
    root.geometry("+300+300")
    root.iconbitmap(resource_path("icon.ico"))
    app = MainApplication(root)
    root.mainloop()
