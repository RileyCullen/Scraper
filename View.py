# Cullen, Riley
# View.py
# Created on 10/23/21

import pandas

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
            tmp.append(str(matches))
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
            if (timestamp != 'p1' and timestamp != 'p2'):
                tmp.append(timestamp)
        return tmp

    # desc: Returns the betmaker odds for a given timestamp
    #
    # Parameters:
    # ---------------
    # tournamentKey : string
    # matchKey : string
    # timestamp : string 
    #
    # Returns: A pandas DataFrame containing the odds information
    def GetBetmakerOdds(self, tournamentKey, matchKey, timestamp):
        tmp = []
        timestamps = self._data[tournamentKey][matchKey][timestamp]
        col_list = ['p1', 'p2']
        row_list = []
        for odds in timestamps:
            row_list.append(odds)
            tmp.append([timestamps[odds]['0'], timestamps[odds]['1']])
        return pandas.DataFrame(tmp, row_list, col_list)