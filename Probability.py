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

# desc : Remove the bookmaker influence from the scraped odds.
# 
# Parameters:
# ---------------
# p0 : float 
#   The non-adjusted bookmaker odd of pN winning.
# margin : float
def AdjustProbability(p0, margin):
    return ((2 * p0) / (2 - (margin * p0)))

# desc : Calculate the margin
#
# Parameters:
# ---------------
# p1 : float
# p2 : float
def CalculateMargin(p1, p2):
    return ((1 / p1) + (1 / p2) - 1)