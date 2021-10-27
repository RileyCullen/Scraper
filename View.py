# Cullen, Riley
# View.py
# Created on 10/23/21

class ViewJSON:
    # desc: Constructor for ViewJSON class
    def __init__(self):
        self._data = 0

    # desc: Updates _data
    # 
    # Parameters:
    # ---------------
    # data : JSON object
    #   A JSON object consisting of data obtained from the OddsPortal
    def SetData(self, data):
        self._data = data

    # desc: Returns the tournaments in _data
    # Returns: An array of the tournament names in _data
    def GetTournaments(self):
        tmp = []
        for keys in self._data:
            tmp.append(keys)
        return tmp
    
    # desc: Returns the matches for a given tournament
    # 
    # Parameters:
    # --------------
    # tournamentKey : string 
    #   The tournament key needed to access the match data in _data
    #
    # Returns: An array of match data (key + players)
    def GetMatches(self, tournamentKey):
        tmp = []
        tournament = self._data[tournamentKey]
        for matches in tournament:
            tmp.append(str(matches) + ": " + tournament[matches]['p1'] + ' vs ' + \
                tournament[matches]['p2'])
        return tmp

    # desc: Returns the timestamps for a given match
    #
    # Parameters:
    # --------------
    # tournamentKey : string
    # matchKey : string 
    # 
    # Returns: An array of timestamp information.
    def GetMatchTimestamps(self, tournamentKey, matchKey):
        tmp = []
        match = self._data[tournamentKey][matchKey]
        for timestamp in match:
            tmp.append(timestamp)
        return tmp