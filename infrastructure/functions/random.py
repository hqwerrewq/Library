import random
import string

def random_id_generator(length=8):
    while True:
        yield ''.join(random.choices(string.ascii_letters + string.digits, k=length))