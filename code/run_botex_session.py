import logging
logging.basicConfig(level=logging.INFO)

import botex 

from dotenv import load_dotenv
load_dotenv('secrets.env')

mftrust = botex.init_otree_session(config_name = "mftrust", npart = 10)

botex.run_bots_on_session(
  session_id = mftrust['session_id']
)