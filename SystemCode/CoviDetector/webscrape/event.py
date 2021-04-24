import requests
from bs4 import BeautifulSoup



class Event(object):

	def __init__(self, url):
		self.url = url
		
	def getSoup(self):
		page = requests.get(self.url)
		soup = BeautifulSoup(page.content, 'html.parser')
		return soup
		
	def getExternalSoup(self, url):
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		return soup