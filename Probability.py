# desc: Calculate the implied probability for every entry in data.
#
# Parameters:
# ---------------
# data : JSON
# 
# Returns: A JSON object with the implied probabilities
def CalculateProbability(data):
    tmp = {}
    for tournament in data:
        print(tournament)
        tmp[tournament] = {}
        for match in data[tournament]:
            print(match)
            tmp[tournament][match] = {}
            for timestamp in data[tournament][match]:
                print(timestamp)
                if (timestamp != 'p1' and timestamp != 'p2'):
                    tmp[tournament][match][timestamp] = {} 
                    for betmaker in data[tournament][match][timestamp]:
                        print(betmaker)
                        p1Odds = data[tournament][match][timestamp][betmaker]['0']
                        p2Odds = data[tournament][match][timestamp][betmaker]['1']
                        try:
                            tmp[tournament][match][timestamp][betmaker] = {
                                '0': 1 / float(p1Odds),
                                '1': 1 / float(p2Odds)
                            }
                        except ValueError:
                            print('Not a float')
    return tmp