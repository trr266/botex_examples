import botex
from scipy import stats
from tabulate import tabulate

BOTEX_DB = 'data/external/botex_session_exp.sqlite3'
responses = botex.read_responses_from_botex_db(
  botex_db = BOTEX_DB
)
sent_amount_first_round = [
    r['answer'] for r in responses 
      if r['question_id'] == "id_sent_amount" and r['round'] == 1
]
print(tabulate({"Sent Amount": sent_amount_first_round}, headers = "keys"))
t_stat, p_value = stats.ttest_1samp(sent_amount_first_round, 50)

print("t statistic:", '{:.2f}'.format(t_stat))
print("p-value:", '{:.3f}'.format(p_value))
