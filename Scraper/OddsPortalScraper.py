# Cullen, Riley
# OddsPortalScraper.py
# Last updated 10/21/21

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class OddsPortalScraper:
    def __init__(self, headless = True):
        options = Options()
        options.headless = headless
        self.__webdriver = webdriver.Chrome('/Users/rileycullen/chromedriver', 
            options=options)   

    # desc: Destructor for OddsPortalScraper class
    def __del__(self):
        # if __webdriver has been initialized, close the browser instance.
        if (self.__webdriver):
            self.__webdriver.quit() 

test = OddsPortalScraper(headless=False)