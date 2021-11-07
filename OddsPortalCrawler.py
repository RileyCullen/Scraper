from Remove import RemoveTournaments
from FileWriter import WriteToJSON
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
    data = ParseTennis(scraper, username, password, {})
    print(data)
    WriteToJSON(data, 'data-multithreading.json')
    print('Elapsed: ' + str(time.time() - startTime))

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
    for th in threads:
        tData = th.join()
        for key in tData:
            tmp[key] = tData[key]
    return tmp

def ParseTournament(tournament, scraper, data):
    print('\n**********Tournament: ' + tournament['name'])
    matches = scraper.GetMatches(tournament['link'])
    print(matches)
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
        print('joined')
        threading.Thread.join(self)
        return self._return

if __name__ == '__main__':
    Main()