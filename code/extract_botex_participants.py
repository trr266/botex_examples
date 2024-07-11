import botex
from tabulate import tabulate

# Adjust this to where you stored the botex data 
BOTEX_DB = 'data/external/botex_single_exp.sqlite3'
part = botex.read_participants_from_botex_db(
  botex_db = BOTEX_DB
)
disp_part = [
  [r[v] for v in ('session_name', 'participant_id', 'is_human', 'time_in','time_out')] 
  for r in part
]
print(tabulate(
  disp_part, 
  headers=["Session", "Participant ID", "Is Human?", "Time in", "Time out"]
))