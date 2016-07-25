import requests
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import json

class bigSoup:
	response = [];
	allUrls = [];
	CSOUrls = [];
	policeBrutalityURLS = [];
	freeSpeechURLS = [];
	protestURLS = [];
	politicalViolenceURLS = [];
	warURLS = [];
	humanRightsURLS = [];
	policeBrutality = ["police brutality", "arbitrary arrest", "unlawful arrest", "wrongful arrest", "arbitrary detention", "illegal detention", "abduction", "disappearance", "enforced disappearance", "torture", "extrajudicial killing", "summary execution"];
	CSO = ["office break-in", "ransacked offices", "security guard", "beaten", "killed"];
	freeSpeech = ["defamation", "criminal libel", "insulting the president", "cybercrime", "censorship", "social media shutdown", "internet shutdown", "media clampdown", "dissent"];
	protest = ["opposition protest", "youth protest", "opposition rally", "political rally", "public demonstration", "defiance campaign", "freedom of assembly", "riot", "teargas","election","violence", "crackdown on the opposition", "clashes", "barricades"];
	politicalViolence=["coup plot", "coup attempt", "coup d'etat", "assassination", "subversive activities", "treason"];
	war = ["rebel group", "rebel army", "rebel activity", "war crimes", "crimes against humanity", "genocide", "army"];
	humanRights = ["human rights", "gender-based violence", "sexual violence", "sexual assault", "sexual abuse", "sexual exploitation", "rape", "female", "genital mutilation", "anti-LGBT violence", "anti-gay violence", "homophobia", "violence against children", "child abuse", "human rights abuse", "human rights violation"];
	keywords = [policeBrutality, CSO, freeSpeech, protest, politicalViolence, war, humanRights];
	keywordsName = ["policeBrutality", "CSO", "freeSpeech", "protest", "politicalViolence", "war", "humanRights"];
	numKeywords = [0,0,0,0,0,0,0];

	#nytimes.com
	def getNYTURL(self):
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
					self.allUrls.append({'url': str(href)});
					self.getNYTCat(href)

	def getNYTCat(self, href):
		url = href;
		r = requests.get(url)
		text = r.text
		soup = BeautifulSoup(text, "html.parser")
		page = soup.findAll('p', {'class': 'story-body-text story-content'})
		self.catagorize(page)

	#newvision.co.ug
	def getNewVisionURL(self):
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
				self.allUrls.append({'url': str(href)});
				self.getNewVisionCat(href)

	def getNewVisionCat(self, href):
		url = href;
		r = requests.get(url)
		text = r.text
		soup = BeautifulSoup(text, "html.parser")
		for story in soup.findAll('div', {'class': 'article-content'}):
			page = soup.findAll('p')
		#print(page)
		self.catagorize(page)

	#allAfrica

	def getAfricaURL(self):
		pageNum = 1
		maxPage = 2
		while pageNum <= maxPage:
			url = "http://allafrica.com/eastafrica/?page=" + str(pageNum)
			r = requests.get(url)
			text = r.text
			soup = BeautifulSoup(text)
			for story in soup.findAll('ul', {'class': 'stories'}):
				for li in story.findAll('li'):
					href = li.find('a')
					if str(href) != "None":
						href = href.get('href')
						if "all" in str(href):
							print href
							self.allUrls.append({'url': str(href)});
							getAfricaCat(href)
						else:
							href = "http://allafrica.com" + href
							print href
							self.allUrls.append({'url': str(href)});
							getAfricaCat(href)
			pageNum = pageNum + 1
			print pageNum

	def getAfricaCat(self, href):
		url = href;
		r = requests.get(url)
		text = r.text
		soup = BeautifulSoup(text, "html.parser")
		page = ""
		for story in soup.findAll('div', {'class': 'story-body'}):
			global page
			page = soup.findAll('p')
		self.catagorize(page);

	#washington post
	def getWashingtonURL(self):
		url = 'https://www.washingtonpost.com/world/africa/'
		r = requests.get(url)
		text = r.text
		soup = BeautifulSoup(text)
		for story in soup.findAll('div', {'class': 'main-content-chain section-main-content-chain-1 pb-chain'}):
			for h3 in story.findAll('h3'):
				href = h3.a.get('href')
				print href
				self.allUrls.append({'url': str(href)});
				if(href != ""):
					self.getWashingtonCat(href)

	def getWashingtonCat(self, href):
		url = href;
		r = requests.get(url)
		text = r.text
		soup = BeautifulSoup(text, "html.parser")
		page = ""
		for div in soup.findAll('div', {'id': 'article-body'}):
			global page
			page = div.findAll('p')
		#print page
		self.catagorize(page)

	def catagorize(self, page):
		page = str(page)
		index = 0
		for array in self.keywords:
			i = 0
			while i < len(array):
				word = array[i]
				if word in page:
					num = self.numKeywords[index]
					num+=1
					self.numKeywords[index] = num
				i+=1
			index+=1

	def printNumKeywords(self):
		j = 0
		while j < 7:
			print str(self.keywordsName[j]) + " " + str(self.numKeywords[j])
			self.response.append({'n': self.numKeywords[j], 'label': self.keywordsName[j]});
			j = j+1

	def printJSON(self):
		#   { y: 21, label: "21%", indexLabel: "Video" },
		with open('output.json', 'w') as outfile:
			json.dump(bigSoup.response, outfile)
		with open('allUrls.json', 'w') as outfile:
			json.dump(bigSoup.allUrls, outfile)	

soup = bigSoup();
soup.getNYTURL();
soup.getWashingtonURL();
soup.getAfricaURL();
soup.getNewVisionURL();
soup.printNumKeywords();
soup.printJSON();
#getNewVisionURL()
#getAfricaURL()
#getWashingtonURL()
