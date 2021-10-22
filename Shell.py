from Scraper.OddsPortalScraper import OddsPortalScraper

# desc: Starting point for OddsPortal scraper shell
def main():
    isRunning = True
    print('Initializing OddsPortal scraper...')
    # Initialize webscraper
    scraper = OddsPortalScraper(headless = True)
    while(isRunning):
        # Get user's command and parse it into tokens
        request = input('[scraper] $ ')
        tokens = request.split(' ')

        if (tokens[0] == 'scrape'):
            pass
        elif (tokens[0] == 'login'):
            if (len(tokens) == 3):
                status = scraper.Login(tokens[1], tokens[2])
                if (status): print('Login Successful')
                else: print('Login Failed')
            else:
                PrintError('missing login info: login (username) (password)')
        elif (tokens[0] == 'quit'):
            isRunning = False

# desc: Print an error message     
def PrintError(message):
    print('Error: ' + message)
    
if __name__ == '__main__':
    main()