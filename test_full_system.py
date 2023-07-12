# imports
from services.service import DialogSystem
from services.hci.console import ConsoleInput,ConsoleOutput
from utils.domain.jsonlookupdomain import JSONLookupDomain
from services.hci.gui import GUIServer
from services.soloist_interaction.college_system import CollegeAdviser

# testing the system
if __name__ == "__main__":
    #gui_service = GUIServer()
    current_domain = JSONLookupDomain(name='college')
    user_in = ConsoleInput()
    user_out = ConsoleOutput()
    college_adviser = CollegeAdviser(domain=current_domain)
    #ds = DialogSystem(services=[domain_tracker,nlu,bst,policy,nlg,gui_service])
    ds = DialogSystem(services=[college_adviser,user_in,user_out])
    error_free = ds.is_error_free_messaging_pipeline()
    if not error_free:
        ds.print_inconsistencies()
        #ds.draw_system_graph()
    ds.run_dialog({"gen_user_utterance":""})
    ds.shutdown()