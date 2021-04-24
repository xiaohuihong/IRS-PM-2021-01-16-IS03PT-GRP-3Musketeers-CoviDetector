from event import Event
import pandas as pd

class MOH(Event):

	def __init__(self, url):
		super(MOH, self).__init__(url)
		self.soup = self.getSoup()
		self.question_list = ["What is the current DORSCON Level?", 
		"How many import cases are there?",
		"How many active cases are there?",
		"How many people have taken their first dose of vaccination?",
		"How many people are fully vaccinated?",
		"How many swap tests has been done?"]
	
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
		
	def get_data(self, row_count):
		d_level = self.get_dorscon_level()
		import_case = self.get_imported_cases()
		active_case = self.get_active_cases()
		first_dose = self.get_first_dose_number()
		full_vac = self.get_full_vaccination_number()
		swap_test = self.get_number_swap_tested()

		data = {'sn': list(range(row_count, row_count + 6)),
				'Queston': self.question_list,
				'Answer': [d_level, import_case, active_case, first_dose, full_vac, swap_test]
				}

		df = pd.DataFrame(data, columns = ['sn', 'Queston', 'Answer'])
		df['Short Answer'] = "NA"
		return df
