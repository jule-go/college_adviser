# imports 
from adviser.services.service import DialogSystem
from adviser.services.hci.console import ConsoleInput,ConsoleOutput
# from adviser.utils.domain.jsonlookupdomain import JSONLookupDomain
from adviser.utils.domain import Domain
# from adviser.services.hci.gui import GUIServer
from adviser.services.soloist_interaction.college_system import CollegeAdviser
from adviser.utils.topics import Topic

# testing the system
if __name__ == "__main__":
    print(">>> Hello, I'm CollegeBot. How can I help you?")
    domain_specific = False # do you want to specify the domain of the service?

    if domain_specific: # domain specific version
        current_domain = Domain("college")
        user_in = ConsoleInput(domain=current_domain)
        user_out = ConsoleOutput(domain=current_domain)
        # print("console configuration worked")
        college_adviser = CollegeAdviser(domain=current_domain)
        # print("college adviser loaded")
        dialogue_start_signals={"dialog_end/college": False}
    else:
        user_in = ConsoleInput()
        user_out = ConsoleOutput()
        # print("console configuration worked")
        college_adviser = CollegeAdviser()
        # print("college adviser loaded")
        dialogue_start_signals={}
    ds = DialogSystem(services=[college_adviser,user_out, user_in])
    # print("dialogue system loaded")
    error_free = ds.is_error_free_messaging_pipeline()
    # print("is error free: ",error_free)
    if not error_free:
        ds.print_inconsistencies()
        ds.draw_system_graph()
    if domain_specific:
        ds.run_dialog(dialogue_start_signals)
    else:
        ds.run_dialog()
    ds.shutdown()

        # ds.run_dialog() #"gen_user_utterance":"" Topic.DIALOG_START: True