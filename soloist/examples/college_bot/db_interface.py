""" Interaction with our database: Converts a bs into an SQL query and gets all relevant rows """
import sqlite3, re
from contextlib import closing

column_dict = {"id": "UNITID", "name": "NAME", "alias": "ALIAS", "city": "CITY", "state": "STATE", "region":"REGION", "url": "URL", "control":"CONTROL" ,
"students": "NUM_UGDS", "admission_rate":"ADM_RATE", "sat": "SAT_AVG", "cost": "COSTT4_A", 	"price_range": "PRICE_RANGE", "earnings":"EARNINGS_MDN", "debt":"DEBT_MDN", "completion": "COMPL_RATE",
"architecture": "CIP04BACHL", "journalism": "CIP09BACHL", "computer science": "CIP11BACHL", "education": "CIP13BACHL", "engineering": "CIP14BACHL", "linguistics": "CIP16BACHL", "law": "CIP22BACHL", 
"literature": "CIP23BACHL", "biology": "CIP26BACHL", "mathematics": "CIP27BACHL", "philosophy": "CIP38BACHL", "physics": "CIP40BACHL", "psychology": "CIP42BACHL", "social science": "CIP45BACHL", 	
"arts": "CIP50BACHL", "health": "CIP51BACHL", "business": "CIP52BACHL", "history": "CIP54BACHL", "areas": "SUM"}
#column_to_name = {value: key for key, value in column_dict.items}
slots = list(column_dict.keys())

# BS looks like
#"belief": "belief : cuisine = German ; object_type = restaurant"

def query_from_db(beliefstate: str):
    """ 
    Converts a bs into an SQL query and returns the number of results and the relevant rows.
    Contains some functionality and error handling to account for weaknesses of the model
    """
    with closing(sqlite3.connect("/mount/studenten-temp1/users/zabereus/adviser/soloist_env/soloist/examples/college_bot/pruned_v4.db")) as connection:
        cursor = connection.cursor()

        query = "SELECT * FROM pruned_v4 WHERE "
        query_conditions = []
        beliefstate = beliefstate.lower()
        for condition in beliefstate.split(";"):#.split(":")[1]
            condition = condition.strip()
            key, sign, value = re.fullmatch(f"(\S+) ([<>=]) (.+)", condition).group(1,2,3)
            #print(key, sign, value)
            if key not in column_dict and key not in ["area"]:
                print(f"{key} is not a valid slot")
                continue

            assert sign in "<>="

            # converting "area = architecture" to "architecture = 1"
            if key == "area":
                key = value
                value = 1
            # allowing for aliases
            if key == "name":
                query_conditions.append(f"(NAME LIKE '%{value}%' OR ALIAS LIKE '%{value}%')")
            elif key == "state" or key == "region" or key == "city":
                query_conditions.append(f"(STATE = '{value}' OR REGION = '{value}' OR CITY = '{value}')")
            elif key == "options":
                pass
            else:
                try:
                    query_conditions.append("{}{}'{}'".format(column_dict[key], sign, value))
                except KeyError:
                    print("!")
                    return 0, []

        query += " AND ".join(query_conditions)
        #print(query)
        if not query_conditions:
            query += " 1 = 1 "
        rows = cursor.execute(query).fetchall()

        # convert db rows to dicts
        row_dicts = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                row_dict[slots[i]] = value
            row_dicts.append(row_dict)
        print(len(row_dicts))
        #print(row_dicts)
        options = len(rows)
        return options, row_dicts

# def request_from_db(beliefstate: dict):
#     with closing(sqlite3.connect("pruned_v2.db")) as connection:
#         cursor = connection.cursor()

#         query = "SELECT name FROM pruned_v2 WHERE 1=1"
#         for key, value in beliefstate["requests"].items():
#             #TODO
#             pass

#         rows = cursor.execute(query).fetchall()
#         options = len(rows)
#         db_state = []
#         return db_state

#query_from_db("belief : region = CA ; debt < 13000; area = engineering")