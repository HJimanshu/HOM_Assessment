
import json
import os
# store the specific tasks in file
Storage_path="storage.json"

def load_tasks():
    if not os.path.exists(Storage_path):
        return {}
    if not os.path.getsize(Storage_path) == 0:
        return {}
        
    with open(Storage_path,"r")as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
    
def save_task(data):
    with open(Storage_path,"w") as f:
        json.dump(data,f)