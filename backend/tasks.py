from store_data import load_tasks,save_task
import uuid

def get_user_tasks(username:str):
    data=load_tasks()
    return data.get(username, [])
    
def add_task(username:str,task:str):
    data=load_tasks()
    user_tasks=data.get(username,[])
    task_id=uuid.uuid4().int >> 64
    user_tasks.append({"id":task_id,"task":task})
    data[username]=user_tasks
    save_task(data)
    return task_id

def delete_tasks(username:str,task_id:int):
    data=load_tasks()
    user_tasks=data.get(username,[])
    print("Debug user_tasks:..........",user_tasks)
    user_tasks=[i for i in user_tasks if i["id"] != task_id]
    # for i in user_tasks:
    #     if i["id"] != task_id:
    #         break
            # del user_tasks[i]
    data[username] = user_tasks 
    save_task(data)
    return {"Success": True,"Message":"Task record deleted successfully"}
    # return {"Success":False,"Message":"Task Not Found"}       