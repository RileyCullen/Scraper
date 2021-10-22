# Cullen, Riley
# OddsPortalScraper.py
# Last updated 10/21/21

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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
            pass

    # desc: Goes to OddsPortal's login page to login
    #
    # Parameters:
    # ---------------
    # username : string
    #   User's OddsPortal username
    # 
    # password : string 
    #   User's OddsPortal password
    #
    # Returns: A boolean indicating whether or not login was successful
    def Login(self, username, password):
        # Go to login page
        loginURL = 'https://www.oddsportal.com/login/'
        self._webdriver.get(loginURL)

        # find input fields for username and password
        usernameInput = self._webdriver.find_element_by_id('login-username1')
        passwordInput = self._webdriver.find_element_by_id('login-password1')   
  
        # fill input fields with username and password respectively
        usernameInput.send_keys(username)
        passwordInput.send_keys(password)

        # submit page
        passwordInput.send_keys(Keys.ENTER)

        return (self._webdriver.current_url == 'https://www.oddsportal.com/' 
            or self._webdriver.current_url == 'https://www.oddsportal.com/settings/')

    # desc: Scrapes a match link for bet maker odds
    #
    # Parameters:
    # ---------------
    # link : string
    #   A link containing to OddsPortal containing the bet maker odds.
    #
    # Returns: A json object containing the bookmaker name as the key and the 
    # bookmaker odds as the value.
    def GetBetmakerOdds(self, link): 
        bookmakerOdds = {}

        # Go to link
        self._webdriver.get(link)

        # Get betmaker odds table
        tableElements = self._webdriver\
            .find_elements_by_css_selector('#odds-data-table > div.table-container > \
            table > tbody > tr')

        for element in tableElements:
            try:
                betmakerName = element.find_element_by_css_selector('td > div.l > a.name').text
                playerOneOdds, playerTwoOdds = element.find_elements_by_css_selector('td.right.odds > div')

                bookmakerOdds[betmakerName] = {
                    '0': playerOneOdds.text,
                    '1': playerTwoOdds.text,
                }
            except NoSuchElementException:
                pass
        
        return bookmakerOdds