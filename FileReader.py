import json

# desc: Reads the .json file specified by path then stores the file contents in
#       a python dictionary
#
# Parameters:
# ---------------
# path : str
#   The path to the .json file you want to open
#
# Returns: A python dictionary with the contents of the file specified by path.
def ReadFromJSON(path):
    tmp = {}
    with open(path) as f:
        tmp = json.load(f)
    return tmp