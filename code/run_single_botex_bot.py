import logging
logging.basicConfig(level=logging.INFO)

import botex 

from dotenv import load_dotenv
load_dotenv('secrets.env')

# The missing config (botex_db, openai_api_key) will be read from the environment
botex.run_single_bot(
    url = "http://localhost:8000/InitializeParticipant/ca1cfrdk"
)
