# This file is designed to take a URL and output the title, title text, main text and explanation of a comic from Explain XKCD

import urllib.request as urllib
import re
from bs4 import BeautifulSoup

def read_url(url):
	"""Input the URL to a comic page, returns the html 'soup' of the page""" 
	# Because Explain XKCD blocks urllib scrapers, use the request function to spoof the user-agent as a browser
	req = urllib.Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # Returns urllib request object
	webpage = urllib.urlopen(req).read() # turns the request object as byte encodings
	content = webpage.decode('utf-8') # Decodes bytes into UTF-8 unicode
	# content = ''.join([line.strip() for line in content.split('\n')])
	soup = BeautifulSoup(content, "html.parser") 
	soup.prettify() # makes a pretty print version of the soup. MUCH easier to read
	return soup


def get_title(soup):
	"""Returns the title of an xkcd comic given the soup"""
	title = soup.title.string
	title = title.replace(' - explain xkcd','').strip() # Strip the explain xkcd tag
	return title.replace("\n"," ")

def get_title_text(soup):
	"""Returns the title text of an xkcd comic given the soup"""
	text = soup.find_all('a',{'class':'image'})
	title_text = text[0]['title'].strip()
	return title_text.replace("\n"," ")


def get_transcript(soup):
	"""Returns the transcript of an xkcd comic given the soup"""
	transcript = []
	header = soup.find('span',{'id':"Transcript"}).parent
	for sibling in header.next_siblings:
		if sibling.name == 'dl':
			transcript.append(sibling.text)
		elif sibling.name == 'h2':
			break
	transcript = " ".join(transcript)
	return transcript.replace("\n"," ")
	
	# for sibling in soup.find('span',{'class':"mw-headline",'id':"Transcript"}).next_siblings:
	# 	print(sibling)


def get_explanation(soup):
	"""Returns the explanation of an xkcd comic given the soup"""

	# for pp in soup.find(class_='mw-content-ltr').find_all('p'):
	# 	print(pp.text)
	
	# for pp in soup.find(class_='mw-content-ltr').find_all('p'):
	# 	siblings = pp.next_siblings # Get generator of siblings
	# 	sibling= next(siblings)
	# 	print("NAME: ",sibling.name,'\n',sibling)

	
	explanation = []
	for sibling in soup.find('h2').next_siblings:
		if sibling.name == 'p':
			explanation.append(sibling.text)
		elif sibling.name == 'a' and sibling.title == "Edit section: Transcript": # Define end of explanation as start transcript
			break
		else:
			continue
	explanation = " ".join(explanation)

	return explanation.replace("\n"," ")


def parse_comic(url):
	soup = read_url(url)
	try:
		title = get_title(soup)
	except:
		title = ""
	try:
		title_text = get_title_text(soup)
	except:
		title_text = ""
	try:
		explanation = get_explanation(soup)
	except:
		explanation = ""
	try:
		transcript = get_transcript(soup)
	except:
		transcript = ""
	if "" in [title,title_text,explanation,transcript]:
		print("ERROR:",url)	# This is for handling edge cases
	result = (title,title_text,explanation,transcript)
	return result

# example = "http://www.explainxkcd.com/wiki/index.php/936:_Password_Strength"
example2 = "http://www.explainxkcd.com/wiki/index.php/1168:_tar"
print(parse_comic(example2))



