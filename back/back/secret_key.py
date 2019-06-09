from django.core.management.utils import get_random_secret_key

def get():
    try:
        with open('./secretkey.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        key = get_random_secret_key()
        with open('./secretkey.txt', 'w') as f:
            f.write(key)
        return key
