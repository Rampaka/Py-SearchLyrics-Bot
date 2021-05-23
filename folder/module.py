from .config import *
import lyricsgenius

genius = lyricsgenius.Genius(key)

async def GetArtist(artist_name):
    artist = genius.search_artist(artist_name,max_songs=0)
    return artist

async def SplitList(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

async def ListToText(list,count):
    text = ''
    if count == 0:
        num = 0
        for i in list[count]:
            if num == 0:
                text = text + i
            else:
                text = text + '[' + i + '\n'
            num = num + 1
    else:
        for i in list[count]:
            text = text + '[' + i + '\n'

    return text