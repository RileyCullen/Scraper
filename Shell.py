from Scraper.OddsPortalScraper import OddsPortalScraper
from View import ViewJSON
from FileWriter import WriteToJSON

# desc: Starting point for OddsPortal scraper shell
def main():
    isRunning = True
    print('Initializing OddsPortal scraper...')
    # Initialize webscraper
    scraper = OddsPortalScraper(headless = True)
    view = ViewJSON()
    while(isRunning):
        # Get user's command and parse it into tokens
        request = input('[scraper] $ ')
        tokens = request.split(' ')

        if (tokens[0] == 'scrape'):
            # if only 'scrape' is typed, then start from /tennis/ and scrape down
            if (len(tokens) == 1):
                data = ParseTennis(scraper)
                view.SetData(data)
        elif (tokens[0] == 'login'):
            if (len(tokens) == 3):
                status = scraper.Login(tokens[1], tokens[2])
                if (status): print('Login Successful')
                else: print('Login Failed')
            else:
                PrintError('missing login info: login (username) (password)')
        elif (tokens[0] =='view'):
            if (len(tokens) == 2):
                if (tokens[1] == 'tournaments'):
                    tournaments = view.GetTournaments()
                    print('\nTournament List:')
                    for tournament in tournaments:
                        print(tournament)
                    print('\n')
            if (len(tokens) == 3):
                if (tokens[1] == 'matches'):
                    matches = view.GetMatches(tokens[2])
                    print('\nMatch List:')
                    for match in matches:
                        print(match)
                    print('\n')
        elif (tokens[0] == 'write'):
            filename = 'data.json'
            if (len(tokens) == 2):
                filename = tokens[1]
            WriteToJSON(data, filename)
        elif (tokens[0] == 'quit'):
            isRunning = False

# desc: Print an error message     
def PrintError(message):
    print('Error: ' + message)

# desc: Start at /tennis/ page, find all of the tournaments, then find all of
# the tournament matches and scrape that for betmaker odds
#
# Parameters:
# ---------------
# scraper : OddsPortalScraper
#   Scraper object we want to use
def ParseTennis(scraper):
    tournaments = scraper.GetTournaments('https://www.oddsportal.com/tennis/')

    print('\nParsing results from /tennis/ page...')

    data = {}

    for tournament in tournaments:
        print('\n**********Tournament: ' + tournament['name'])
        matches = scraper.GetMatches(tournament['link'])

        tournamentKey = tournament['name'].replace(' ', '-')
        data[tournamentKey] = {}

        matchCount = 0
        for match in matches:
            print('\n***************Match: ' + match['name'])
            odds = scraper.GetBetmakerOdds(match['link'])

            data[tournamentKey][matchCount] = {}
            data[tournamentKey][matchCount]['p1'], data[tournamentKey]\
                [matchCount]['p2'] = match['name'].split(" - ")
            data[tournamentKey][matchCount]['odds'] = odds

            print(odds)
            matchCount += 1

if __name__ == '__main__':
    main()