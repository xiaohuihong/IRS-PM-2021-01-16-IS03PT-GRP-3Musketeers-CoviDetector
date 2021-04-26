from event import Event
import pandas as pd

class WM(Event):

	def __init__(self, url):
		super(WM, self).__init__(url)
		self.soup = self.getSoup()
		self.question_list = ["{} total cases: {}",
		"{} new cases: {}", 
		"{} total death: {}", 
		"{} new death: {}", 
		"{} total recovered cases: {}", 
		"{} new recovered cases: {}", 
		"{} active cases: {}", 
		"{} serious,critical cases: {}", 
		"{} total cases per 1M pop: {}",
		"{} death per 1M pop: {}",
		"{} total test: {}",
		"{} test per 1M pop: {}"]
		
	def get_world_cases(self):
		result = self.soup.find(id = 'main_table_countries_today')
		countries = []
		final = []
		trs = result.find_all('tr')
		for tr in trs:
			countries.append(tr)
		countries.pop(0)
		for country in countries:
			tds = country.find_all("td")
			name = tds[1].text.replace("\n", "")
			count = 2
			for q in self.question_list:
				final.append(q.format(name, tds[count].text))
				count = count + 1
		return final

