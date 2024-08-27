import json
import re

def load_training_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_response(user_query, training_data):
    user_query = user_query.lower()
    best_match = None
    highest_score = 0

    for intent in training_data["intents"]:
        for pattern in intent["patterns"]:
            pattern_re = re.compile(re.escape(pattern.lower()), re.IGNORECASE)
            if pattern_re.search(user_query):
                score = len(pattern)
                if score > highest_score:
                    highest_score = score
                    best_match = intent["responses"]

    if best_match:
        return best_match[0]
    else:
        return "Sorry, I can't answer that."
