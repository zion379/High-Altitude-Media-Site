from werkzeug.security import generate_password_hash

def gen_pass_hash(password):
    hashed_password = generate_password_hash(password, method='scrypt')
    print(f'Generated hash for the given password {password}. Hash : "{hashed_password}" ')
    