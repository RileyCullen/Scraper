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