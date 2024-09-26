#API_KEY
API_KEY = 'bb1d421d5ff8b46afc88b98ea098fb16-6366a971f49832b64f2992233bb88b6b'
USER_ID = '101-004-21322380-001'

def set_user_id(user_id=None):
    global USER_ID
    if user_id is not None:  # If a new user ID is provided
        USER_ID = user_id  
     # Update the global USER_ID
    return USER_ID  # Return the current USER_ID

