from otree.api import *
import random
import pandas as pd
from collections import Counter
from numpy import random as rnd
import numpy as np
doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL         = 'Intro'
    PLAYERS_PER_GROUP   = None
    NUM_ROUNDS          = 1
    # Setup/Experiment variables 
    iPracticeRounds     = 3
    iOptions            = 54 # 3 x 6 x 4
    # iNumTrials          = 5
    iNumTrials          = iPracticeRounds + iOptions
    # Template variables
    AvgDur              = '30'
    iBonus              = '2.5'

    ## Symbols directory
    # Base
    UvA_logo            = 'global/figures/UvA_logo.png'
    path1               = 'global/figures/Not_mine/example1.png'
    path2               = 'global/figures/Not_mine/example2.png'
    pathGif             = 'global/figures/Not_mine/demoMouseCrop.gif'
    pathData            = '_static/global/files/Data4Exp.csv'

    # Folders
    imgNumbers      = "global/figures/numbers/n_"
    imgStars        = "global/figures/stars/star_"
    imgLeafs        ="global/figures/leafs/leaf_"
    imgNegatives    ="global/figures/negatives/neg-eco-"

    # Instructions
    OneTreePlanted      = "global/figures/Logo_OneTreePlanted.png"
    star_symbol         = "global/figures/one_star.png"
    leaf_symbol         = "global/figures/one_leaf.png"
    neg_symbol          = "global/figures/one-neg.png"
    revealed_pos        = "global/figures/revealed_task_pos.png"
    revealed_neg        = "global/figures/revealed_task_neg.png"
    circled_task_pos    = "global/figures/circled_task_pos.png"
    circled_task_neg    = "global/figures/circled_task_neg.png"

    # Gifs
    TreatPos          = "global/figures/TreatPos.gif"
    TreatNeg          = "global/figures/TreatNeg.gif"

    # Multiple leaf/neg/stars
    one_leaf            ="global/figures/leafs/leaf_1.png"
    two_leaf            ="global/figures/leafs/leaf_2.png"
    three_leaf          ="global/figures/leafs/leaf_3.png"
    one_neg             ="global/figures/negatives/neg-eco-1.png"
    two_neg             ="global/figures/negatives/neg-eco-2.png"
    three_neg           ="global/figures/negatives/neg-eco-3.png"
    three_star          = "global/figures/stars/star_3.png"

    # Links 
    # You might want to have different links, for when they submit differen answers
    sLinkReturn         = "https://app.prolific.com/submissions/complete?cc=XXXXX"
    sLinkReturnCal      = "https://app.prolific.com/submissions/complete?cc=YYYYY"
    sLinkOtherBrowser   = "https://YOUR-EXPERIMENT.herokuapp.com/room/room1"
    SubmitLink          = 'https://app.prolific.com/submissions/complete?cc=ZZZZZ'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass
    sTreesLocation = models.StringField()

# FUNCTIONS
    
def creating_session(subsession):
    # Load Session variables
    s = subsession.session 
    if subsession.round_number ==1:
        for player in subsession.get_players():
            # Store any treatment variables or things that stay constant across rounds/apps
            p = player.participant
            p.bTimeout = False
            # When creating the session, you can define whether you have a random treatment or a specific one. 
            if s.config['treatment']=='random':
                p.sTreatment = random.choice(['Positive','Negative'])
            else:
                p.sTreatment = s.config['treatment']
            # Randomly selected trial
            p.iSelectedTrial = random.randint(C.iPracticeRounds,C.iNumTrials)
            ## LOAD HERE YOUR DATABASE 



# PAGES


class Instructions(Page):
    form_model = 'player'
    form_fields = ['sTreesLocation']

    @staticmethod
    def js_vars(player: Player):
        ## Variables necessary for javascript
        p = player.participant
        return dict(
            lSolutions = [
                'a','c', 'a', str(C.iPracticeRounds) # Solutions to control questions
            ]
        )
    
    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        return dict(  
            pos_treatment =  p.sTreatment=="Positive" 

        )


page_sequence = [Instructions]