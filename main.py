import requests
from urllib import parse, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yt_dlp
import time
import vlc

genre = input("What song genre do you wish to listen to?\n")
genre = str(genre)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getNewSong():
    global webdriver
    initialWebDriver = webdriver
    # this url might expire in a few years. I will change services if needed.
    r = requests.get('https://europe-west1-randommusicgenerator-34646.cloudfunctions.net/app/getRandomTrack?genre='+genre+'&market=random&decade=all&tag_new=false&exclude_singles=false')
    songTitle = r.json()['name']

    print(bcolors.OKGREEN + songTitle + bcolors.ENDC)

    options = Options()
    options.headless = True
    options.page_load_strategy = 'normal'
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    initialWebDriver = initialWebDriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
    initialWebDriver.get("https://www.youtube.com/results?search_query="+parse.quote_plus(songTitle+" "+genre))

    # this fixed XPATH can change when youtube updates their website's front-end design. I'll update if needed.
    vid = initialWebDriver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a")
    vid = vid.get_attribute("href")

    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(vid, download=False)
        duration = song_info['duration']
        audio_url = song_info['url']

    #audio = video.url
    #video.download()

    initialWebDriver.close()
    # sometimes the songs won't load so we pick a new one
    try:
        Instance = vlc.Instance("--no-xlib -q > /dev/null 2>&1")
        player = Instance.media_player_new()
        Media = Instance.media_new(str(audio_url), ":no-video")
        Media.get_mrl()
        player.set_media(Media)
        player.play()
    except:
        getNewSong()

    time.sleep(duration)
    getNewSong()

getNewSong()

