import hashlib
import pyfiglet
import string
import random
import time
import psutil
import os

# Start timer for execution
execution_start_time = time.time()

def show_logo():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("""

       ______        __ __ _        _                ______ _             __
      / ____/____   / // /(_)_____ (_)____   ____   / ____/(_)____   ____/ /___   _____
     / /    / __ \ / // // // ___// // __ \ / __ \ / /_   / // __ \ / __  // _ \ / ___/
    / /___ / /_/ // // // /(__  )/ // /_/ // / / // __/  / // / / // /_/ //  __// /
    \____/ \____//_//_//_//____//_/ \____//_/ /_//_/    /_//_/ /_/ \__,_/ \___//_/

          """)


    print("""

    ****************************************
    *                                      *
    *      MD5 COLLISION FINDER MENU       *
    *      Created by danielvilaca         *
    *                                      *
    ****************************************

          """)


def display_menu():
    print("\n Please select an option:")
    print("1. Find Random MD5 Collisions")
    print("2. Find Specific MD5 Collisions")
    print("3. Exit")

def get_user_choice():
    try:
        choice = int(input("Enter your choice: "))
        return choice
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        return None

def get_user_input_for_random():
    """
    Get input parameters for the random collision finder.
    """
    print("Please enter the following parameters (leave them blank to use defaults):")

    string_length = input(f"String length for random generation (default: 8): ")
    string_length = int(string_length) if string_length else 10

    hash_length = input(f"Hash length to analyze for collision (default: 16) : ")
    hash_length = int(hash_length) if hash_length else 8

    max_ram_usage = input(f"Max RAM usage before auto stop (default: 50%): ")
    max_ram_usage = int(max_ram_usage) if max_ram_usage else 50

    max_collisions = input(f"Number of collisions to find before stopping: ")
    max_collisions = int(max_collisions) if max_collisions else 3

    print("\n")
    print("*************************************************************************")
    print(f"\nParameters: \n -String length for random generation: {string_length}"
          f"\n-Hash length to analyze for collision: {hash_length}"
          f"\n-Max RAM usage before auto stop: {max_ram_usage}%"
          f"\n-The program will find {max_collisions} collisions before stopping"
          f"\n-Progress updates every 10,000 tests \t \t \t \t \t \t")
    print("\n*************************************************************************")


    return string_length, hash_length, max_ram_usage, max_collisions

def get_user_input_for_specific():
    """
    Get input parameters for the specific collision finder.
    """
    # Step 1: Ask for the specific string
    user_string = input("Please enter the string to search for MD5 collisions: ")

    # Step 2: Automatically set the hash length to 8 (or another default)
    hash_length = 8  # Default hash length for MD5 collision search

    max_ram_usage = input(f"Max RAM usage before auto stop (default: 50%): ")
    max_ram_usage = int(max_ram_usage) if max_ram_usage else 50

    max_collisions = input(f"Number of collisions to find before stopping (default: 3): ")
    max_collisions = int(max_collisions) if max_collisions else 3

    # print(f"\n Parameters: \n -Searching for collisions with string: {user_string} \n"
    #       f" -Hash length to analyze for collision: {hash_length} \n"
    #       f" -Max RAM usage before auto stop: {max_ram_usage}% \n"
    #       f" -The program will find {max_collisions} collisions before stopping \n")

    return user_string, hash_length, max_ram_usage, max_collisions

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_random_string(length=17, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(length))

def compute_hash(input_string, length=8):
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    return md5_hash[:length]

def check_for_collision(hash_value, string_value, hashmap):
    if hash_value in hashmap and hashmap[hash_value] != string_value:
        global collision_count, collision_details
        collision_details[hash_value] = hashmap[hash_value]
        print(f"***** COLLISION FOUND *****")
        print(f"Hash 1: {hash_value} with value: {string_value}")
        print(f"Hash 2: {hash_value} with value: {hashmap[hash_value]}")
        print(f"Using {hash_length} characters long hash in {time.time() - execution_start_time} seconds")
        print("************************* \n")
        collision_count += 1
        return True
    else:
        hashmap[hash_value] = string_value
        return False

def track_memory_usage():
    return psutil.virtual_memory().percent

def run_random_collision_detection(string_length, hash_length, max_ram_usage, max_collisions):
    global collision_count, hashmap, collision_details
    collision_count = 0
    hashmap = {}
    collision_details = {}

    test_counter = 0
    while collision_count < max_collisions:
        test_counter += 1
        ram_usage = track_memory_usage()

        # Periodic progress update
        if test_counter % 10000 == 0:
            print(f"Progress Update: {test_counter} tests completed")
            print(f"Elapsed Time: {time.time() - execution_start_time} seconds")
            print(f"RAM usage: {ram_usage}%")
            print(f"Collisions found: {collision_count}")
            print(f"Current hashmap size: {len(hashmap)}\n")

        # Generate random strings and compute their hashes
        string_a = generate_random_string(string_length)
        string_b = generate_random_string(string_length)
        hash_a = compute_hash(string_a, hash_length)
        hash_b = compute_hash(string_b, hash_length)

        # Check for collisions
        if check_for_collision(hash_a, string_a, hashmap) or check_for_collision(hash_b, string_b, hashmap):
            collision_count += 1

        # Stop if RAM usage exceeds the limit
        if ram_usage > max_ram_usage:
            print("Stopping. Excessive RAM usage detected.")
            break

def run_specific_collision_detection(user_string, hash_length, max_ram_usage, max_collisions):
    global collision_count, hashmap, collision_details
    collision_count = 0
    hashmap = {}
    collision_details = {}

    user_hash = compute_hash(user_string, hash_length)

    print(f"Searching for collisions with hash: {user_hash}")

    test_counter = 0
    while collision_count < max_collisions:
        test_counter += 1
        ram_usage = track_memory_usage()

        # Simplified progress update
        if test_counter % 10000 == 0:
            print("====================================================================")
            print("\n")
            print(f"Progress Update: {test_counter} tests completed")
            print(f"Elapsed Time: {time.time() - execution_start_time} seconds")
            print(f"RAM usage: {ram_usage}% \n")

        # Generate random strings and compute their hashes
        string_a = generate_random_string()  # You can generate random strings of default length here
        hash_a = compute_hash(string_a, hash_length)

        # Check if this hash matches the user-specified hash
        if hash_a == user_hash:
            collision_count += 1
            print(f"***** COLLISION FOUND *****")
            print(f"String: {string_a} produces hash: {hash_a}")
            print("************************* \n")

        # Stop if RAM usage exceeds the limit
        if ram_usage > max_ram_usage:
            print("Stopping. Excessive RAM usage detected.")
            break


# Execution starts here
show_logo()

while True:
    display_menu()
    choice = get_user_choice()

    if choice == 1:
        print("\n")
        print("====================================================================")
        print("\n")
        string_length, hash_length, max_ram_usage, max_collisions = get_user_input_for_random()  # Use the random collision input function
        print("Running Random MD5 Collision Finder...\n")
        run_random_collision_detection(string_length, hash_length, max_ram_usage, max_collisions)
        break
    elif choice == 2:
        print("\n")
        print("====================================================================")
        print("\n")
        user_string, hash_length, max_ram_usage, max_collisions = get_user_input_for_specific()  # Use the specific collision input function
        print("Running Specific MD5 Collision Finder...\n")
        run_specific_collision_detection(user_string, hash_length, max_ram_usage, max_collisions)
        break
    elif choice == 3:
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please choose between 1, 2, or 3.")
