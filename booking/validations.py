import re
from django.core.validators import validate_email

def validation_form(phone_number, email):

    validation_message = ''
    
    if not re.match(r"^\+?\d{7,15}$", phone_number):
        validation_message += "- Invalid phone number. Use only digits or the prejix '+' opcional\n"
    
    try:
        validate_email(email)
    except:
        validation_message += "- Invalid email\n"
    
    return validation_message