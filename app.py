from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find("table", {"class":"table table-striped table-hover table-hover-solid-row table-simple history-data"})
table = table.find_all("tr")

row_length = len(table)

Date = [row.contents[0].text for row in table]
Day = [row.contents[1].text for row in table]
Rate = [row.contents[2].text for row in table]

#temp = [] #initiating a list 

#for i in range(1, row_length):
#insert the scrapping process here
    
#    temp.append((____,____,____)) 

#temp = temp[::-1]

#change into dataframe
Table_Kurs = pd.DataFrame(list(zip(Date, Day, Rate)), columns=["Date","Day","USD Rate"])

#insert data wrangling here
Table_Kurs['Date'] = pd.to_datetime(Table_Kurs['Date'])
Table_Kurs["Day"] = Table_Kurs["Day"].astype("category")
Table_Kurs["USD Rate"] = Table_Kurs["USD Rate"].str.strip(" IDR")
Table_Kurs["USD Rate"] = Table_Kurs["USD Rate"].str.replace(",","").astype("float")
Table_Kurs=Table_Kurs.set_index("Date")
period = pd.date_range(start="2022-01-01", end="2022-07-07")
Table_Kurs_Daily=Table_Kurs.reindex(period)
Table_Kurs_Daily=Table_Kurs_Daily.fillna(method="ffill").fillna(method="bfill")

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{Table_Kurs_Daily["USD Rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = Table_Kurs_Daily.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)