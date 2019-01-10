
import requests
import bs4
import os
import eyed3
from shutil import move

test=0
#Return list of mp3
def filelist():
    f=[]
    for filenames in os.walk("./"):
        for list in filenames:
            for file in list:
                if ".mp3" in str(file):
                    f.append(str(file))
    return f

#Check if mp3 is tagged & tag mp3
def mp3tag(list):
    for song in list:
            audio=eyed3.load("./"+song)
            try:
                print("tagged-"+str(audio.tag.artist)+"-"+str(audio.tag.album))
            except:
                print("Not Tagged")
                info=artistalbum(song.replace(".mp3","")) #info[0]=artist info[1]=album
                print( song + ">" + info[0] + ">"+info[1])
                coverloc=coverart(song.replace(".mp3",""),info[0],info[1])
                audio.initTag()
                audio.tag.images.set(3, open(coverloc,'rb').read(), 'image/jpeg')
                audio.tag.artist=info[0]
                audio.tag.album=info[1]
                audio.tag.save()


#Find artist and album
def artistalbum(song):
    #artist+ album
    link="https://www.google.com/search?q=song+"+song.replace(" ","+")
    res=requests.get(link)
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    elem=soup.find_all(class_="fl")
    info=[]
    info.append(str(elem[1].getText()))
    info.append(str(elem[2].getText()))
    return info
    #info[0]=artist info[1]=album

#Get cover art
def coverart(song,artist,album):
    artlink="https://www.google.com/search?q="+song.replace(" ","+")+album.replace(" ","+")+"+album+art"+".jpg"+".jpg&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjSjNXMncXfAhVMfSsKHe-LDIIQ_AUIDigB&biw=1760&bih=873"
    artres=requests.get(artlink)
    artsoup=bs4.BeautifulSoup(artres.text,'html.parser')
    artelem=artsoup.select("img")
    imageurl=artelem[0].get("src")
    print("Image found : "+song)
    if not os.path.exists("./CoverArt"):
        os.mkdir("./CoverArt")
    loc="./CoverArt/"+album+"-"+artist+"-AlbumArt.jpg"
    with open(loc, "wb") as f:
                f.write(requests.get(imageurl).content)
    print("\n Downloading cover of "+album +"by"+artist)
    return loc

#Sort mp3s
def mp3sort(songs):
    for song in songs:
        audio=eyed3.load("./"+song)
        try:
            if not os.path.exists("./"+audio.tag.artist):
                os.mkdir("./"+str(audio.tag.artist))
                print("Creating folder :"+str(audio.tag.artist))
            move("./"+song,"./"+str(audio.tag.artist)+"/"+song)
        except:
            print("could not move file")


if __name__=="__main__":
    mp3s=filelist()
    mp3tag(mp3s)
    opt=input("Do you want to sort your songs?(y/n)")
    if opt=="Y" or opt =="y":
        mp3sort(filelist())
