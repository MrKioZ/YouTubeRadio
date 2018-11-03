print("Loading Python Modules")
from pytube import YouTube #https://stackoverflow.com/questions/40713268/download-youtube-video-using-python
from win10toast import ToastNotifier 
from threading import Thread #Thanks to "Right leg" #https://stackoverflow.com/questions/40581649/passing-multiple-arguments-in-python-thread
import random, os, feedparser, time, urllib
import subprocess # https://stackoverflow.com/questions/2837214/python-popen-command-wait-until-the-command-is-finished TouchStone
print("Python Modules Loaded!")

#Start Read RSS
Channels        = ["UC_aEa8K-EOJ3D6gOs7HcyNg", "UCa10nxShhzNrCE1o2ZOPztg"] # The Channels that you want to get the from it the videos.
CACHE_PATH      = "songs/" #The Music Directory
remove_Cache    = False #if you want to remove the Played music or not (that just for Storage)
playagain       = False #Play The Music That Played Before
Shuffle         = False #Shuffle all Songs or play it As it Should be
repeat          = False #Repeat The Songs

counter = 0

def count_videos(thelist):
    videos_count = 0
    for channel in thelist:
        #https://danielmiessler.com/blog/rss-feed-youtube-channel/
        yt_feed = "https://www.youtube.com/feeds/videos.xml?channel_id="+thelist[counter]
        feed = feedparser.parse(yt_feed)
        videos = feed['entries']
        videos_count += int(len(videos))
    return videos_count

print("There is",count_videos(Channels),"Videos Total To Listen to ;3")

def notify(title, msg):
    '''
    Credit to Mohamed A ElGayar
    @ https://www.quora.com/How-can-I-send-desktop-notifications-on-Windows-with-Python
    '''
    print("Sending Notification to the User")
    toaster = ToastNotifier()
    icons = ["Sweet.ico", "YouTube.ico"]
    ico_rand = random.choice(icons)
    toaster.show_toast(title, msg, icon_path=ico_rand, duration=10, threaded=True)

def audio_play(myfile):
    '''
    Thanks to Jiaaro For the Solve
    @
    https://stackoverflow.com/questions/260738/play-audio-with-python
    '''
    music_playing = False
    if music_playing == False:
        music_playing = True
        notify("YouTube Radio", "you are now Listening to "+myfile)
        some_command = "ffmpeg\\bin\\ffplay -nodisp -autoexit \""+myfile+"\""
        #https://stackoverflow.com/questions/11615455/python-start-new-command-prompt-on-windows-and-wait-for-it-finish-exit
        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()  
        p_status = p.wait()
        music_playing = False
        if remove_Cache == False:
            pass
        elif remove == True:
            os.remove(myfile)
    elif music_playing == True:
        print("Error Sorry but there is Already Playing Song")

