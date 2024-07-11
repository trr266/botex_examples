import botex
from tabulate import tabulate

# Adjust this to where you stored the botex data 
BOTEX_DB = 'data/external/botex_single_exp.sqlite3'

# Reading response data from botex database
responses = botex.read_responses_from_botex_db(
  botex_db = BOTEX_DB
)
print(tabulate(responses, headers="keys"))