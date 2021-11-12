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
        tmp[tournament] = {}
        for match in data[tournament]:
            tmp[tournament][match] = {}
            for timestamp in data[tournament][match]:
                if (timestamp != 'p1' and timestamp != 'p2'):
                    tmp[tournament][match][timestamp] = {} 
                    for betmaker in data[tournament][match][timestamp]:
                        try: 
                            p1Odds = float(data[tournament][match][timestamp]\
                                [betmaker]['0'])
                            p2Odds = float(data[tournament][match][timestamp]\
                                [betmaker]['1'])
                        except ValueError:
                            pass

                        margin = CalculateMargin(p1Odds, p2Odds)
                        adjustedP1Odds = AdjustProbability(p1Odds, margin)
                        adjustedP2Odds = AdjustProbability(p2Odds, margin)

                        tmp[tournament][match][timestamp][betmaker] = {
                            '0': 1 / adjustedP1Odds,
                            '1': 1 / adjustedP2Odds
                        }
    return tmp

# desc : Remove the bookmaker influence from the scraped odds.
# 
# Parameters:
# ---------------
# p0 : float 
#   The non-adjusted bookmaker odd of pN winning.
# margin : float
def AdjustProbability(p0, margin):
    return ((2.0 * p0) / (2.0 - (margin * p0)))

# desc : Calculate the margin
#
# Parameters:
# ---------------
# p1 : float
# p2 : float
def CalculateMargin(p1, p2):
    return ((1.0 / p1) + (1.0 / p2) - 1.0)