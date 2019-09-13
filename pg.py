from bs4 import BeautifulSoup
import requests
import json
import re

def grab_data(lis):
	o = []
	for l in lis:
		print("Parsing through: " + l)
		url = l
		rq = requests.get(url)

		soup = BeautifulSoup(rq.content, 'html.parser')
		raw = []

		various_artists = False

		for ul in soup.findAll('ul', attrs={'class':'single-album-tombstone__artist-links'}):
			if ul.get_text() == "Various Artists":
				print("Various Artists skipped.")
				various_artists = True
				break

		if not various_artists:
			# Artist name(s)
			for div in soup.findAll('div', attrs={'class':'row'}):
				raw.append(div.find('a').contents[0])

			# Album title
			for hgroup in soup.findAll('hgroup', attrs={'class':'single-album-tombstone__headings'}):
				raw.append(hgroup.find('h1').contents[0])

			# Score
			for div in soup.findAll('div', attrs={'class':'score-circle'}):
				raw.append(div.find('span').contents[0])

			# Album art
			for div in soup.findAll('div', attrs={'class':'single-album-tombstone__art'}):
				raw.append(div.find('img')['src'])

			# Sift through raw
			d = {
				"artist_name": 	raw[1],
				"album_title": 	raw[4],
				"score":		raw[5],
				"link":			raw[6]
			}
			o.append(d)
		
	print("Done!")
	return o


def clean_URLs(lis):
	print("Cleaning urls...")
	o = []
	for item in lis:
		o.append('https://pitchfork.com' + item)

	print("Done!")
	return o

def grab_URLs():
	o = []
	print("Grabbing review links...")
	for i in range(30):
		l = 'https://pitchfork.com/reviews/albums/?page=' + str(i + 1)
		print(l)
		r = requests.get(l)

		s = BeautifulSoup(r.content, 'html.parser')

		for div in s.findAll('div', attrs={'class':'review'}):
			o.append(div.find('a')['href'])
		
	print("Done!")
	return o

def main():
	u = grab_URLs()
	u = clean_URLs(u)
	d = grab_data(u)
	print("Writing to output.json")
	with open('output.json', 'w') as outfile:
		json.dump(d, outfile, indent = 4, separators=(',', ': '))

if __name__ == '__main__':
	main()