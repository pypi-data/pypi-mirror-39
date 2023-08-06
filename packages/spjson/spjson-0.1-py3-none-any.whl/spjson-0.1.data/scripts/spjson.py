import pandas as pd
from pandas.io.json import json_normalize
import flatten_json
import json

def openJSONfile(inputFile):
     f = open(inputFile)
     a_string = f.read()
     data = json.loads(a_string)         
     f.close()
     return data
     
def flattern_json_to_df(inputFile):
     data = openJSONfile(inputFile)
     flat = flatten_json.flatten_json(data)
     df = json_normalize(flat)
     return df