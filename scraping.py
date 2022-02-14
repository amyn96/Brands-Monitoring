## import module
import requests
import time
from datetime import datetime
import socks
import xmltojson
import json
from bs4 import BeautifulSoup

## proxies
proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

## function to read lines in files
def readFile(fileName):
	fileObj = open(fileName, "r") #opens the file in read mode
	words = fileObj.read().splitlines() #puts the file into an array
	fileObj.close()
	return words


## create session using requests and proxies
session = requests.Session()
session.proxies.update(proxies) 

## load target detail from target json
filters = open('files/target.json')
data = json.load(filters)
data_size = len(data)
i = data_size

target = []
		
for link in data :
	target.append(link)

## looping for each target
while i > 0 :
	link = data[target[data_size - i]]['link']
	scrap_tag = data[target[data_size - i]]['scrape_class']['tag']
	scrap_class = data[target[data_size - i]]['scrape_class']['class']
	
	## checking whether target has certain details or not
	if "title" in data[target[data_size - i]] :
		title_tag = data[target[data_size - i]]['title']['class']
		title_class = data[target[data_size - i]]['title']['val']
	else :
		title_tag = "missing"
		title_class = "missing"			
					
	if "desc" in data[target[data_size - i]] :
		desc_tag = data[target[data_size - i]]['desc']['class']
		desc_class = data[target[data_size - i]]['desc']['val']
	else :
		desc_tag = "missing"
		desc_class = "missing"					
						
	if "date" in data[target[data_size - i]] :
		date_tag = data[target[data_size - i]]['date']['class']
		date_class = data[target[data_size - i]]['date']['val']
	else :
		date_tag = "missing"
		date_class = "missing"	
	
	## print output
	print("____________________________________________________________________________________________________________________\n")
	print("link : " + link)
	
	## try to check whether the target link is active or not
	try :
		ses = session.get(link)
		
		## Using beautifulsoup to get the website content into a nice format
		soup = BeautifulSoup(ses.content, 'html.parser')
		
		print("\nScrapping..\n")
		time.sleep(3)
		
		## try to check scrapping process has error or not
		try :
			## scrap for each card section
			scrap = soup.find_all(scrap_tag, scrap_class)
			
			print("Done Scraping!\n")
			time.sleep(1)
			
			print("filter result : \n")
			
			## save name by date of scrap
			now = datetime.now()
			today = now.strftime("%d-%m-%Y")
			
			scrape_detail = {}
			res = []
			scrape_detail={'link':link}
			res.append(scrape_detail)
			
			## loop to filter required details on each card section
			for scraps in scrap:
				
				title_element = scraps.find(title_tag,class_=title_class)
				desc_element = scraps.find(desc_tag,class_=desc_class)
				date_element = scraps.find(date_tag,class_=date_class)
				
				## checking whether the details is Nonetype or not
				if(title_element is not None):
					title = title_element.text.strip()
					print("Title : " + title)
				else :
					print("Title : No Title\n")
				
				if(desc_element is not None):
					desc = desc_element.text.strip()
					print("Description : " + desc)
				else :
					print("Description : No Description\n")
					
				if(date_element is not None):
					date = date_element.text.strip()
					print("Date : " + date + "\n\n")
				else :
					print("Date : No Date\n\n")
				
				## save scrape result into json
				scrape_detail = {
					'title': title,
					'desc': desc
				}
				
				res.append(scrape_detail)	
				
			result_name = 'json/result_' + str(today) + '.json'
				
			with open(result_name, 'a') as json_file:
		    			json.dump(res, json_file)
		    			
		except Exception as e:
			print("\n****************************************************************************************\n\nThere's an error : ")
			print(e)
			print("\n****************************************************************************************\n")
			
		i -= 1
	
	except requests.exceptions.RequestException as e:
		print("\n****************************************************************************************\n\nThere's an error : ")
		print(e)
		print("\n****************************************************************************************\n")
		
		i -= 1

filters.close()