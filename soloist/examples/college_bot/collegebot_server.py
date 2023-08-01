from flask import Flask, request, Response, jsonify
from flask import render_template
from flask_cors import CORS
import flask
import json, re
from collections import defaultdict
import random
from .db_interface import query_from_db
from .soloist.server import sample,sample2
from .soloist.server import main
from .soloist.server import *
import copy
import functools
from nltk.tokenize import sent_tokenize, word_tokenize
import os
from queue import Queue
from threading import Thread

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['HF_MODELS_CACHE'] = '/mount/studenten-temp1/users/zabereus/adviser/soloist_env/soloist/cache'
os.environ['TRANSFORMERS_CACHE'] = '/mount/studenten-temp1/users/zabereus/adviser/soloist_env/soloist/cache'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

app = Flask(__name__)
CORS(app)

rgi_queue = Queue(maxsize=0)
rgo_queue = Queue(maxsize=0)

def parse(sampled_results):
    
    candidates = []
    for system_response in sampled_results:
        system_response = system_response.split('system :')[-1]
        system_response = ' '.join(word_tokenize(system_response))
        system_response = system_response.replace('[ ','[').replace(' ]',']')
        candidates.append(system_response)

    candidates_bs = []
    for system_response in sampled_results:
        system_response = system_response.strip()
        system_response = system_response.split('system :')[0]
        system_response = ' '.join(system_response.split()[:])
        svs = system_response.replace(",", ";").split(';')
        bs_state = {}
        for sv in svs:
            if '=' in sv:
                s,v = sv.split('=')
                s = s.strip()
                v = v.strip()
                bs_state[s] = v
        candidates_bs.append(copy.copy(bs_state))

    candidates_w_idx = [(idx, v) for idx,v in enumerate(candidates)]
    candidates = sorted(candidates_w_idx, key=functools.cmp_to_key(compare))

    #print(candidates)
    #print("bs: ", candidates_bs)

    idx, response = candidates[-1]
    states = candidates_bs[idx]
    return states,response

def compare(key1, key2):
    key1 = key1[1]
    key2 = key2[1]
    if key1.count('[') > key2.count('['):
        return 1
    elif key1.count('[') == key2.count('['):
        return 1 if len(key1.split()) > len(key2.split()) else -1
    else:
        return -1  

def predictor(context, bs=None, db_state=None):
    context_formated = []
    for idx, i in enumerate(context):
        if idx % 2 == 0:
            context_formated.append(f'user : {i}')
        else:
            context_formated.append(f'system : {i}')
            
    if bs:
        sampled_results = sample2(context_formated, bs)
    else:
        #print(f"into server {context_formated}")
        sampled_results = sample(context_formated) #TODO oh that was bad, was [-1:]
    print("sampled results", sampled_results)
    belief_states, response = parse(sampled_results)
    print(f"response {response}, bs {belief_states}")
    return response, belief_states

def get_response(history: str):
    #print("now predicting...")
    memory = []
    _, belief_states = predictor(history)

    if belief_states != {}:
        t = []
        for s,v in belief_states.items():
            if s != "options":
                t.append(f'{s} = {v}')
        memory.append(' ; '.join(t))
    #print("memory", memory)

    options, rows = query_from_db(beliefstate=memory[-1])

    memory[-1] += f"; options = {options}" # = memory[-1].replace("options = \d", f"options = {options}")
    response, _ = predictor([history[-1]], memory[-1])
    

    followup = fill_delex(response, rows)

    return followup, belief_states


global_counter = 0
@app.route('/generate', methods=['GET','POST'])
def generate_queue():
    global global_counter, rgi_queue, rgo_queue
    try:
        in_request = request.json
        print(in_request)
    except:
        return "invalid input: "
    global_counter += 1
    rgi_queue.put((global_counter, in_request))
    output = rgo_queue.get()
    rgo_queue.task_done()
    return jsonify(output)

def generate_for_queue(in_queue, out_queue):
    memory = []
    while True:
        _, in_request = in_queue.get()
        obs = in_request['msg']
        print("now predicting...")
        response, belief_states = predictor(obs)    #We only use BS from here: change to _, belief_states
 
        if belief_states != {}:
            t = []
            for s,v in belief_states.items():
                t.append(f'{s} = {v}')
            memory.append(' ; '.join(t))
        print("memory", memory)

        options, rows = query_from_db(beliefstate=memory[-1])

        db_state = f"database {options} results "
        #response, _ = predictor(obs, memory[-1] + "<EOB> ", db_state)
        

        followup = fill_delex(response, rows)
        print(followup)

        res = {}
        res['response'] = response
        res['memory'] = memory
        res['followup'] = followup
        out_queue.put(res)
        in_queue.task_done()

def fill_delex(pattern:str, rows: list):

    # if no results, but pattern has delex slot, append fail message
    if  len(rows) == 0:
        if "[" in pattern:
            return "I couldn't find anything matching your query. Would you like to try again?" # pattern + "nores" * int("[" in pattern)
        else:
            return pattern

    fill_dict = rows[0] # {key: value for key, value in rows[0].items()} what was i smoking there
    #slot_dict
    slots_to_fill = re.findall(r"\[(\S+)\]", pattern)
    if "name1" in pattern:
        fill_dict["name1"] = rows[0]["name"]
        fill_dict["name2"] = rows[1]["name"]
    # if "area" in pattern:
    #     pass # might not need that
    # TODO maybe sometimes alias
    for delex in slots_to_fill:
        try:
            pattern = pattern.replace("["+ delex + "]", str(fill_dict[delex]))
        except KeyError:
            print(f"slot {delex} couldn't be filled")
    return pattern


# if __name__ == "__main__":
#     # from soloist.server import *
#     args.model_name_or_path = '/mount/studenten-temp1/users/zabereus/adviser/soloist_env/soloist/examples/college_bot/college_model'
#     main()

#     predictor(["What is the admission rate at Harvard"])
#     print("-------------------")
#     predictor(["I'm looking for expensive colleges in New England", "What would you like to study there?", "physics"])    
#     print("-------------------")
#     predictor(["show me affordable colleges", "Where would you like to study?", "Texas"])


#     worker = Thread(target=generate_for_queue, args=(rgi_queue, rgo_queue,))
#     worker.setDaemon(True)
#     worker.start()

#     # rgi_queue.put((2, {'msg': ["how expensive is it to study there?"]}))
#     rgi_queue.put((2, {'msg': ["how expensive is it to study there?","where do you want your college to be?","in new england"]}))
#     print("-------------------")
#     #rgi_queue.put((2, {'msg': ["What is the admission rate at Harvard"]}))

#     app.run(host='0.0.0.0',port=8081)