import argparse 
import requests
import bs4
import re
import time
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import random
import numpy


def addToFile(filename, line):
	f=open(filename, "a+")
	f.write(line)

def appendLyrics(url, filename):
	ua=UserAgent()
	headers = {'User-Agent':str(ua.random)}
	print(url)
	pattern = re.compile(r'\s+' or r'\w' or r'(')
	url = re.sub(pattern, '', url).lower()

	rep = {"\'":"", "(":"", ")":"", "p.m.":"pm", "a.m.":"am"}
	rep = dict((re.escape(k), v) for k, v in rep.items())
	pattern = re.compile("|".join(rep.keys()))
	url = pattern.sub(lambda m: rep[re.escape(m.group(0))], url)


	url = url.replace("\'","")
	print(url)
	request = requests.get(url, headers=headers)
	for line in bs4.BeautifulSoup(request.text, "html.parser").find_all("div", {"class":""}):
		print(line.text)
		addToFile(filename, line.text)
		time.sleep(random.random() * 0.8)

def getSongs(url):
	ua=UserAgent()
	headers = {'User-Agent':str(ua.random)}
	request = requests.get(url, headers=headers)
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
	songs=numpy.random.choice(songs, 15, replace=False)
	for song in songs:
		print(song)
		lyricsUrl = "http://www.azlyrics.com/lyrics/%s/%s.html" % (args.artist, song)
		appendLyrics(lyricsUrl, args.file)

if __name__ == '__main__':
    main()