# Hash Cracker
## Description

Hash Cracker is a Python script designed to crack UNIX hashes using a wordlist. The script utilizes multithreading to efficiently test multiple password candidates against a target hash defined within the source code.

## Usage

Clone the script
```
git clone https://github.com/Shad0wMazt3r/hash-cracker

cd hash-cracker
```

Add the hash you want to crack by modifying the following line:
```
target_hash = "$6$xgLS35S6$2UjEq.dUhICPw9zgDVJXcQYQp/9ilLPQt/8Zgu0uwngI5mVvB1eKQG9SnVLjmOOfkB4Jjb5VSAXGXjY4Cf5k90"
```
Install the requirements
```
pip install -r requirements.txt
```
Run the script
```
python hash_cracker.py -w <wordlist-name>
```
A wordlist is already included.

## Important Note

Make sure to modify the target hash in the source code. Look for the line with # CHANGEME and change the target_hash variable to the hash you want to crack.

This script requires openssl to be installed


## How It Works

The script reads the target hash components from the target_hash variable.

It then reads the wordlist file specified by the user.

The wordlist is divided into chunks, and each chunk is processed by a separate thread.

Each thread hashes words from its chunk using OpenSSL and compares the generated hash with the target hash.

If a match is found, the original word is printed, and all threads stop processing.