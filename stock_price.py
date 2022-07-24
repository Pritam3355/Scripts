
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup 
import csv,time,datetime,os
from urllib.parse import urljoin
import pandas as pd

#url_g ='https://in.investing.com/commodities/gold-historical-data?end_date=1594578600&interval_sec=weekly&st_date=1531420200&interval_sec=daily'
url_g = 'https://in.investing.com/commodities/gold-historical-data?end_date=1594578600&interval_sec=weekly&st_date=1436725800&interval_sec=daily'

#remove any file stored in current directory with same name

if os.path.exists('data.csv'):
	os.remove('data.csv')
	print('File Found,Deleted.')
else:
	pass

#open file in write mode
f = open('data.csv','w',newline='')
#create a csv writer object to read & write sequence
w = csv.writer(f)

#send request & collect the table data in raw html format
#use the network tab in inspect element of any web page to get your browser headers
request = Request(url=url_g,headers={'User-Agent': 'Mozilla/5.0'})  
soup = BeautifulSoup(urlopen(request).read(),features="html5lib")
tbody = soup.find('table',{"class":"common-table medium js-table"})

# table format

# <table class="common-table medium js-table">
# 	<colgroup>different column name identifying class
# 	</colgroup>
# 	<thread>
# 		<tr>property & functionality of the table</tr>
# 	</thread>
# 	<tbody>
# 		<tr>
# 			<td>date,open,high,low,%change value</td>
# 		</tr>
# 	</tbody>
# <table>


for row in tbody.find_all('tr'):    #inside <tbody> go through each <tr>
	cols = row.find_all('td')       #find all <td> inside <tr>
	cols = [x.text.strip() for x in cols] #collect text inside <td>
	#heading row , no data present only column names are present 
	if cols == []:                         
		w.writerow(['Date','Price','Open','High','Low','Volume','Chg%'])
	#data column , store them row-wise
	else:                                   
		w.writerow(cols)

df = pd.read_csv('data.csv')
#convert to pandas date time object so that we can use it as index
df['Date'] = pd.to_datetime(df['Date'])
#returns a string representing date,time or datetime object
df['Date'] = df['Date'].dt.strftime("%d/%m/%Y")
remove_ = ['Price','Open','High','Low']
#['Price','Open','High','Low'] has 1,801.90 format, we change to 1801.90
df[remove_] = df[remove_].replace({',':''},regex=True)
#Volume has 223.83K fromat , we change to 223.83
df['Volume'] = df['Volume'].replace({'K':''},regex=True)
#Chg% has -0.11% format , we change to -0.11
df['Chg%'] = df['Chg%'].replace({'%':''},regex=True)
#10/07/2020 is first & 06/11/2015 is last , so we reverse it
df=df[::-1].reset_index()
#reset index to RangeIndex(start=0, stop=1238, step=1)
df = df[['Date','Price','Open','High','Low','Volume']]
df.to_csv('gold_data.csv',index=False)

print("Data stored in gold_data.csv")
