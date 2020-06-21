from bs4 import BeautifulSoup
import requests
import json
import re

def grab_data(lis):
	# data = []
	# o = {
	# 	"data": data
	# }
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

			print(raw)

			# Sift through raw
			d = {
				"artist_name": 	raw[1],
				"album_title": 	raw[4],
				"score":		raw[5],
				"link":			raw[6]
			}
			try:  
			    float(raw[5]) 
			    res = True
			except: 
			    print("Score not a float...Skipping...") 
			    res = False

			if res:
				# info = []
				# info.append(d["score"])
				# info.append(d["album_title"] + ", " + d["artist_name"])
				# o["data"].append(info)
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

def grab_URLs(r):
	o = []
	print("Grabbing review links...")
	for i in range(r):
		l = 'https://pitchfork.com/reviews/albums/?page=' + str(i + 1)
		print(l)
		r = requests.get(l)

		s = BeautifulSoup(r.content, 'html.parser')

		for div in s.findAll('div', attrs={'class':'review'}):
			o.append(div.find('a')['href'])

	# l = 'https://pitchfork.com/reviews/albums/?page=' + str(256)
	# print(l)
	# r = requests.get(l)

	# s = BeautifulSoup(r.content, 'html.parser')

	# for div in s.findAll('div', attrs={'class':'review'}):
	# 	o.append(div.find('a')['href'])
		
	print("Done!")
	return o

def format_graph_data(all_data):
	gd = [0] * 11
	for review in all_data:
		s = float(review['score'])

		if s >= 0.0 and s <= 0.5:
			gd[0] += 1
		elif s >= 0.6 and s <= 1.5:
			gd[1] += 1
		elif s >= 1.6 and s <= 2.5:
			gd[2] += 1
		elif s >= 2.6 and s <= 3.5:
			gd[3] += 1
		elif s >= 3.6 and s <= 4.5:
			gd[4] += 1
		elif s >= 4.6 and s <= 5.5:
			gd[5] += 1
		elif s >= 5.6 and s <= 6.5:
			gd[6] += 1
		elif s >= 6.6 and s <= 7.5:
			gd[7] += 1
		elif s >= 7.6 and s <= 8.5:
			gd[8] += 1
		elif s >= 8.6 and s <= 9.5:
			gd[9] += 1
		elif s >= 9.6 and s <= 10.0:
			gd[10] += 1
	return gd


def main():
	u = grab_URLs(1)
	u = clean_URLs(u)
	all_data = grab_data(u)
	graph_data = format_graph_data(all_data)

	import datetime
	import plotly.graph_objects as go
	import plotly.io as pio

	title = 'Pitchfork Scores as of: '
	title += str(datetime.datetime.now())

	labels = ['0.0-0.5', '0.6-1.5', '1.6-2.5', '2.6-3.5', '3.6-4.5', '4.6-5.5', '5.6-6.5', '6.6-7.5', '7.6-8.5', '8.6-9.5', '9.6-10']
	fig = go.Figure(go.Bar(x=labels, y=graph_data, marker={'color': graph_data, 'colorscale': 'Viridis'}))
	fig.update_layout(title_text=title)
	pio.write_html(fig, file='data/graph.html', auto_open=True)


	# print("Writing to output.json")
	# with open('data/output.json', 'w') as outfile:
	# 	json.dump(all_data, outfile, indent = 4, separators=(',', ': '))

if __name__ == '__main__':
	main()