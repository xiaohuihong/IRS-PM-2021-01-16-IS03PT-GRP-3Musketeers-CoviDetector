from event import Event

class MOH(Event):

	def __init__(self, url):
		super(MOH, self).__init__(url)
		self.soup = self.getSoup()
	
	def get_dorscon_level(self):
		results = self.soup.find('div', class_='sfContentBlock')
		r = results.find_all('h4')
		return r[1].text


	def get_imported_cases(self):
		results = self.soup.find_all('div', class_='sfContentBlock')
		r = results[1].find_all('span')
		return r[2].text
	
	def get_active_cases(self):
		results = self.soup.find_all('div', class_='sfContentBlock')
		r = results[3].find('span')
		return r.text
	
	def get_first_dose_number(self):
		results = self.soup.find_all('div', class_='sf_colsOut')
		r = results[6].find_all('span')
		return r[1].text
	
	def get_full_vaccination_number(self):
		results = self.soup.find_all('div', class_='sf_colsOut')
		r = results[7].find_all('span')
		return r[1].text
	
	def get_number_swap_tested(self):
		results = self.soup.find_all('div', class_='sf_colsOut')
		r = results[9].find_all('span')
		return r[1].text
	
	def get_vaccination_centre_list(self):
		vacsoup = self.getExternalSoup('https://www.vaccine.gov.sg/locations-vcs')
		results = vacsoup.find(id='main-content')
		rlist = results.find_all("tr")
		centres = []
		for r in rlist:
			if "address" not in r.text.lower():
				centres.append(r.text.replace("\n", "|"))
		return centres

	def get_latest_article(self):
		results = self.soup.find_all("tbody")
		r = results[14].find("a")
		latest = r.get('href')
		lsoup = self.getExternalSoup(latest)
		lweb = lsoup.find("div", class_="left-content")
		latest_content = lweb.find_all("div", class_="row")
		return latest_content[1].text
