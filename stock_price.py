from urllib.request import Request,urlopen
from bs4 import BeautifulSoup 
import csv,time,datetime
from urllib.parse import urljoin

#url_g ='https://in.investing.com/commodities/gold-historical-data?end_date=1594578600&interval_sec=weekly&st_date=1531420200&interval_sec=daily'
url_g = 'https://in.investing.com/commodities/gold-historical-data?end_date=1594578600&interval_sec=weekly&st_date=1436725800&interval_sec=daily'

f = open('data.csv','w',newline='')
w = csv.writer(f)

request = Request(url=url_g,headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(request).read(),features="html5lib")
tbody = soup.find('table',{"class":"common-table medium js-table"})

for row in tbody.find_all('tr'):
	cols = row.find_all('td')
	cols = [x.text.strip() for x in cols]
	if cols == []:
		w.writerow(['Date','Price','Open','High','Low','Volume','Chg%'])
	else:
		w.writerow(cols)

print("Data stored in data.csv")