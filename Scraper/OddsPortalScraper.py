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
         
        # switch to EU odds
        self._SwitchToEUOdds()

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
                # Get the odds and store it
                odds = element.find_elements_by_css_selector('td.right.odds > div')

                # If the request is empty (this occurs when the odds are not 
                # div elements and are actually links), then get these links 
                # instead
                aOdds = element.find_elements_by_css_selector('td.right.odds > a') 
                if aOdds != []:
                    for a in aOdds:
                        odds.append(a)

                bookmakerOdds[betmakerName] = {
                    '0': odds[0].text,
                    '1': odds[1].text
                }
            except NoSuchElementException:
                pass
        
        return bookmakerOdds

    # desc: Scrapes a tournament link for matches 
    #
    # Parameters: 
    # ---------------
    # link : string
    #   A link to a tournament on OddsPortal (containing individual matches)
    #
    # Returns: An array of links to individual matches
    def GetMatches(self, link): 
        matches = []

        # Go to link
        self._webdriver.get(link)

        # Get all the links to the matches
        matchLinks = self._webdriver.find_elements_by_css_selector('td.name.table-participant > a')

        for link in matchLinks:
            # Get link's href attribute
            href = link.get_attribute('href')

            # if the first letter is an 'h', then this is a real link (to a match)
            # and we need to add it to matches.
            if (href[0] == 'h' and link.text != ""):
                tmp = {
                    'name': link.text,
                    'link': href
                }
                matches.append(tmp)
    
        return matches

    # desc: Scrapes the tennis page for tournament links
    # 
    # Parameters:
    # ---------------
    # link : string 
    #   A link to the OddsPortal tennis page
    #
    # Returns: An array of links to the tournament 
    def GetTournaments(self, link):
        tournaments = []

        # Go to link
        self._webdriver.get(link)

        # Get tournament entires 
        tournamentLinks = self._webdriver.find_elements_by_css_selector('td > \
            a[foo="f"]')
        
        # For each entry, get the tournament name and link to tournament page
        for tournament in tournamentLinks:
            tmp = {
                'name': tournament.text,
                'link': tournament.get_attribute('href')
            }
            tournaments.append(tmp)
        
        return tournaments

    # desc: Switches the OddsPortal odds to display EU odds
    def _SwitchToEUOdds(self):
        # Find dropdown list with all oof the options and click on it (expand it)
        expander = self._webdriver.find_element_by_css_selector('#user-header-oddsformat-expander')
        expander.click()

        # Find the options in the expanded dropdown menu
        elems = self._webdriver.find_elements_by_css_selector('#user-header-oddsformat > li > a')
        
        # For each option found, check the text content. If it says "EU Odds",
        # then click on it
        for elem in elems:
            if elem.text == 'EU Odds':
                elem.click()