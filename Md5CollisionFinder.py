import hashlib
import pyfiglet
import string
import random
import time
import psutil
import os

# Start timer for execution
program_start_time = time.time()

def display_header():
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


def print_menu():
    print("\n Please select an option:")
    print("1. Find Random MD5 Collisions")
    print("2. Find Specific MD5 Collisions")
    print("3. Exit")

def get_menu_choice():
    try:
        menu_choice = int(input("Enter your choice: "))
        return menu_choice
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        return None

def get_random_collision_parameters():
    """
    Get input parameters for the random collision finder.
    """
    print("Please enter the following parameters (leave them blank to use defaults):")

    generated_string_length = input(f"String length for random generation (default: 8): ")
    generated_string_length = int(generated_string_length) if generated_string_length else 10

    hash_chars_to_check = input(f"Hash length to analyze for collision (default: 16): ")
    hash_chars_to_check = int(hash_chars_to_check) if hash_chars_to_check else 8

    memory_limit_percent = input(f"Max RAM usage before auto stop (default: 50%): ")
    memory_limit_percent = int(memory_limit_percent) if memory_limit_percent else 50

    target_collision_count = input(f"Number of collisions to find before stopping: ")
    target_collision_count = int(target_collision_count) if target_collision_count else 3

    print("\n")
    print("*************************************************************************")
    print(f"\nParameters: \n -String length for random generation: {generated_string_length}"
          f"\n-Hash length to analyze for collision: {hash_chars_to_check}"
          f"\n-Max RAM usage before auto stop: {memory_limit_percent}%"
          f"\n-The program will find {target_collision_count} collisions before stopping"
          f"\n-Progress updates every 10,000 tests \t \t \t \t \t \t")
    print("\n*************************************************************************")


    return generated_string_length, hash_chars_to_check, memory_limit_percent, target_collision_count

def get_specific_collision_parameters():
    """
    Get input parameters for the specific collision finder.
    """
    # Step 1: Ask for the specific string
    target_string = input("Please enter the string to search for MD5 collisions: ")

    # Step 2: Automatically set the hash length to 8 (or another default)
    hash_length_default = 8  # Default hash length for MD5 collision search

    ram_usage_limit = input(f"Max RAM usage before auto stop (default: 50%): ")
    ram_usage_limit = int(ram_usage_limit) if ram_usage_limit else 50

    collision_goal = input(f"Number of collisions to find before stopping (default: 3): ")
    collision_goal = int(collision_goal) if collision_goal else 3

    return target_string, hash_length_default, ram_usage_limit, collision_goal

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_random_string(length=17, char_pool=string.ascii_uppercase):
    return ''.join(random.choice(char_pool) for _ in range(length))

def calculate_md5_hash(input_data, slice_length=8):
    full_md5_hash = hashlib.md5(input_data.encode()).hexdigest()
    return full_md5_hash[:slice_length]

def detect_collision(hash_key, associated_value, hash_mapping):
    if hash_key in hash_mapping and hash_mapping[hash_key] != associated_value:
        global total_collisions_found, collision_log
        collision_log[hash_key] = hash_mapping[hash_key]
        print(f"***** COLLISION FOUND *****")
        print(f"Hash 1: {hash_key} with value: {associated_value}")
        print(f"Hash 2: {hash_key} with value: {hash_mapping[hash_key]}")
        print(f"Using {hash_chars_to_check} characters long hash in {time.time() - program_start_time} seconds")
        print("************************* \n")
        total_collisions_found += 1
        return True
    else:
        hash_mapping[hash_key] = associated_value
        return False

def get_ram_usage():
    return psutil.virtual_memory().percent

def random_collision_detection(string_len, hash_len, ram_limit, collision_limit):
    global total_collisions_found, hash_database, collision_log
    total_collisions_found = 0
    hash_database = {}
    collision_log = {}

    test_attempts = 0
    while total_collisions_found < collision_limit:
        test_attempts += 1
        current_ram_usage = get_ram_usage()

        # Periodic progress update
        if test_attempts % 10000 == 0:
            print(f"Progress Update: {test_attempts} tests completed")
            print(f"Elapsed Time: {time.time() - program_start_time} seconds")
            print(f"RAM usage: {current_ram_usage}%")
            print(f"Collisions found: {total_collisions_found}")
            print(f"Current hashmap size: {len(hash_database)}\n")

        # Generate random strings and compute their hashes
        generated_string1 = create_random_string(string_len)
        generated_string2 = create_random_string(string_len)
        hash_for_string1 = calculate_md5_hash(generated_string1, hash_len)
        hash_for_string2 = calculate_md5_hash(generated_string2, hash_len)

        # Check for collisions
        if detect_collision(hash_for_string1, generated_string1, hash_database) or detect_collision(hash_for_string2, generated_string2, hash_database):
            total_collisions_found += 1

        # Stop if RAM usage exceeds the limit
        if current_ram_usage > ram_limit:
            print("Stopping. Excessive RAM usage detected.")
            break

def specific_collision_detection(input_string, hash_slice_length, ram_limit, collision_target):
    global total_collisions_found, hash_database, collision_log
    total_collisions_found = 0
    hash_database = {}
    collision_log = {}

    input_string_hash = calculate_md5_hash(input_string, hash_slice_length)

    print(f"Searching for collisions with hash: {input_string_hash}")

    num_tests = 0
    while total_collisions_found < collision_target:
        num_tests += 1
        current_ram_usage = get_ram_usage()

        # Simplified progress update
        if num_tests % 10000 == 0:
            print("====================================================================")
            print("\n")
            print(f"Progress Update: {num_tests} tests completed")
            print(f"Elapsed Time: {time.time() - program_start_time} seconds")
            print(f"RAM usage: {current_ram_usage}% \n")

        # Generate random strings and compute their hashes
        random_test_string = create_random_string()  # Default length
        test_hash = calculate_md5_hash(random_test_string, hash_slice_length)

        # Check if this hash matches the user-specified hash
        if test_hash == input_string_hash:
            total_collisions_found += 1
            print(f"***** COLLISION FOUND *****")
            print(f"String: {random_test_string} produces hash: {test_hash}")
            print("************************* \n")

        # Stop if RAM usage exceeds the limit
        if current_ram_usage > ram_limit:
            print("Stopping. Excessive RAM usage detected.")
            break


# Execution starts here
display_header()

while True:
    print_menu()
    selected_option = get_menu_choice()

    if selected_option == 1:
        print("\n")
        print("====================================================================")
        print("\n")
        str_len, hash_chars_to_check, max_ram_limit, collision_goal = get_random_collision_parameters()  # Use random collision parameters
        print("Running Random MD5 Collision Finder...\n")
        random_collision_detection(str_len, hash_chars_to_check, max_ram_limit, collision_goal)
        break
    elif selected_option == 2:
        print("\n")
        print("====================================================================")
        print("\n")
        user_input, hash_chars_to_check, max_ram_limit, collision_goal = get_specific_collision_parameters()  # Use specific collision parameters
        print("Running Specific MD5 Collision Finder...\n")
        specific_collision_detection(user_input, hash_chars_to_check, max_ram_limit, collision_goal)
        break
    elif selected_option == 3:
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please choose between 1, 2, or 3.")
