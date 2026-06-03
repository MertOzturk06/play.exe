from pytubefix import *
from pytubefix.extract import video_id
import requests
import time
import sqlite3
import webbrowser

from rich import print
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import track
from rich.table import Table


class Links():
    def __init__(self,database="playlist.db"):
        self.playlist_dict = { }
        self.new=sqlite3.connect(database)
        self.cursor=self.new.cursor()

        self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS your_playlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        url TEXT
    )
    """)

        self.new.commit()

    def playlist(self,name,url):
        self.playlist_dict[name] = url

        self.cursor.execute("""
           INSERT INTO your_playlist (name,url) VALUES (?,?)
        """,(name,url))
        self.new.commit()

    def playlist_count(self):
        self.cursor.execute("SELECT name , url FROM your_playlist")
        result_list=self.cursor.fetchall()
        how_many=len(result_list)
        return how_many       
    
    def playlist_result_list(self):
        self.cursor.execute("SELECT name  FROM your_playlist")
        result_list=self.cursor.fetchall()
        playlist_table=Table(title="Your List")
        playlist_table.add_column("Number",style="white")
        playlist_table.add_column("Video Name",style="magenta")
        for x,(a,) in enumerate(result_list,start=1):
            playlist_table.add_row(str(x),a)

        print(playlist_table)  
    

    def playlist_all(self):
        self.cursor.execute("SELECT name , url FROM your_playlist")
        # dict yapımızı tuple dolu list e çevirecek
        result_list=self.cursor.fetchall()
        return result_list

      



url_list=Links()


def open_link(opening):
    select_name,select_url_link=url_list.playlist_all()[opening-1]
    time.sleep(1.75)

    print(f"{select_name} is opening your browser ....")
    time.sleep(1)
    webbrowser.open(select_url_link)

    for _ in track(range(35),description="Loading...."):
        time.sleep(0.05)


    print(" ")
    whatsnext_menu="""
    1- Select another video
    2- Return Start
    3- Add any videos
    4- Exit
    """
    print(Panel(whatsnext_menu,border_style="blue",title="...............WHAT'S NEXT..............."))
    print(" ")

    

    while True:

        try:
            what_next=input("To continue, please pick one (1-2-3-4)  ")

            what_next=int(what_next)

            match what_next:
                case 1:
                    current_full_list()
                    break
                case 2:
                    menu()
                    break
                case 3:
                    before_adding()
                    break
                case 4:
                    time.sleep(1)
                    for _ in track(range(35),description="THANKS FOR USING MY FIRST PROGRAM 😇"):
                        time.sleep(0.05)    
                    time.sleep(1)
                    exit()


                    

        except ValueError:
            print("Invalid... Please try again")    
            continue

    



def current_full_list():
    time.sleep(1.5)
    print("...............")
    print(f"You have {url_list.playlist_count()} video(s) :")
    print(" ")
    url_list.playlist_result_list()
    print(" ")
    time.sleep(1.5)

    while True:
        try:
            grab_one=input("Which video do you play? Select the video's number  ")

            grab_one=int(grab_one)

            if 1 <= grab_one <= url_list.playlist_count():
                open_link(grab_one)
                break
            else:
                print("Invalid number. Please choose a valid number within your list...")
                time.sleep(0.55)
            

        
        except ValueError:
            print("Please enter a number")
            time.sleep(0.55)
        

        







def before_adding():
    youtube_one="youtube.com"
    youtube_two="youtube.be"


    while True:
        take_url=input("Please enter a valid YoutubeUrl Link:  ")

        if take_url :
            if youtube_one in take_url or youtube_two in take_url:
                adding(take_url)
                break
            else:
                print("Invalid...")    

        else:
            print("Invalid ...")  
            time.sleep(0.75)       



def adding(new_url):
    take_youtube=YouTube(new_url)
    youtube_name=take_youtube.title
    
    url_list.playlist(youtube_name,new_url)
    print(f"{youtube_name} is added your list...")
    time.sleep(1.51)

    while True:
        take_number=input("Would you rather add any songs (press 1) or list your songs (press 2) (to exit, press 0)  ")


        if take_number == "0":
            print("Exiting...")
            time.sleep(0.75)
            break
        elif take_number == "1":
            before_adding()
            break
        elif take_number == "2":
            current_full_list()
            break
        else:
            print("Invalid...")
            continue


    



def making():
    print("ok.LET'S GET STARTED....")
    time.sleep(2)

    before_adding()

    


    


def menu():
    play_logo=r"""
           __                             
    ____  / /___ ___  __    ___  _  _____ 
   / __ \/ / __ `/ / / /   / _ \| |/_/ _ \
  / /_/ / / /_/ / /_/ /  _/  __/>  </  __/
 / .___/_/\__,_/\__, /  (_)___/_/|_|\___/ 
/_/            /____/                     

"""
    print(f"[blue]{play_logo}[blue]")
    time.sleep(1.57)
    first_title="[bold blue]WELCOME TO OUR PLAYLIST....[bold blue]"
    print(Panel(first_title))
    time.sleep(2)


    print(" ")
    print(" ")
    
    first_menu="""
    1- List your videos
    2- Add any videos
    3- Exit
    """
    print(Panel(first_menu,border_style="blue",title="...............☰ M E N U ☰..............."))
    print(" ")

    time.sleep(1.51)

    while True:
        try:
            first_ask=input("To Continue, Please select one of the menu (press 1-2-3)  ")
            first_ask = int(first_ask)

            match first_ask:
                case 1:
                    if url_list.playlist_count() == 0:
                        print("................")
                        time.sleep(0.35)
                        print("You do not have any video(s), so you need to add any songs...")
                        time.sleep(0.75)
                        making()
                    else:
                        time.sleep(1)
                        current_full_list()    
                case 2:
                    before_adding()
                    break
                case 3:
                    time.sleep(1)
                    for _ in track(range(35),description="Exiting..."):
                        time.sleep(0.05)
                    time.sleep(1)
                    exit()
    


        except ValueError :
            print("Invalid...")
        




if __name__ == "__main__":
    menu()