import sqlite3
from contextlib import closing

column_dict = {"cost": "COSTT4_A", "price_range": "PRICE_RANGE", "state": "STATE"}

# how does the BS look like?
# is it "belief": "ds : cuisine = German ; object_type = restaurant" ?

def query_from_db(beliefstate: dict):
    connection = sqlite3.connect("pruned_v2.db")
    cursor = connection.cursor()

    query = "SELECT name FROM pruned_v2 WHERE 1=1"
    for key, value in beliefstate["informs"].items():
        query += "AND {}={}".format(column_dict[key], value)

    rows = cursor.execute(query).fetchall()
    options = len(rows)
    db_state = []
    return db_state

def query_from_db(beliefstate: str):
    with closing(sqlite3.connect("pruned_v2.db")) as connection:
        cursor = connection.cursor()

        query = "SELECT name FROM pruned_v2 WHERE 1=1"
        for condition in beliefstate.split(":")[1].split(";"):
            condition = condition.strip()
            key, value = condition.split(" = ")
            query += " AND {}='{}'".format(column_dict[key], value)
        print(query)
        rows = cursor.execute(query).fetchall()
        print(rows)
        options = len(rows)
        db_state = [options, rows] # maybe a dict here, maybe just names
        return db_state

def request_from_db(beliefstate: dict):
    with closing(sqlite3.connect("pruned_v2.db")) as connection:
        cursor = connection.cursor()

        query = "SELECT name FROM pruned_v2 WHERE 1=1"
        for key, value in beliefstate["requests"].items():
            #TODO
            pass

        rows = cursor.execute(query).fetchall()
        options = len(rows)
        db_state = []
        return db_state

query_from_db("ds : price_range = expensive ; state = CA")