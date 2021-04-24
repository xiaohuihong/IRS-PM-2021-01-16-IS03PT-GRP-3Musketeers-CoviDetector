from moh import MOH
import openpyxl
import pandas
import os 


URL = 'https://www.moh.gov.sg/covid-19'
moh_event = MOH(URL)

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

#write structure data to excel
wb = openpyxl.load_workbook("../../../Miscellaneous/COVID_FAQ.xlsx")
sheet = wb.worksheets[0]
row_count = sheet.max_row
data = moh_event.get_data(row_count)

writer = pandas.ExcelWriter('COVID_FAQ.xlsx', engine='openpyxl') 
writer.book = wb
writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)

data.to_excel(writer, "FAQ", startrow = row_count, header= False, index = False)

writer.save()


# write non structure data to text
f = open("../../../Miscellaneous/COVID_KNOWLEDGE.txt", "a")
f.write(moh_event.get_latest_article())
f.close()