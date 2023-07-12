import json
import os
import re
from typing import List

from services.service import PublishSubscribe
from services.service import Service
from utils import UserAct, UserActionType
from utils.beliefstate import BeliefState
from utils.common import Language
from utils.domain.jsonlookupdomain import JSONLookupDomain
from utils.logger import DiasysLogger
from utils.sysact import SysAct, SysActionType



def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CollegeAdviser(Service):
    """
    Class that accesses the soloist model trained on some college-data-dialogues.
    It is an end-to-end approach that does NLU, BST, Policy and NLG on its own.
    Class for Handcrafted Natural Language Understanding Module (HDC-NLU).
    """

    def __init__(self, domain: JSONLookupDomain, logger: DiasysLogger = DiasysLogger(),
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
            domain {domain.jsonlookupdomain.JSONLookupDomain} -- Domain
        """
        Service.__init__(self, domain=domain)
        self.model_path = '/mount/studenten-temp1/users/zabereus/adviser/soloist_env/soloist/examples/college_bot/college_model'
        self.logger = logger
        self.language = language if language else Language.ENGLISH
        self.domain_name = domain.get_domain_name()


    def dialog_start(self):
        """
        Initiates the trained soloist model

        """
        args.model_name_or_path = self.model_path
        main()

    @PublishSubscribe(sub_topics=["user_utterance"], pub_topics=["sys_acts"])
    def communicate(self,user_utterance: str = None):
        """
        """
        system_utterance, beliefstate = predictor([user_utterance])

        return {'sys_utterance': system_utterance}