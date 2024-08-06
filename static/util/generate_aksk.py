import random
import string


def generate_aksk():
    access_key_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    secret_access_key = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    return access_key_id, secret_access_key


access_key, secret_access = generate_aksk()
print("AccessKey ID:", access_key)
print("Secret Access Key:", secret_access)
