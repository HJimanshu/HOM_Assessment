import uuid

# This file module i am used for in memory user store and token store

token_store={}
token_list=set()

# generate the token if user are authenticated
def generate_token(username:str):
    token=str(uuid.uuid4())
    token_store[token]=username
   
    return token

#verify the token after getting username from token.
def get_username_from_token(token:str):
    
    return token_store.get(token)

def invalidate_token(token:str):
    token_list.add(token)

    token_store.pop(token,None)
