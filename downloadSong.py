from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import youtube_dl
import requests
import pandas as pd
import os


def getVideoID(songName): 
    print("Getting video ID for:" + songName)
    BASEURL = "http://www.youtube.com/results?search_query="
    searchURL = (BASEURL + songName)
    searchURL.replace(" ", "+") #when searches have a space youtube's url replaces with a plus sign
    page = requests.get(searchURL) #get the search page
    session = HTMLSession()
    response = session.get(searchURL)
    response.html.render(sleep = 1)
    soup = BeautifulSoup(response.html.html, "html.parser")
    
    result = soup.find('a', id= "video-title") 
    print(result['href'])
    return "finished"


getVideoID("Dirty Soda")



#print(df["song title"].to_list())
def __main__(): 
    #get data as a list of songs
    df = pd.read_csv("songs.csv" )
    los = df["song title"].to_list()
    print("We found" + len(los) + "songs")
