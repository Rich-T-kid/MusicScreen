import pprint
import time
"""clientID = "DKuxhyZLBBe32xioQQlKAtzLWp-pLOE8MTflchbbvsg7hj1ZDVCjmKKTUvdLCcJb"
clientSec = "kmxs4rzTW3jgC3RT4oMxPqtq9HSCTRCGgsovze404Xe_cTeyWJe7Kyu5oMitDjVUE4gkiwpsgDpystXJi0OSTQ"
clientAsces = "rb4HfT4matpsR6TLo4bXbLY0sL5GZiI-hhjy8vFeFpUU4POG4GcXrin7D9VpON6L"
"api.genius.com/"""

ArtistId = ["2h93pZq0e7k5yf4dywlkpM","73sIBHcqh3Z3NyqHKZ7FOL","3Sz7ZnJQBIHsXLUSo0OQtM","57vWImR43h4CaDao012Ofp","1U1el3k54VvEUzo3ybLPlM","2ICR2m4hOBPhaYiZB3rnLW"]
albumID = []

import requests #2w9zwq3AktTeYYMuhMjju8
# returns name of artist and there hype rating 0/100 given a artistID
def artistnameAndHype(artistId:str):
	url = "https://spotify23.p.rapidapi.com/artists/"
	querystring = {"ids":artistId}
	headers = {
		"X-RapidAPI-Key": "0de5ecf93cmsha4904745c74c190p148e47jsn9d4af9735775",
		"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	return response.json()['artists'][0]['name'], response.json()['artists'][0]['popularity']
# retuns all singles produced by an artist
def artistSingles(artistid:str):
	artistName_Hype = artistnameAndHype(artistid)
	url = "https://spotify23.p.rapidapi.com/artist_singles/"

	querystring = {"id":artistid,"offset":"0","limit":"20"}

	headers = {
		"X-RapidAPI-Key": "0de5ecf93cmsha4904745c74c190p148e47jsn9d4af9735775",
		"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)

	songNames = []
	for i in response.json()['data']['artist']['discography']['singles']['items']:
		single = i["releases"]['items'][0]['name']
		songNames.append(single)
		"""with open("musicdata.txt","a") as file:
			file.writelines(single + "- " + str(artistName_Hype) +"\n")"""

	return songNames



	
def Search_Gen(SongName,Artist):
    clientAccessesToken = "yyRkWEhTVG-WI24TAebeBOup0LAu9If_k09IuWd79vIJzTP4Yaz17gAs45HY7FHq"	
    base_url = "https://api.genius.com"
    search_url = f"{base_url}/search"

    headers = {
        "Authorization": f"Bearer {clientAccessesToken}"
    }
    params = {
        "q": f"{SongName} {Artist}"
    }

    response = requests.get(search_url, headers=headers, params=params)
    return  response.json()



#doesnt work as inted use the method below 
def ArtistIDD(SongName,artist):
	data = Search_Gen(SongName,Artist=artist)["response"]["hits"][0]["result"]
	fullTitle = data['full_title']
	artistID = data['id']
	release_date = data["release_date_for_display"]
	return {artist:{"fullTitle":fullTitle,"artistID":artistID,"realease_date":release_date}}
"""
{'Lil Baby': {'artistID': 5151922,
              'fullTitle': 'Sum 2 Prove by\xa0Lil\xa0Baby',
              'realease_date': 'January 10, 2020'}}
"""
# helper fucntion. returns artist ID and featured artist ID given a song name and artist of song spelt almost correct
def ArtistID_Data(songname:str,artist:str):
	a = []
	ArtistData = {}
	for i in Search_Gen(songname,artist)["response"]["hits"][0]["result"]["featured_artists"]:
		a.append(i['name'] + " id: " +str(i['id']))

	ArtistData["primary"] = str(Search_Gen("one dance","drake")["response"]["hits"][0]["result"]['primary_artist']["name"]) + " id: " + str(Search_Gen("one dance","drake")["response"]["hits"][0]["result"]['primary_artist']["id"])
	ArtistData["featured"] = a
	return ArtistData

#pprint.pprint(ArtistID_Data("3 headed goat","Lil Durk"))
#Helper function
def Helpersonglyrics(songid:str):
	url = "https://spotify23.p.rapidapi.com/track_lyrics/"
	querystring = {"id":str(songid)}
	headers = {
	"X-RapidAPI-Key": "0de5ecf93cmsha4904745c74c190p148e47jsn9d4af9735775",
	"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
}
	response = requests.get(url=url,params=querystring,headers=headers)
	return response.json()
# returns all lyrics in a song given song id
def ReturnSongLyrics(songid):
	words = []
	for i in Helpersonglyrics(str(songid))["lyrics"]["lines"]:
		words.append(i["words"])
	return words

# returns all the track id's in an album,given track/song id
def AllTrackID(TrackID):
	TrackIDAlbum = []
	trackName = []
	url = "https://spotify23.p.rapidapi.com/album_tracks/"
	querystring = {"id":TrackID,"offset":"0","limit":"300"}

	headers = {
		"X-RapidAPI-Key": "0de5ecf93cmsha4904745c74c190p148e47jsn9d4af9735775",
		"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)

	for i in response.json()["data"]['album']["tracks"]["items"]:
		x =  i['track']['uri']
		name = i["track"]['name']
		TrackIDAlbum.append(x[14:])
		trackName.append(name)
		combined = zip(trackName,TrackIDAlbum) #zip(TrackIDAlbum,trackName) 
	return list(combined)

#retuns every album produced by an artist

def AllArtistAlbums(ArtistID):
	AllAlbumIDs = []
	Data = []
	
	url = "https://spotify23.p.rapidapi.com/artist_albums/"
	querystring = {"id":ArtistID,"offset":"0","limit":"100"}
	headers = {
		"X-RapidAPI-Key": "0de5ecf93cmsha4904745c74c190p148e47jsn9d4af9735775",
		"X-RapidAPI-Host": "spotify23.p.rapidapi.com"
	}
	response = requests.get(url, headers=headers, params=querystring)
	print(response)
	for i in response.json()["data"]["artist"]["discography"]['albums']['items']:

			AlbumName = i['releases']['items'][0]["name"]
			AlbumID = i['releases']['items'][0]["id"]
			tracks = i['releases']['items'][0]['tracks']
			release_date = i['releases']['items'][0]["date"]["year"]
			albumData = {"AlbumName":AlbumName,"albumID":AlbumID,"trackCount":tracks,"realaseDate":release_date}
			Data.append(albumData)
			AllAlbumIDs.append(AlbumID)
	return Data,AllAlbumIDs


def WriteSongNamesFile(ArtistID:str):
	artistData = artistnameAndHype(ArtistID)
	#print(artistData[0])
	with open("jude.txt","a") as file:
		file.writelines(artistData[0] + "\n")
		for i in artistSingles(ArtistID):
			file.writelines(i+ "- " + "\n")
		file.writelines(artistnameAndHype(ArtistID)[0]+"\n")
		for i in AllArtistAlbums(ArtistID):
			print(i)
			pprint.pprint(AllTrackID(i[0]["albumID"][0]))
			print(type(AllTrackID(i[0]["albumID"])))



			file.writelines(str(i[0]) + "\n")
			for j in  AllTrackID(i[0]["albumID"]):
				print(j)
				file.writelines(j)
		file.writelines("done")
	return "finished correctly"
#print(artistSingles("1Xyo4u8uXC1ZmMpatF05PJ"))
"""for i in AllArtistAlbums("1Xyo4u8uXC1ZmMpatF05PJ")[0]:
	time.sleep(1)
	#print(i['albumID'])
	print(i)
	for  j in AllTrackID(i['albumID']):
		time.sleep(1)
		print(j)"""
"""text= []
with open("musicdata.txt","r") as file:
	for line in file:
		print(line.strip())
		text.append(line.strip())
"""
#print(artistnameAndHype("699OTQXzgjhIYAHMy9RyPD"))
#print(AllTrackID("2QRedhP5RmKJiJ1i8VgDGR"))
print("this wont work til sep 1st because we used up all the api calls for a month")
"""for i in AllTrackID("2QRedhP5RmKJiJ1i8VgDGR"):
	print(i)"""
print( AllArtistAlbums("0Y5tJX1MQlPlqiwlOH1tJY"))
#print(WriteSongNamesFile("0Y5tJX1MQlPlqiwlOH1tJY"))

print("done")