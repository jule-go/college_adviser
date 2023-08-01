import json
import os
import re
from typing import List

# imports needed for our trained soloist model
from soloist.examples.college_bot.soloist.server import *
from soloist.examples.college_bot.collegebot_server import *

from adviser.services.service import PublishSubscribe
from adviser.services.service import Service
from adviser.utils import UserAct, UserActionType
from adviser.utils.beliefstate import BeliefState
from adviser.utils.common import Language
# from adviser.utils.domain.jsonlookupdomain import JSONLookupDomain
from adviser.utils.domain import Domain
from adviser.utils.logger import DiasysLogger
from adviser.utils.sysact import SysAct, SysActionType
from adviser.utils.topics import Topic



def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CollegeAdviser(Service):
    """
    Class that accesses the soloist model trained on some college-data-dialogues.
    It is an end-to-end approach that does NLU, BST, Policy and NLG on its own.
    Class for Handcrafted Natural Language Understanding Module (HDC-NLU).
    """

    def __init__(self, domain: Domain = None, logger: DiasysLogger = DiasysLogger(),
                language: Language = None):
        """
        Loads
            - domain key
            - informable slots
            - requestable slots
            - domain-independent regular expressions
            - domain-specific regualer espressions

        It sets the previous system act to None

        Args:
            domain {Domain} -- Domain
        """
        Service.__init__(self, domain=domain)
        self.model_path = '/mount/studenten-temp1/users/zabereus/adviser/soloist_env/soloist/examples/college_bot/college_model'
        self.logger = logger
        self.language = language if language else Language.ENGLISH
        self.domain_name = domain.get_domain_name() if domain else ""
        self.conversation_tracker = [] # to keep track of conversation between user and system


    def dialog_start(self):
        """
        Initiates the trained soloist model

        """
        # from college_adviser.soloist.examples.college_bot.soloist.server import *
        args.model_name_or_path = self.model_path
        main() # of server
        self.dialogue_history = [] # keep track of user and system utterances

    @PublishSubscribe(sub_topics=["gen_user_utterance"], pub_topics=["sys_utterance"])
    def communicate(self, gen_user_utterance: str = None):
        """
        available topics: user_utterance user_acts sys_state sys_act sys_utterance beliefstate
        """
        #print("arrived here")
        user_utterance = gen_user_utterance
        self.dialogue_history += [user_utterance]
        with contextlib.redirect_stdout(None):
            system_utterance, beliefstate = get_response(self.dialogue_history)
        self.dialogue_history += [system_utterance]

        return {'sys_utterance': system_utterance}

