from Probability import CalculateProbability
from Remove import RemoveTournaments
from FileWriter import WriteToJSON
from FileReader import ReadFromJSON
from Scraper.OddsPortalScraper import OddsPortalScraper
import datetime, sys, threading, time, copy

def Main():
    if len(sys.argv) < 2:
        print('Please enter username and password')
        return

    scraper = OddsPortalScraper(headless=True)
    scraper.Login(sys.argv[1], sys.argv[2])
    Crawl(scraper, sys.argv[1], sys.argv[2])

def Crawl(scraper, username, password):
    startTime = time.time()

    readFromFile = input('Read from existing file (Y/N)? ')
    filename = ''

    data = {}
    if (readFromFile == 'Y' or readFromFile == 'y'):
        filename = input('Read from: ')
        data = ReadFromJSON(filename)
    else:
        filename = input('Data output filename: ')

    scrapeCount = int(input('Scrape iterations (enter -1 for infinite): '))

    print('Scraping... (note this may take a while)')
    while (scrapeCount > 0):
        data = ParseTennis(scraper, username, password, data)
        probabilityData = CalculateProbability(data)
        WriteToJSON(data, filename)
        print('Elapsed: ' + str(time.time() - startTime))
        scrapeCount -= 1

def ParseTennis(scraper, username, password, data = {}):
    time.sleep(3)
    tournaments = RemoveTournaments(scraper.GetTournaments('https://www.oddsportal.com/tennis/'), ['Doubles'])
    threads = []

    for tournament in tournaments:
        tournamentScraper = OddsPortalScraper(headless=True)
        tournamentScraper.Login(username, password)
        dataCopy = copy.deepcopy(data)

        th = TournamentParser(target=ParseTournament, args=(tournament, tournamentScraper\
            , dataCopy))
        th.start()
        threads.append(th)

    tmp = {}
    tArr = []

    for th in threads:
        tArr.append(th.join())

    print('Combining data...')
    for tData in tArr:
        for key in tData:
            if (key not in tmp.keys()):
                tmp[key] = {}
            for match in tData[key]:
                if (match not in tmp[key].keys()):
                    tmp[key][match] = {}
                for timestamp in tData[key][match]:
                    if (timestamp not in tmp[key][match]):
                        tmp[key][match][timestamp] = tData[key][match][timestamp]

    return tmp

def ParseTournament(tournament, scraper, data):
    # print('\n**********Tournament: ' + tournament['name'])
    matches = scraper.GetMatches(tournament['link'])
    # print(matches)
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