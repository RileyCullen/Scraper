# desc: Remove all tournament entries from tournaments that have a given keyword
#       in their text.
#
# Parameters:
# ---------------
# tournaments : json
# keywords    : list
def RemoveTournaments(tournaments, keywords):
    tmp = []
    for tournament in tournaments:
        for keyword in keywords:
            if keyword not in tournament['name']:
                tmp.append(tournament)
    return tmp