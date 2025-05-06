from fastapi import FastAPI,Request,HTTPException,Depends,Header
from pydantic import BaseModel
from tasks import get_user_tasks,add_task,delete_tasks
from token_store import generate_token,get_username_from_token,invalidate_token
app=FastAPI()

#---Models here----
class User(BaseModel):
    username:str
    password:str

class TaskInput(BaseModel):
    task:str


# This file module i am used for in memory user store and tk store
users={}
#register the user
def register_user(username:str,password:str):
    if username in users:
        return False
    users[username]= password
    return True
# Authenticate the user
def authenticate_user(username: str, password:str):
    return users.get(username)==password    
    
#---------------Get current user  -------------
def get_user(token:str = Header(default=None)):
    username=get_username_from_token(token)
    if not username:
        raise HTTPException(status_code=401,detail="Invalid and missing token")
    return username


#----Create a routes endpoints ----------

@app.post("/register")
def register(user:User):
    if not register_user(user.username,user.password):
        raise HTTPException(status_code=400,detail="User Allready exists")
    return {"Message":"User Registered"}

@app.post("/login")
def login(user:User):
    if not authenticate_user(user.username,user.password):
        raise HTTPException(status_code=400,detail="User not exist")
    token=generate_token(user.username)
    print("You can get token from here",token)
    return {"Message":"User Login Successfully","Token":token}

@app.post("/create_tasks")
def create_task(task:TaskInput,username:str=Depends(get_user)):
    task_id=add_task(username,task.task)
    return {"Message":"Task Added","Id":task_id}

@app.get("/tasks")
def view_tasks(username:str=Depends(get_user)):
    return {"Tasks":get_user_tasks(username)}



@app.delete("/tasks_delete/{task_id}")
def delete_task(task_id:int,username:str=Depends(get_user)):
    delete_tasks(username,task_id)
    return {"Message":"Task Deleted Successfully"}

@app.post("/logout")
def logout(token:str = Header(default=None)):
    if not token:
        raise HTTPException(status_code=400,detail="token missing")
    invalidate_token(token)
    return {"Message":"Logout Successfully"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port= 8800)