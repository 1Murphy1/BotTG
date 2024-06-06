import os

def log_message(user_id, message):
    log_file = f"{user_id}.log"
    with open(log_file, 'a', encoding='utf-8') as file:
        file.write(message + '\n')
