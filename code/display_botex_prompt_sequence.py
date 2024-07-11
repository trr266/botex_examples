import botex
from tabulate import tabulate

import json

# Adjust this to where you stored the botex data 
BOTEX_DB = 'data/external/botex_single_exp.sqlite3'

# Reading response data from botex database
conv = botex.read_conversations_from_botex_db(
  botex_db = BOTEX_DB
)

prompt_sequence = json.loads(conv[0]['conversation'])
print(tabulate(prompt_sequence, headers="keys"))