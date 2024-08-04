import subprocess
import threading
import argparse

parser = argparse.ArgumentParser(
                    prog='Hash Cracker',
                    description='Cracks a UNIX hash',
                    epilog='')

parser.add_argument('-w', '--wordlist', help='Wordlist to use', required=True)
args = parser.parse_args()

print("Make sure to modify the hash in the source code.")
# Target hash to crack
# CHANGEME
target_hash = "$6$xgLS35S6$2UjEq.dUhICPw9zgDVJXcQYQp/9ilLPQt/8Zgu0uwngI5mVvB1eKQG9SnVLjmOOfkB4Jjb5VSAXGXjY4Cf5k90"



try:
    hash_id, salt, hashed_password = target_hash.split('$')[1:]
except ValueError:
    print("Invalid hash format. Expected format: $id$salt$hashed")
    exit(1)


# Shared variable to indicate if the hash has been cracked
hash_cracked = False
hash_lock = threading.Lock()

# Number of threads
num_threads = 15

# Wordlist file path
wordlist_file = args.wordlist



# Function to crack the hash
def crack_hash(wordlist, thread_num):
    global hash_cracked
    try:
        with open(wordlist, "r") as f:
            lines = f.readlines()
            # Divide the wordlist between threads
            chunk_size = len(lines) // num_threads
            start = thread_num * chunk_size
            end = (thread_num + 1) * chunk_size if thread_num < num_threads - 1 else len(lines)
            for word in lines[start:end]:
                word = word.strip()
                # Hash word using openssl utility in os
                hashed_word = subprocess.check_output(['openssl', 'passwd', f'-{hash_id}', '-salt', 'xgLS35S6', '-stdin'], input=word.encode()).decode().strip()
                with hash_lock:
                    if hashed_word == target_hash:
                        print("Hash cracked! The original word is:", word)
                        hash_cracked = True
                        # Stop if hash has been cracked
                        return
                    if hash_cracked:
                        return
    except Exception as e:
        print("An error occurred in thread", thread_num, ":", e)


# Create and start threads
print(f"Cracking hash {target_hash}")
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=crack_hash, args=(wordlist_file, i))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()