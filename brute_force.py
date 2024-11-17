import hashlib
import requests

# URLs of password files in order of priority
password_file_urls = [
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/2020-200_most_used_passwords.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/2023-200_most_used_passwords.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/500-worst-passwords.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10k-most-common.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10-million-password-list-top-1000000.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Honeypot-Captures/multiplesources-passwords-fabian-fingerle.de.txt"
]

def read_hash():
    """Read the stored MD5 hash from machine_passwd file"""
    try:
        with open('./machine_passwd', 'r') as f:
            return f.read(32)  # Read the first 32 characters (length of an MD5 hash)
    except FileNotFoundError:
        print("Error: machine_passwd file not found")
        exit(1)

def get_wordlist(url):
    """Fetch the wordlist from GitHub"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching wordlist from {url}: {e}")
        return []

def md5_hash(word):
    """Return the MD5 hash of the given word"""
    return hashlib.md5(word.encode('utf-8')).hexdigest()

def find_password(machine_passwd):
    """Attempt to find the password by comparing MD5 hashes"""
    for url in password_file_urls:
        print(f"Fetching and searching in {url}...")
        wordlist = get_wordlist(url)
        for word in wordlist:
            if md5_hash(word) == machine_passwd:
                print(f"Password found: {word}")
                return
    print("Password not found in the provided wordlists.")

if __name__ == '__main__':
    # Read the stored hash
    machine_passwd = read_hash()
    # Start the password search
    find_password(machine_passwd)