class yt:
    def lookup(Channel=None, Channels=None):
        if Channels is not None:
            counter = 0
            count = 0
            query = []
            for channel in Channels:
                yt_feed = "https://www.youtube.com/feeds/videos.xml?channel_id="+Channels[counter]
                feed = feedparser.parse(yt_feed)
                videos = feed['entries']
                if len(videos) > 0:
                    for video in videos:
                        try:
                            video = videos[count]
                        except urllib.error.URLError:
                            print("Sorry but You Are Disconnected from the Internet")
                            permission = input("Reconnect? (y/n): ")
                            if permission == "y":
                                pass
                            elif permission == "n":
                                print("Thank you for using Our Software")
                                print("we hope that you get Internet Connection back")
                                exit()
                        video_id = video['id'].replace("yt:video:", "")
                        count += 1
                        query.append(video_id)
                    return query # Returns list of ids
                else:
                    return "there is no new videos on this Channel"

        elif Channel is not None:
            yt_feed = "https://www.youtube.com/feeds/videos.xml?channel_id="+Channel
            feed = feedparser.parse(yt_feed)
            videos = feed['entries']
            query = []
            if len(videos) > 0:
                for video in videos:
                    try:
                        video = videos[count]
                    except urllib.error.URLError:
                        print("Sorry but You Are Disconnected from the Internet")
                        permission = input("Reconnect? (y/n): ")
                        if permission == "y":
                            pass
                        elif permission == "n":
                            print("Thank you for using Our Software")
                            print("we hope that you get Internet Connection back")
                            exit()
                    video_id = video['id'].replace("yt:video:", "")
                    video_title = video['title_detail']['value']
                    video_author = video['author_detail']['name']
                    query.append({"id":video_id, "title":video_title, "channel":video_author})
                    return query

        elif (Channel is not None) and (Channel is not None):
            raise "Error: Please Choose Only One Option"
        elif (Channel is None) and (Channel is None):
            raise "Error: All Elements in Empty Please Choose one"

    def _download(myid):
        playedbefore = open("playedbefore.txt", "r").readlines()
        #print(playedbefore)
        vid = YouTube("https://youtube.com/watch?v="+myid)
        fimiliar = False
        count = 0
        for song in playedbefore:
            if str(playedbefore[count]) == vid.title:
                fimiliar = True
                count += 1
        if fimiliar == False:
            #https://stackoverflow.com/questions/40713268/download-youtube-video-using-python
            audio = vid.streams.filter(only_audio=True).first()
            files = os.listdir()
            count = 0
            for file in files:
                if vid.title == files[count]:
                    return "Already Downlaoded"
                count += 1
            audio.download()
            some_command = "move \""+vid.title+".mp4"+"\" "+CACHE_PATH
            p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
            p_status = p.wait()

        elif fimiliar == True:
            return "This Downloaded File Before..."

    def lookup_n_download(Channels=None, Channel=None):
        if (Channel is not None) and (Channel is not None):
            raise "Error: Please Select one only Element"

        elif (Channel is None) and (Channel is None):
            raise "Error Please Add One Element"

        elif Channels is None:
            count = 0
            for Channel in Channels:
                Channel = Channels[count]
                query = self.lookup(Channel=channel)
                counter = 0
                for video in query:
                    video = query[counter]
                    print("Downloading ",video["title"])
                    self._download(video["id"])
                    counter += 1
                count += 1

        elif Channel is not None:
            counter = 0
            query = self.lookup(Channel=Channel)
            for video in query:
                video = query[counter]
                print("Downloading",video["title"])
                self._download(video["id"])
                counter += 1

#Checking if the Script Run At the First time or not
#First time
#lookup then save the videos ids into a file and download
#Start to lookup
array_ids = yt.lookup(Channels=Channels)
print(array_ids)
with open("video_ids.txt", "wb") as f:
    count = 0
    for _id in array_ids:
        tobewritten = array_ids[count]
        tobewritten = bytes(tobewritten+"\n", 'utf-8')
        f.write(tobewritten)
        count += 1
    f.close()

#download Threaded
def download_threaded():
    count = 0
    file = open("video_ids.txt", "rb")
    listofids = file.readlines()
    file.close()
    for _id in listofids:
        _id = listofids[count]
        #print(listofids)
        _id = _id.decode("utf-8")
        _id = _id.replace("\n", "")
        print("Downloading Id:",_id)
        some_command = "cd "+CACHE_PATH
        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()
        yt._download(_id)
        some_command = "cd .."
        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
        p_status = p.wait()
        count += 1

#refresh the list and playing in threaded mode
def play_each_song():
    filenotfound = True
    while filenotfound:
        songs = os.listdir(CACHE_PATH)
        if (len(songs)-1) > 1:
            print("Song(s) Founded!")
            print("Playing it..")
        else:
            print("There is no Songs in the directory Trying Later..")
            time.sleep(10)

    while repeat:
        if Shuffle == False:
            songs = os.listdir(CACHE_PATH)
            audio_play(CACHE_PATH+random.choice(songs))
        for song in songs:
            songs = os.listdir(CACHE_PATH)
            audio_play(CACHE_PATH+songs[count])
            count += 1

    if Shuffle == True:
        songs = os.listdir(CACHE_PATH)
        audio_play(CACHE_PATH+random.choice(songs))
    



t1 = Thread(target=download_threaded) #Downloading Videos
t1.start()

t2 = Thread(target=play_each_song) #Playing Downloaded Videos
t2.start()