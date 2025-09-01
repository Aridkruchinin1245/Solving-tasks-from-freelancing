import random
import string

def createPromo():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

