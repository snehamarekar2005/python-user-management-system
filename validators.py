import re

def validate_username(username):
    
    if len(username) < 5:
        return False, "⚠️ Username kam se kam 5 characters ka hona chahiye."
    return True, ""


def validate_password_strength(password):
    
    if len(password) < 8:
        return False, "⚠️ Password kam se kam 8 characters ka hona chahiye."
    if not re.search(r"[A-Z]", password):
        return False, "⚠️ Password mein kam se kam ek uppercase letter hona chahiye."
    if not re.search(r"[a-z]", password):
        return False, "⚠️ Password mein kam se kam ek lowercase letter hona chahiye."
    if not re.search(r"[0-9]", password):
        return False, "⚠️ Password mein kam se kam ek digit hona chahiye."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        return False, "⚠️ Password mein kam se kam ek special character hona chahiye (!@#$% etc)."
    return True, ""


def validate_passwords_match(password, confirm_password):
    if password != confirm_password:
        return False, "⚠️ Passwords match nahi kar rahe."
    return True, ""
