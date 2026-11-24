import random
import string
import json
import os

def validate_length(length: int) -> bool:
    """Checks if the length is within the valid range [4, 32]."""
    return 4 <= length <= 32

def check_options_count(checked_count: int) -> bool:
    """
    Checks if at least 2 options are selected from the optional categories.
    According to the spec: 'Uppercase, Number, Special Char' must have 2 or more checked.
    """
    return checked_count >= 2

def generate_password(length: int, use_upper: bool, use_number: bool, use_special: bool) -> str:
    """
    Generates a password of the given length.
    Lowercase is always included.
    Ensures at least one character from each selected category is present.
    """
    if length < 1:
        return ""

    lowercase = string.ascii_lowercase
    pool = lowercase
    selected_chars = []
    
    # Always include one lowercase
    selected_chars.append(random.choice(lowercase))

    if use_upper:
        upper = string.ascii_uppercase
        pool += upper
        selected_chars.append(random.choice(upper))
    
    if use_number:
        numbers = string.digits
        pool += numbers
        selected_chars.append(random.choice(numbers))
        
    if use_special:
        special = "!@#$%^&*"
        pool += special
        selected_chars.append(random.choice(special))

    # If length is smaller than the mandatory chars we just added, 
    # we need to adjust.
    if len(selected_chars) > length:
        selected_chars = selected_chars[:length]
    else:
        # Fill the rest of the password length
        remaining_length = length - len(selected_chars)
        for _ in range(remaining_length):
            selected_chars.append(random.choice(pool))
    
    # Shuffle to ensure randomness
    random.shuffle(selected_chars)
    return "".join(selected_chars)

def save_password_to_json(file_path: str, site_name: str, password: str) -> bool:
    """Saves the site name and password to a JSON file."""
    data = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    data = json.loads(content)
        except (json.JSONDecodeError, IOError):
            data = []
    
    data.append({"site": site_name, "password": password})
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except IOError:
        return False

def load_passwords_from_json(file_path: str) -> list:
    """Loads passwords from a JSON file."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []
