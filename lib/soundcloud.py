from bs4 import BeautifulSoup as bs4
import requests, json
import time

class scpy:
	def __init__(self):
		self.ses = requests.Session()
		self.headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
			"Accept": "*/*",
			"DNT" : "1"
		}
		self.ses.headers.update(self.headers)
		self.url = None
		self.inputparam = None
		self.token = None

	def setdata(self,settype,value):
		if settype == "url":
			self.url=value
		elif settype == "input":
			self.inputparam = value
		elif settype == "headers":
			self.headers = value

	def getandsettoken(self):
		r =  self.ses.get(self.url)
		html_bytes = r.text
		soup = bs4(html_bytes, 'lxml')
		self.token = soup.find('input', {'name':'csrfmiddlewaretoken'})['value']

	def createimage(self):
		r =  self.ses.post(self.url,files = self.inputparam)
		html_bytes = r.text
		soup = bs4(html_bytes, 'lxml')
		result = soup.find('a', {'class': 'expanded button'})['href']
		try:
			result = result.text
		except:
			pass
		return result

	def style_gplay(self,text1):
		self.url = "https://sclouddownloader.net/download-sound-track"
		self.getandsettoken()
		self.inputparam = (
						('csrfmiddlewaretoken', (None, self.token)),
						('sound-url', (None, 'https://soundcloud.com/aviwkila/aviwkila-doa-untuk-kamu')),
					)
		return self.createimage()