#! usr/bin/python3

from bs4 import BeautifulSoup
import time
from csv import DictWriter
import pprint
import datetime
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_driver():
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 5)
	return driver

def scroll(driver, start_date, end_date):
	driver.get("https://twitter.com/search?l=en&q=DJIA%2C%20OR%20Apple%2C%20OR%20Microsoft%2C%20OR%20stock%2C%20OR%203M%2C%20OR%20McDonals%2C%20OR%20AmericanExpress%2C%20OR%20Intel%2C%20OR%20Cisco%20since%3A{}%20until%3A{}&src=typd&lang=en".format(start_date, end_date))
	max_time = 120
	start_time = time.time()  # remember when we started
	while (time.time() - start_time) < max_time:
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scrape_tweets(driver):
	try:
		tweet_divs = driver.page_source
		obj = BeautifulSoup(tweet_divs, "html.parser")
		content = obj.find_all("div", class_="content")
		dates=[]
		names=[]
		tweet_texts=[]
		for i in content:
			date = (i.find_all("span", class_="_timestamp")[0].string).strip()
			try:
				name = (i.find_all("strong", class_="fullname")[0].string).strip()
			except AttributeError:
				name = "Anonymous"
				
			tweets = i.find("p", class_= "tweet-text").strings
			tweet_text = "".join(tweets)
			# hashtags = i.find_all("a", class_="twitter-hashtag")[0].string
			dates.append(date)
			names.append(name)
			tweet_texts.append(tweet_text)

		data = {
			"date": dates,
			"name": names,
			"tweet": tweet_texts, 
		}

		make_csv(data, start_date)

	except Exception:
		print("Whoops! Something went wrong!")
		driver.quit()

def make_csv(data, start_date):

	l = len(data['date'])
	print(l)
	print(data['tweet'][0])
	with open("data_%s.csv"%start_date, "a+") as file:
		fieldnames = ['Date', 'Name', 'Tweets']
		writer = DictWriter(file, fieldnames = fieldnames)
		writer.writeheader()
		for i in range(l):
			print('{}\n{}\n{}\n\n\n'.format(data['date'][i],
											data['name'][i],
											data['tweet'][i]
											))
			writer.writerow({'Date': data['date'][i],
							'Name': data['name'][i],
							'Tweets': data['tweet'][i],
							})
def get_all_dates(start_date, end_date):
	start_date = start_date.split('-')
	start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
	end_date = end_date.split('-')
	end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
	print("{} , {}".format(start_date, end_date))
	delta = end_date - start_date         # timedelta
	print(delta)
	dates = []
	for i in range(delta.days + 1):
	    dates.append(start_date + timedelta(days=i))
	    print(dates)
	return dates

if __name__ == "__main__":
	start_date = input("Enter the start date in (Y-M-D): ")
	end_date = input("Enter the end date in (Y-M-D): ")
	all_dates = get_all_dates(start_date, end_date)
	print(all_dates)
	for i in range(len(all_dates)-1):
		driver = init_driver()
		scroll(driver, str(all_dates[i]), str(all_dates[i+1]))
		scrape_tweets(driver)
		time.sleep(5)
		print("The tweets are ready!")
		driver.quit()