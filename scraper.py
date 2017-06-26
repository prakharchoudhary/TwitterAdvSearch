#! usr/bin/python3

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def init_driver():
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 5)
	return driver

def scroll(driver):
	driver.get("https://twitter.com/search?l=en&q=DJIA%2C%20OR%20Apple%2C%20OR%20Microsoft%2C%20OR%20stock%2C%20OR%203M%2C%20OR%20McDonals%2C%20OR%20AmericanExpress%2C%20OR%20Intel%2C%20OR%20Cisco%20since%3A2009-06-17%20until%3A2009-06-18&src=typd&lang=en")
	max_time = 4
	start_time = time.time()  # remember when we started
	while (time.time() - start_time) < max_time:
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scrape_tweets(driver):
	try:
		tweet_divs = driver.page_source
		obj = BeautifulSoup(tweet_divs, "html.parser")
		content = obj.find_all("div", class_="content")
		for i in content:
			date = (i.find_all("span", class_="_timestamp")[0].string).strip()
			try:
				name = (i.find_all("strong", class_="fullname")[0].string).strip()
			except AttributeError:
				name = "Anonymous"
				
			tweets = i.find("p", class_= "tweet-text").strings
			tweet_text = "".join(tweets)
			# hashtags = i.find_all("a", class_="twitter-hashtag")[0].string

			print("{}				{}					{}".format(name, date, tweet_text))
	except Exception:
		print("Whoops! Something went wrong!")
		driver.quit()

if __name__ == "__main__":
	driver = init_driver()
	scroll(driver)
	scrape_tweets(driver)
	time.sleep(5)
	print("The tweets are ready!")
	driver.quit()