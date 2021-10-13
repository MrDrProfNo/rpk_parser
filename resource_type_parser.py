import json
""" 
Print names of all resource types 

@author Moonshine, MrNo
"""
with open('type_ids.json') as f:
    r = json.load(f)
    for item in r:
        hex_string = " ".join([f"{byte:02x}" for byte in bytes.fromhex(item[1][2:])])
        if hex_string[-5:] != "44 47":
            print("(incorrect?)", end=" ")
        print(item[0], ":", hex_string)
