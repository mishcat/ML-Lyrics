import argparse 
import requests
import bs4
import re

def addToFile(filename, line):
	f=open(filename, "a+")
	f.write(line)

def appendLyrics(url, filename):
	print(url)
	pattern = re.compile(r'\s+')
	url = re.sub(pattern, '', url).lower()
	print(url)
	request = requests.get(url)
	for line in bs4.BeautifulSoup(request.text, "html.parser").find_all("div", {"class":""}):
		print(line.text)
		addToFile(filename, line.text)

def getSongs(url):
	request = requests.get(url)
	songs=[]
	#get each song
	for line in bs4.BeautifulSoup(request.text, "html.parser").find_all("a", {"target": "_blank"}):
		songs.append(line.text)
	print(songs)
	return songs


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--artist', type=str, required=True)
	parser.add_argument('--file', type=str, required=True) 
	args = parser.parse_args()
	print(args.artist)
	print(args.file)
	songlist = "https://www.azlyrics.com/%s/%s.html" % ((args.artist)[0], args.artist)
	
	#make a new file to avoid old contents
	f=open(args.file, "w+")

	songs = getSongs(songlist)	

	#add lyrics of each song to the file
	for song in songs[1:10]:
		print(song)
		lyricsUrl = "http://www.azlyrics.com/lyrics/%s/%s.html" % (args.artist, song)
		appendLyrics(lyricsUrl, args.file)

if __name__ == '__main__':
    main()