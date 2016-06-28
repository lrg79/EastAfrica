import requests
from bs4 import BeautifulSoup

import schedule
import time

#nytimes.com
def getNYTURL():
	url = "http://www.nytimes.com/pages/world/africa/index.html?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=World%2FAfrica&contentPlacement=2&pgtype=Homepage"
	r = requests.get(url)
	a = ["east africa", "kenya", "tanzania", "burundi", "rwanda", "uganda", "sudan", "ethiopia", "eritrea", "djibouti", "somalia"]
	text = r.text
	soup = BeautifulSoup(text, "html.parser")
	for story in soup.findAll('div', {'class':'abColumn'}):
		for link in story.findAll('a'):
			href = link.get('href')
			if any(x in href for x in a):
				print(href)
				getNYTCat(href)

def getNYTCat(href):
	url = href;
	r = requests.get(url)
	text = r.text
	soup = BeautifulSoup(text, "html.parser")
	page = soup.findAll('p', {'class': 'story-body-text story-content'})
	print(page)

#newvision.co.ug
def getNewVisionURL():
	url = "http://www.newvision.co.ug/category/east-africa"
	r = requests.get(url)
	text = r.text
	soup = BeautifulSoup(text, "html.parser")
	for story in soup.findAll('div', {'class': 'common_list common-left'}):
		for article in story.findAll('div', {'class':'list_discription'}):
			a = article.find('a')
			href = a.get('href')
			href = 'http://www.newvision.co.ug/' + href
			print href
			getNewVisionCat(href)

def getNewVisionCat(href):
	url = href;
	r = requests.get(url)
	text = r.text
	soup = BeautifulSoup(text, "html.parser")
	for story in soup.findAll('div', {'class': 'article-content'}):
		page = soup.findAll('p')
	print(page)

#Monitor.co.ug
def getMonitorURL():
	url = "http://www.monitor.co.ug/News/National/-/688334/688334/-/vgpkiq/-/index.html"
	r = requests.get(url)
	text = r.text
	soup = BeautifulSoup(text, "html.parser")
	for story in soup.findAll('div', {'class': 'subcolumns'}):
		for article in story.findAll('div', {'id': 'featurednews'}):
			head = article.h2
			href = "http://www.monitor.co.ug" + head.a.get('href')
			print href
			getMonitorCat(href)
		for article in story.findAll('div', {'id': 'morefeaturednews'}):
			for content in article.findAll('div', {'class': 'featured_column_content'}):
				head = content.h3
				href = "http://www.monitor.co.ug" + head.a.get('href')
				print href
				getMonitorCat(href)

def getMonitorCat(href):
	url = href;
	r = requests.get(url)
	text = r.text
	soup = BeautifulSoup(text, "html.parser")
	for story in soup.findAll('div', {'id': 'article_text'}):
		page = soup.findAll('p')
	print(page)	

#getNYTURL()
#getNewVisionURL()
getMonitorURL()
