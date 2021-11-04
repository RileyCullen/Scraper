from Remove import RemoveTournaments
from FileWriter import WriteToJSON
from Scraper.OddsPortalScraper import OddsPortalScraper
import datetime, sys, threading, time

def Main():
    if len(sys.argv) < 2:
        print('Please enter username and password')
        return

    scraper = OddsPortalScraper(headless=True)
    scraper.Login(sys.argv[1], sys.argv[2])
    time.sleep(2)
    Crawl(scraper, sys.argv[1], sys.argv[2])

def Crawl(scraper, username, password):
    data = ParseTennis(scraper, username, password, {})
    print(data)
    WriteToJSON(data, 'data-multithreading.json')

def ParseTennis(scraper, username, password, data = {}):
    tournaments = RemoveTournaments(scraper.GetTournaments('https://www.oddsportal.com/tennis/'), ['Doubles'])
    threads = []
    dataLock = threading.Lock()
    for tournament in tournaments:
        print(tournament)
        tournamentScraper = OddsPortalScraper(headless=True)
        tournamentScraper.Login(username, password)
        
        th = threading.Thread(target=ParseTournament, args=(tournament, scraper\
            , data, dataLock))
        th.start()
        threads.append(th)
    
    for th in threads:
        th.join()
    return data

def ParseTournament(tournament, scraper, data, lock):
    print('\n**********Tournament: ' + tournament['name'])
    matches = scraper.GetMatches(tournament['link'])

    tournamentKey = tournament['name'].replace(' ', '-')
    hasTournamentKey = True
    # if the tournament entry does NOT exist, create one
    if (not (tournamentKey in data.keys())):
        hasTournamentKey = False

        try:
            lock.acquire()
            data[tournamentKey] = {}
        finally:
            lock.release()

    for match in matches:
        print('\n***************Match: ' + match['name'])
        matchKey = match['name']
        odds = scraper.GetBetmakerOdds(match['link'])

        try:
            lock.acquire()
            if (not hasTournamentKey or not (matchKey in data[tournamentKey].keys())):
                data[tournamentKey][matchKey] = {}
                data[tournamentKey][matchKey]['p1'], data[tournamentKey]\
                    [matchKey]['p2'] = match['name'].split(" - ")
            
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data[tournamentKey][matchKey][timestamp] = odds 
        finally:
            lock.release()

        print(odds)

if __name__ == '__main__':
    Main()