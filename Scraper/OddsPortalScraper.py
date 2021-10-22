# Cullen, Riley
# OddsPortalScraper.py
# Last updated 10/21/21

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class OddsPortalScraper:
    # desc: Constructor for OddsPortalScraper class
    #
    # Parameters: 
    # ---------------
    # headless : boolean
    #   Toggle that determines if the webdriver should create an instance of 
    #   the browser window (headless = False) or if the webdriver should not create
    #   an instance oof the browser window (headless = True)
    def __init__(self, headless = True):
        options = Options()
        options.headless = headless
        self._webdriver = webdriver.Chrome('/Users/rileycullen/chromedriver', 
            options=options)   

    # desc: Destructor for OddsPortalScraper class
    def __del__(self):
        # if __webdriver has been initialized, close the browser instance.
        if (self._webdriver):
            self._webdriver.quit() 

    # desc: Goes to OddsPortal's login page to login
    #
    # Parameters:
    # ---------------
    # username : string
    #   User's OddsPortal username
    # 
    # password : string 
    #   User's OddsPortal password
    def Login(self, username, password):
        pass

test = OddsPortalScraper(headless=False)