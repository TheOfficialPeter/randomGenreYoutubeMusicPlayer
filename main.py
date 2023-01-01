import requests
from urllib import parse, request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import vlc
import pafy

genre = "dance"

# this url might expire in a few years. I will change services if needed.
r = requests.get('https://europe-west1-randommusicgenerator-34646.cloudfunctions.net/app/getRandomTrack?genre='+genre+'&market=random&decade=2010s&tag_new=false&exclude_singles=false')
songTitle = r.json()['name']

options = Options()
options.headless = True

webdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
result = webdriver.get("https://www.youtube.com/results?search_query="+parse.quote_plus(songTitle))

# wait for youtube videos to load in (for people with slow internet)
time.sleep(10)

# this fixed XPATH can change when youtube updates their website's front-end design. I'll update if needed.
vid = webdriver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div[2]/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a")
vid = vid.get_attribute("href")

vid = pafy.new(str(vid))
video = vid.getbest()
Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(str(video.url))
Media.get_mrl()
player.set_media(Media)
player.play()

time.sleep(int(vid.length))
