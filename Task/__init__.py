from otree.api import *
import numpy.random as rnd  
import random 
import pandas as pd 

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 54
    NUM_PROUNDS = 3

    # List of attributes (id)
    lAttrID     = ['p','s','q']
    lAttrNames  = ['Price','Sustainability','Quality']
    
    # Template vars
    lColNames   = ['Product 1','Product 2']


    # In between round messages
    BetweenTrialMessages = {
        "1": f"Now you will have {NUM_PROUNDS} practice rounds.", 
        str(int(NUM_PROUNDS+1)): "The practice rounds are over."
        }
    
    # Image paths 
    imgCandidate    = "global/figures/candidate.png"
    imgNumbers      = "global/figures/numbers/n_"
    imgStars        = "global/figures/stars/star_"
    imgLeafs        ="global/figures/leafs/leaf_"
    imgNegatives    ="global/figures/negatives/neg-eco-"
    
    # Confidence page
    iLikertConf     = 7
    sConfQuestion   = f"From 1 to {iLikertConf}, how confident are you on your choice?"
    sLeftConf       = "Very unsure"
    sRightConf      = "Very sure"

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # DVs
    sChoice     = models.StringField()
    dRT_dec     = models.FloatField()
    iConfidence = models.IntegerField()
    dRT_conf    = models.FloatField()

    # Attribute values
    P1=models.FloatField()
    P2=models.FloatField()
    S1=models.IntegerField()
    S2=models.IntegerField()
    Q1=models.IntegerField()
    Q2=models.IntegerField()


    # Attention variables
    sNames      = models.LongStringField(blank=True)
    sDT         = models.LongStringField(blank=True)

    # Timestamps
    sStartDec   = models.StringField()
    sEndDec     = models.StringField()
    sStartCross = models.StringField()
    sEndCross   = models.StringField()
    sStartConf = models.StringField()
    sEndConf   = models.StringField()


    # Others 
    sBetweenBtn = models.StringField()

    
def creating_session(subsession):
    # Load Session variables
    s = subsession.session 

    # Read CSV file
    csv_path_pos = "_static/global/table/positive_filtered_trials.csv" #filtered_trials_shuffled
    csv_path_neg = "_static/global/table/negative_filtered_trials.csv"
    trial_data_pos = pd.read_csv(csv_path_pos)
    trial_data_neg = pd.read_csv(csv_path_neg)

    if subsession.round_number==1: 
        for player in subsession.get_players():
            p = player.participant

            # Randomize order of attributes
            lPos = C.lAttrID[:]         # Create hard copy of attributes
            random.shuffle(lPos)        # Shuffle order
            p.lPos = lPos               # Store it as a participant variable
            
            # Select trial for payment (from the first round after practice rounds to the last)
            p.iSelectedTrial = random.randint(C.NUM_PROUNDS+1,C.NUM_ROUNDS)
            
            # Shuffle order of trials for each participant
            if p.sTreatment == "Positive":
                p.trial_data=trial_data_pos.sample(frac=1).reset_index(drop=True)
            else:
                p.trial_data = trial_data_neg.sample(frac=1).reset_index(drop=True)


    for player in subsession.get_players():
        p = player.participant
        player.sBetweenBtn = random.choice(['left','right'])
      
         # Practice Trials
        if player.round_number <= C.NUM_PROUNDS:
            
            # print(player.round_number, "practice")  
            if player.round_number == 1:
                lValues = [1.0,1.0, 1,1, 1,3]
            elif player.round_number == 2:
                lValues = [1.0,1.0, 1,3, 1,1] 
            elif player.round_number == 3:
                lValues = [3.0,1.0, 1,1, 1,1]
              
         # Normal Trials
        else:
            
            # print(player.round_number, "normal")
            trial_index=player.round_number - C.NUM_PROUNDS-1
            lValues = p.trial_data.iloc[trial_index].tolist() # lValues= p.database[int(player.round_number-4)]
            
        P1,P2,S1,S2,Q1,Q2 = lValues
        player.P1,player.P2, player.S1,player.S2,player.Q1,player.Q2 = P1,P2,int(S1),int(S2),int(Q1),int(Q2)


def attributeList(lValues,lPos,treatment): 
    lAttributes = []
    lOrder = []

    for i in range(len(C.lAttrID)):
        id                  = C.lAttrID[i]      
        name                = C.lAttrNames[i]  
        
        # Store the order of the list
        lOrder.append(lPos.index(id))
        lPaths = []
        for v in lValues[i]:
            if id=="q":
                 lPaths.append(f"{C.imgStars}{v}.png")
            elif id=="s" and treatment == "Positive":
                lPaths.append(f"{C.imgLeafs}{v}.png")
            elif id=="s" and treatment == "Negative":
                lPaths.append(f"{C.imgNegatives}{v}.png")
            else:
                lPaths.append(f"{C.imgNumbers}{v}.png")


        # Create object with all the relevant variables
        Attr = {
            'id'        : id,
            'name'      : name,
            'lValues'    : lPaths,
        }
        lAttributes.append(Attr)
    
    lFinal = [ lAttributes[x] for x in lOrder]
    return lFinal

# PAGES

class Message(Page):
    template_name = 'global/Message.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_PROUNDS
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            MessageText = 'The practice rounds ended. <br> The experiment will start now.'
        )

class Decision(Page):
    form_model      = 'player'
    # form_fields     = [ 'sChoice']
    form_fields     = [ 'sStartDec','sEndDec', 'dRT_dec', 'sNames', 'sDT' , 'sChoice'] #'dTime2first',
    
    @staticmethod
    def vars_for_template(player: Player):
        
        # Order of attributes (from participant var)
        p = player.participant
        lPos = p.lPos
        treatment=p.sTreatment
  

        # Candidates values          
      
        lValues = [[player.P1,player.P2],[player.S1,player.S2],[player.Q1,player.Q2]]
        print(lValues)
        return dict(
            lAttr = attributeList(lValues,lPos,treatment), 
        )
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        p = player.participant
        
        if player.round_number == p.iSelectedTrial: 
            p.bChoseA = player.iChooseB == 0   
            print(f"Decision in selected trial recorded: {p.bChoseA}")


class FixCross(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/FixCross.html'


class SideButton(Page):
    form_model = 'player'
    form_fields = [ 'sStartCross','sEndCross' ]
    template_name = 'global/SideButton.html'

    @staticmethod
    def js_vars(player: Player):
        
        return dict(
            sPosition = player.sBetweenBtn
        )


class Confidence(Page):
    form_model      = 'player'
    form_fields     = [ 'sStartConf','sEndConf', 'dRT_conf','iConfidence']
    template_name   = 'global/Confidence.html'
    
    @staticmethod
    def vars_for_template(player: Player):
        p = player.participant
        return dict(
            lScale = list(range(1,C.iLikertConf+1))
        )



page_sequence = [SideButton, Decision, Confidence, Message]

 
