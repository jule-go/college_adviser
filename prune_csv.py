import csv

region_dict = {"1": "New England", "2": "Mid East", "3": "Great Lakes", "4": "Plains", "5": "Southeast", 
               "6": "Southwest", "7": "Rocky Mountains", "8": "Far West"}

# curtesy of chatgpt
state_dict = {'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'DC': 'Washington, DC',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}

"""
Prunes a csv table of colleges: No study areas, combines NPT costs, excludes NULL SAT scores, prunes by student number
"""
def prune():
    out_file = open("pruned_dataset.csv", "w")
    with open("full_dataset.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        writer = csv.writer(out_file, delimiter=',', quotechar='"', lineterminator="\n")
        for row in reader:
            if not ("PrivacySuppressed" in row[18] or "NULL" in row[:13] + row [15:]):
                if row[12] == "UGDS" or int(row[12])>5000:
                    x = row[13] if row[13] != "NULL" else row[14]
                    row = row[:13] + [x] + row[15:]
                    writer.writerow(row)

"""
Prunes a csv table of colleges: Includes study areas, combines NPT costs, allows NULL SAT scores, prunes by student number and income
"""
def prune2():
    out_file = open("pruned_dataset_working", "w")
    with open("full_dataset_working.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        writer = csv.writer(out_file, delimiter=',', quotechar='"', lineterminator="\n")
        for row in reader:
            if row[0] == "UNITID":
                #print(row[12], row[13], row[14], row[15])
                row = row[:13] + ["COST"] + row[15:]
                writer.writerow(row)
            elif not ("PrivacySuppressed" in row[18] or "NULL" in row[:11] + row[12:13] + row [15:]):   # currently allowing NULL SAT scores
                if int(row[12]) > 4500 and int(row[57]) > 15 and int(row[15]) > 70000:                  #maybe prune at 60k
                    x = row[13] if row[13] != "NULL" else row[14]
                    row = row[:13] + [x] + row[15:]
                    writer.writerow(row)

"""
Prunes a csv table of colleges: Includes study areas, combines NPT costs, allows NULL SAT scores, 
prunes by student number, bachelor areas covered and income.
Designed for reordered and reduced dataset, includes binarization of CIP values
"""
def prune3():
    out_file = open("pruned_dataset_xxx.csv", "w")
    with open("full_dataset_working.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        writer = csv.writer(out_file, delimiter=',', quotechar='"', lineterminator="\n")
        header = next(reader)
        ix = {heading: i for i, heading in enumerate(header)}
        print(ix)
        header = header[:12] + ["NET_COST"] + header[14:]
        writer.writerow(header)
        for row in reader:
            if not ("PrivacySuppressed" in row[ix['DEBT_MDN']] or "NULL" in row[3:10] + row[11:12] + row [14:36]):   
                if int(row[ix['NUM_UGDS']]) > 4500 and int(row[ix['SUM']]) > 15 and int(row[ix['EARNINGS_MDN']]) > 70000:
                    x = row[ix['NPT4_PUB']] if row[ix['NPT4_PUB']] != "NULL" else row[ix['NPT4_PRIV']]
                    binaries = [int(bool(int(val))) for val in row[17:ix["SUM"]]]  # some have values > 1, these are mapped to 1 --> binarization
                    row = row[:12] + [x] + row[14:17] + binaries + [row[ix['SUM']]]
                    writer.writerow(row)


"""
Prunes a csv table of colleges: Includes study areas, allows NULL SAT scores, 
prunes by student number, bachelor areas covered and income.
Designed for reordered and reduced dataset, includes binarization of CIP values.
Doesn't include net costs, does include cost bins of total cost
"""
def prune4():
    out_file = open("pruned_dataset_xxx.csv", "w")
    with open("full_dataset_working.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        writer = csv.writer(out_file, delimiter=',', quotechar='"', lineterminator="\n")
        header = next(reader)
        ix = {heading: i for i, heading in enumerate(header)}
        print(ix)
        header = header[:12] + ["PRICE_RANGE"] + header[14:]
        writer.writerow(header)
        for row in reader:
            if not ("PrivacySuppressed" in row[ix['DEBT_MDN']] or "NULL" in row[3:10] + row[11:12] + row [14:36]):   
                if int(row[ix['NUM_UGDS']]) > 4500 and int(row[ix['SUM']]) > 15 and int(row[ix['EARNINGS_MDN']]) > 70000:
                    binaries = [int(bool(int(val))) for val in row[17:ix["SUM"]]]  # some have values > 1, these are mapped to 1 --> binarization
                    cost = int(row[ix["COSTT4_A"]])
                    # puts price into one of four bins (I hate the way I implemented it, but hey, one line!)
                    price_range = ["affordable", "pricey", "expensive", "very expensive"][sum([cost>55000, cost>70000, cost>76000])]
                    row = row[:12] + [price_range] + row[14:17] + binaries + [row[ix['SUM']]]
                    writer.writerow(row)

def get_all_cip():
    out_file = open("full_CIP.csv", "w")
    with open("full_CIP_old.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        writer = csv.writer(out_file, delimiter=',', quotechar='"', lineterminator="\n")
        bachl_list = []
        for row in reader:
            # Go through first row, check which CIP are Bachelor, all others are not transferred
            if row[0] == "CIP01BACHL":
                for i in range(len(row)):
                    if "BACHL" in row[i]:
                        print("added", i)
                        bachl_list.append(i)
                row = [row[i] for i in bachl_list] + ["SUM"]
                writer.writerow(row)
            else:
                try: 
                    cip_sum = sum([bool(int(row[i])) for i in bachl_list])
                except ValueError:
                    cip_sum = 0
                row = [row[i] for i in bachl_list] + [cip_sum]    
                writer.writerow(row)
    print(len(bachl_list))

"""
Refines a pruned csv table of colleges with final columns done:
- rounds numbers for students, cost, debt, earnings, admission rate, completion rate (the latter 2 are now percentages)
- writes out states, regions, and control ("public"/"private")
"""
def get_v3():
    out_file = open("pruned_dataset_final_v3.csv", "w")
    with open("pruned_dataset_final_v2.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        writer = csv.writer(out_file, delimiter=',', quotechar='"', lineterminator="\n")
        header = next(reader)
        ix = {heading: i for i, heading in enumerate(header)}
        print(ix)
        writer.writerow(header)
        for row in reader:
            row[ix["CONTROL"]] = "private" if int(row[ix["CONTROL"]]) > 1 else "public"
            row[ix["REGION"]] = region_dict[row[ix["REGION"]]]
            row[ix["STATE"]] = state_dict[row[ix["STATE"]]]
            
            row[ix["NUM_UGDS"]] = str(round(int(row[ix["NUM_UGDS"]]), -2))
            row[ix["ADM_RATE"]] = str(round(100 * float(row[ix["ADM_RATE"]]), 1)) + '%'

            compl_rate = float(row[ix["COMPL_RATE"]])  #some are not percentages, but #/1000 oder so
            if compl_rate > 1: compl_rate /= 1000
            row[ix["COMPL_RATE"]] = str(round(100 *compl_rate, 1)) + '%' 

            row[ix["COSTT4_A"]] = str(round(int(row[ix["COSTT4_A"]]), -2))
            row[ix["DEBT_MDN"]] = str(round(int(row[ix["DEBT_MDN"]]), -3))
            row[ix["EARNINGS_MDN"]] = str(round(int(row[ix["EARNINGS_MDN"]]), -3))
            writer.writerow(row)

get_v3()