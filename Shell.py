from Scraper.OddsPortalScraper import OddsPortalScraper
from View import ViewJSON
from FileWriter import WriteToJSON
from FileReader import ReadFromJSON

import datetime

# desc: Starting point for OddsPortal scraper shell
def main():
    isRunning = True
    print('Initializing OddsPortal scraper...')
    # Initialize webscraper
    scraper = OddsPortalScraper(headless = True)
    view = ViewJSON()
    data = {}
    while(isRunning):
        # Get user's command and parse it into tokens
        request = input('[scraper] $ ')
        tokens = request.split(' ')

        if (tokens[0] == 'scrape'):
            # if only 'scrape' is typed, then start from /tennis/ and scrape down
            if (len(tokens) == 1):
                data = ParseTennis(scraper, data)
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
                    PrintTournaments(view)
                elif (tokens[1] == 'matches'):
                    PrintTournaments(view)
                    tournament = input('Tournament: ')
                    PrintMatches(view, tournament)
                elif (tokens[1] == 'timestamps'):
                    PrintTournaments(view)
                    tournament = input('Tournament: ')
                    PrintMatches(view, tournament)
                    match = input('Match: ')
                    PrintTimestamps(view, tournament, match)
                elif (tokens[1] == 'odds'):
                    PrintTournaments(view)
                    tournament = input('Tournament: ')
                    PrintMatches(view, tournament)
                    match = input('Match: ')
                    PrintTimestamps(view, tournament, match)
                    timestamp = input('Timestamp: ')
                    PrintOdds(view, tournament, match, timestamp)
        elif (tokens[0] == 'write'):
            filename = 'data.json'
            if (len(tokens) == 2):
                filename = tokens[1]
            WriteToJSON(data, filename)
        elif (tokens[0] == 'read'):
            if (len(tokens) == 2):
                data = ReadFromJSON(tokens[1])
                view.SetData(data)
        elif (tokens[0] == 'quit'):
            isRunning = False

# desc: Print an error message     
def PrintError(message):
    print('Error: ' + message)

# desc: Print title, followed by the contents of list
def PrintList(list, title):
    print('\n' + title)
    for elem in list:
        print(elem)
    print('\n')

# desc: Print all of the tournaments stored in data
def PrintTournaments(view):
    tournaments = view.GetTournaments()
    PrintList(tournaments, 'Tournaments: ')

# desc: Print all of the matches for a given tournament
def PrintMatches(view, tournament):
    matches = view.GetMatches(tournament)
    PrintList(matches, 'Matches: ')

# desc: Print all of the timestamps for a given match
def PrintTimestamps(view, tournament, match):
    timestamps = view.GetMatchTimestamps(tournament, match)
    PrintList(timestamps, 'Timestamps: ') 

# desc: Print all of the betmaker odds for a given timestamp
def PrintOdds(view, tournament, match, timestamp):
    odds = view.GetBetmakerOdds(tournament, match, timestamp)
    print(odds)

# desc: Start at /tennis/ page, find all of the tournaments, then find all of
# the tournament matches and scrape that for betmaker odds
#
# Parameters:
# ---------------
# scraper : OddsPortalScraper
#   Scraper object we want to use
def ParseTennis(scraper, data = {}):
    tournaments = scraper.GetTournaments('https://www.oddsportal.com/tennis/')

    print('\nParsing results from /tennis/ page...')

    for tournament in tournaments:
        print('\n**********Tournament: ' + tournament['name'])
        matches = scraper.GetMatches(tournament['link'])

        tournamentKey = tournament['name'].replace(' ', '-')
        hasTournamentKey = True
        # if the tournament entry does NOT exist, create one
        if (not (tournamentKey in data.keys())):
            hasTournamentKey = False
            data[tournamentKey] = {}

        for match in matches:
            print('\n***************Match: ' + match['name'])
            matchKey = match['name']
            odds = scraper.GetBetmakerOdds(match['link'])

            if (not hasTournamentKey or not (matchKey in data[tournamentKey].keys())):
                data[tournamentKey][matchKey] = {}
                data[tournamentKey][matchKey]['p1'], data[tournamentKey]\
                    [matchKey]['p2'] = match['name'].split(" - ")
            
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data[tournamentKey][matchKey][timestamp] = odds 

            print(odds)
    return data

if __name__ == '__main__':
    main()