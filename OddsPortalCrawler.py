from Probability import CalculateProbability
from Remove import RemoveTournaments
from FileWriter import WriteToJSON
from FileReader import ReadFromJSON
from Scraper.OddsPortalScraper import OddsPortalScraper
import datetime, sys, threading, time, copy

# desc: Defines entry point into the program.
def Main():
    # Don't proceed with the program unless the user gives a username and 
    # password.
    if len(sys.argv) < 2:
        print('Please enter username and password')
        return

    # Create a scraper object to login and obtain tournament information
    scraper = OddsPortalScraper(headless=True)
    scraper.Login(sys.argv[1], sys.argv[2])
    Crawl(scraper, sys.argv[1], sys.argv[2])

# desc: Defines crawling logic.
def Crawl(scraper, username, password):
    startTime = time.time()

    # Get user input on if we want to read from an existing file or not.
    readFromFile = input('Read from existing file (Y/N)? ')
    filename = ''

    data = {}
    if (readFromFile == 'Y' or readFromFile == 'y'):
        # If yes, get user input on which filename we should read from.
        filename = input('Read from: ')
        data = ReadFromJSON(filename)
    else:
        # If no, define the new filename you want to create
        filename = input('Data output filename: ')

    # Get input on how many iterations the scraper should run for.
    scrapeCount = int(input('Scrape iterations (enter -1 for infinite): '))

    # Actual crawling code
    print('Scraping... (note this may take a while)')
    while (scrapeCount > 0):
        data = ParseTennis(scraper, username, password, data)
        WriteToJSON(data, filename)
        print('Elapsed: ' + str(time.time() - startTime))
        scrapeCount -= 1

# Desc: Defines how to collect and structure the odds data.
def ParseTennis(scraper, username, password, data = {}):
    time.sleep(3)
    # Get all the tournaments and remove doubles matches.
    tournaments = RemoveTournaments(scraper.GetTournaments('https://www.oddsportal.com/tennis/'), ['Doubles'])
    threads = []

    for tournament in tournaments:
        # For each tournament, create an OddsPortalScraper, login, then create
        # a new thread object for the tournament scraper.
        tournamentScraper = OddsPortalScraper(headless=True)
        tournamentScraper.Login(username, password)
        dataCopy = copy.deepcopy(data)

        # Pass the current tournament link, the current scraper, and a copy of 
        # the existing data to the thread. Start the thread.
        th = TournamentParser(target=ParseTournament, args=(tournament, tournamentScraper\
            , dataCopy))
        th.start()
        threads.append(th)

    tmp = {}
    tArr = []

    # Wait for all the threads to finish. On finish, each thread will return
    # the tournament data (matches, timestamps, odds, etc).
    for th in threads:
        tArr.append(th.join())

    # Combine data into one dictionary object.
    print('Combining data...')
    # Run loop for all the data returned from each thread (tArr).
    for tData in tArr:
        # For each key in tArr (note this should only be 1)
        for key in tData:
            # Create a new tournament entry in tmp if the key does not exist.
            if (key not in tmp.keys()):
                tmp[key] = {}
            # For each match in the tournament
            for match in tData[key]:
                # Create a new match entry in tmp if the key does not exist
                if (match not in tmp[key].keys()):
                    tmp[key][match] = {}
                # For each timestamp in the match data
                for timestamp in tData[key][match]:
                    # Create a new timestamp if the key does not exist.
                    if (timestamp not in tmp[key][match]):
                        tmp[key][match][timestamp] = tData[key][match][timestamp]

    return tmp

# desc: Defines scraping logic. NOTE that this is the function that each thread
# will be running.
def ParseTournament(tournament, scraper, data):
    matches = scraper.GetMatches(tournament['link'])
    tournamentKey = tournament['name'].replace(' ', '-')
    hasTournamentKey = True
    # if the tournament entry does NOT exist, create one
    if (not (tournamentKey in data.keys())):
        hasTournamentKey = False
        data[tournamentKey] = {}

    for match in matches:
        # print('\n***************Match: ' + match['name'])
        matchKey = match['name']
        odds = scraper.GetBetmakerOdds(match['link'])

        # if the tournament entry did NOT exist originally or matchKey does NOT
        # exist in data[tournamentKeys]
        if (not hasTournamentKey or not (matchKey in data[tournamentKey].keys())):
            data[tournamentKey][matchKey] = {}
            data[tournamentKey][matchKey]['p1'], data[tournamentKey]\
                [matchKey]['p2'] = match['name'].split(" - ")
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data[tournamentKey][matchKey][timestamp] = odds 
    return data

# I am too lazy to properly document this class, but essentially, we need to 
# create this so that each thread has a return value.
class TournamentParser(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    
    # desc: Scraper the tournament link for matches, then the matches for odds
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    # desc: Wait for thread to complete then return the scraped data
    def join(self):
        threading.Thread.join(self)
        return self._return

if __name__ == '__main__':
    Main()