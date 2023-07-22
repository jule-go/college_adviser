# imports 
from adviser.services.service import DialogSystem
from adviser.services.hci.console import ConsoleInput,ConsoleOutput
from adviser.utils.domain.jsonlookupdomain import JSONLookupDomain
# from adviser.services.hci.gui import GUIServer
from adviser.services.soloist_interaction.college_system import CollegeAdviser

# testing the system
if __name__ == "__main__":
    #gui_service = GUIServer()
    current_domain = JSONLookupDomain(name='college')
    user_in = ConsoleInput()
    user_out = ConsoleOutput()
    print("console configuration worked")
    college_adviser = CollegeAdviser(domain=current_domain)
    print("college adviser loaded")
    #ds = DialogSystem(services=[domain_tracker,nlu,bst,policy,nlg,user_in,user_out])
    ds = DialogSystem(services=[college_adviser,user_in,user_out])
    print("dialogue system loaded")
    error_free = ds.is_error_free_messaging_pipeline()
    print("is error free: ",error_free)
    if not error_free:
        ds.print_inconsistencies()
        ds.draw_system_graph()
    ds.run_dialog({"gen_user_utterance":""})
    ds.shutdown()