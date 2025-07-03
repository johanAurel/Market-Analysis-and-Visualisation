#API_KEY
API_KEY = '92b864d1bb3825478403dfb9173bceff-88ca6df194c96c38efaaab97fa06c9d8'
USER_ID = '101-004-31388639-001'

def set_user_id(user_id=None):
    global USER_ID
    if user_id is not None:  # If a new user ID is provided
        USER_ID = user_id  
     # Update the global USER_ID
    return USER_ID  # Return the current USER_ID

