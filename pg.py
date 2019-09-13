from bs4 import BeautifulSoup
import requests

def grab_data(lis):
	o = []
	for l in lis:
		url = l
		rq = requests.get(url)

		soup = BeautifulSoup(rq.content, 'html.parser')
		raw = []
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

	return o


def clean_URLs(lis):
	o = []
	for item in lis:
		o.append('https://pitchfork.com' + item)

	return o

def grab_URLs():
	l = 'https://pitchfork.com/reviews/albums/'
	r = requests.get(l)

	s = BeautifulSoup(r.content, 'html.parser')
	o = []

	for div in s.findAll('div', attrs={'class':'review'}):
		o.append(div.find('a')['href'])

	return o

def main():
	u = grab_URLs()
	u = clean_URLs(u)
	print(u)
	el = grab_data(u)
	print(el)

if __name__ == '__main__':
	main()