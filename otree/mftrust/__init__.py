import string
import random

from otree.api import *
# This code is an adjusted variant of the oTree example code

doc = """
This is a variant of the classic trust game by
<a href="https://doi.org/10.1006/game.1995.1027" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>. In this variant, the manager can send a message to the investor
prior to their first investment decision.
"""

class C(BaseConstants):
    NAME_IN_URL = 'mftrust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    ENDOWMENT = cu(100)
    MULTIPLIER = 3

# This is running the N*(1/62^4) risk that two public IDs are identical.
# I am willing to take that risk ;-)
 
def create_id():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    id_public = ''.join(random.choices(chars, k = 4))
    id_private = ''.join(random.choices(chars, k = 4))
    return("{} {}".format(id_public, id_private))

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    message = models.LongStringField(
        label="Please enter your message to the investor:",
        blank=True
    )
    sent_amount = models.CurrencyField(
        min=cu(0),
        max=C.ENDOWMENT,
        doc="""Amount to invest into the firm:""",
        label="Please enter an amount from 0 to 100:",
    )
    sent_back_amount = models.CurrencyField(
        min=cu(0),
        max=sent_amount*C.MULTIPLIER,
        doc="""Dividend to be paid out to the investor:""",
    )

class Player(BasePlayer):
    wealth = models.CurrencyField(initial = cu(0))
    comprehension_check = models.IntegerField(
        label="What is the role of the multiplier in the experiment?",
        blank=False,
        choices=[
            [1, 'It increases the private wealth of the investor'],
            [2, 'It increases the private wealth of the manager'],
            [3, 'It increases the invested amount, ' + 
            'potentially benefiting both the investor and the manager'],
        ],
    )
    manipulation_check = models.IntegerField(
        label="What was your role in the experiment?",
        blank=False,
        choices=[
            [1, 'Investor'],
            [2, 'Manager'],
        ]
    )

    altruism = models.IntegerField(
        label="I am willing to help others even if I expect that I will never meet them again.",
        blank=False,
        choices = [
            [1, 'Absolutely'],
            [2, 'Very'],
            [3, 'Moderately'],
            [4, 'Slightly'],
            [5, 'Not at all']
        ]
    )
    trust = models.IntegerField(
        label="I believe that most people can be trusted.",
        blank=False,
        choices = [
            [1, 'Absolutely'],
            [2, 'Very'],
            [3, 'Moderately'],
            [4, 'Slightly'],
            [5, 'Not at all']
        ]
    )
    reciprocity = models.IntegerField(
        label="I am willing to incur costs to help someone who has helped me before.",
        blank=False,
        choices = [
            [1, 'Absolutely'],
            [2, 'Very'],
            [3, 'Moderately'],
            [4, 'Slightly'],
            [5, 'Not at all']
        ]
    )
    negative_reciprocity = models.IntegerField(
        label="If someone puts me in a difficult position, I would do the same to that person.",
        blank=False,
        choices = [
            [1, 'Absolutely'],
            [2, 'Very'],
            [3, 'Moderately'],
            [4, 'Slightly'],
            [5, 'Not at all']
        ]
    )

    feedback = models.LongStringField(
        label="Do you have any feedback that you want to share?",
        blank=True
    )


# --- Functions ----------------------------------------------------------------

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.wealth = cu(0)
            p.participant.part_id = create_id()
    
def sent_back_amount_max(group: Group):
    return group.sent_amount * C.MULTIPLIER

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.sent_amount == cu(0): group.sent_back_amount = cu(0)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount
    p1.participant.wealth += p1.payoff
    p2.participant.wealth += p2.payoff


# --- Pages --------------------------------------------------------------------
    
class Introduction(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Message(Page):
    """This page is only for P2 and only in the first round
    P2 has the option to send a free form text message to P1"""

    form_model = 'group'
    form_fields = ['message']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2 and player.round_number == 1

class SendWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    pass

class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        message = group.in_round(1).message
        message_exists = message != ""
        return dict(message_exists=message_exists, message=message)


class SendBackWaitPage(WaitPage):
    pass

class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'

    @staticmethod
    def get_form_fields(player):
        if player.group.sent_amount > 0:
            return ['sent_back_amount']
        else:
            return []

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(tripled_amount=tripled_amount)

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(
            tripled_amount=group.sent_amount * C.MULTIPLIER,
            p1_wealth=group.get_player_by_id(1).participant.wealth,
            p2_wealth=group.get_player_by_id(2).participant.wealth
        )

class Checks(Page):
    """This page is displayed after the experimental run is complete."""
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    
    form_model = 'player'
    form_fields = [
        'comprehension_check', 'manipulation_check', 
        'altruism', 'trust', 'reciprocity', 'negative_reciprocity',
        'feedback'
    ]

class Thanks(Page):
    """This page is displayed after the experimental run is complete."""
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            participant_id=player.participant.part_id
        )
    


page_sequence = [
    Introduction,
    Message,
    SendWaitPage,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
    Checks,
    Thanks
]
