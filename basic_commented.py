# Import required modules for program.
import ast
from datetime import datetime
import time

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Bubble Sort Function                          #
#                            2. Main Program                                  #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
#                                1. Bubble Sort                               #
# --------------------------------------------------------------------------- #

def bubbleSort(array_to_sort):
    # Bubble Sort function.
    # Assisted by reference (11).

    # Calculate array length for use in loops.
    array_length = len(array_to_sort)

    for i in range(array_length):
        # Loop to array length.

        for j in range(0, array_length - i - 1):
            # Loop to array length, minus current parent loop number, minus 1.

            # Split selected array item and value to check against.
            current = array_to_sort[j].split()
            check = array_to_sort[j + 1].split()

            if datetime.strptime(current[0] + " " + current[1], '%d/%m/%Y %H:%M') > datetime.strptime(check[0] + " " + check[1], '%d/%m/%Y %H:%M'):
                # If current datetime (found at start of message) is older (larger) than value being checked against.
                # Parse split data (date and time) into datetime using strptime.

                # Perform swap of positions for two messages.
                array_to_sort[j], array_to_sort[j + 1] = array_to_sort[j + 1], array_to_sort[j]

    # Return array for display to screen.
    return array_to_sort
# --------------------------------------------------------------------------- #
#                               2. Main Program                               #
# --------------------------------------------------------------------------- #

# Load communication log file, parse string contents to list format.
communication_log = open("log.txt", "r")
communication_transmissions = ast.literal_eval(communication_log.read())

# Initialise blank list that will store all messages.
message_list = []

# Set start time for decryption.
decryption_start = time.time()

for message in communication_transmissions:
    # For each message within the communication log, loop.

    # Clear / initialise variables for loop/
    factor = []
    message_output = ""
    split_list = []

    # Algorithm loop to find two prime numbers that go into the public key, the prime factors.
    # Assisted by references (3, 4, 5)
    for i in range(2, message[0] + 1):
        # Count from numbers 3 to 1 more than the public key.

        if(message[0] % i == 0):
            # If the primary key, when modded by the loop number, has a remainder of 0.

            # Set prime_flag to
            prime_flag = 1

            for j in range(2, (i // 2 + 1)):
                # Loop from number 3 to one more than the square root of parent loop number.

                if(i % j == 0):
                    # If the parent loop number, when divided by the loop number, has a remainder of 0.

                    # Reset prime flag to 0 and break loop.
                    prime_flag = 0
                    break

            if (prime_flag == 1):
                # If prime flag has not been cancelled, append factor to list.
                factor.append(i)

    # Calculate key length for future calculations.
    # Assisted by reference (1).
    length = (factor[0] - 1) * (factor[1] - 1)

    # Algorithm loop to find decryption key.
    for i in range(length, length * 3):
        # Loop from length to 3 times the length.

        # Mathematical calculation to validate key.
        if((i * message[1]) % (length) == 1):
            # If loop number times the encryption key, modded by the length returns a value of 1.

            # Set decryption key and break loop.
            decryptionkey = i
            break

    # Split encrypted message by digit length of public key.
    split_length = len(str(message[0]))

    for i in range(0, len(message[2]), split_length):
        # For every set of characters, append to list.

        # Append to list the section of the string.
        # Assisted by reference (2).
        split_list.append(message[2][i:i + split_length] )

    for character in split_list:
        # For each character in the list.

        # Perform the decryption on the character, convert the result into a plain-text string from ASCII.
        # Extremely CPU intensive calculation due to scale of numbers. Will use the most CPU time of whole program.
        # Assisted by reference (1).
        decrypt = chr((int(character) ** int(decryptionkey)) % int(message[0]))

        # Append decrypted character to message result.
        message_output = message_output + decrypt

    # Append whole message to list.
    message_list.append(message_output + " - Private Key: " + str(decryptionkey))

# Restart time under new variable.
decryption_end = time.time()
sort_start = time.time()

# Execute bubble sort on list.
for message in (bubbleSort(message_list)):
    print(message)

# End time for sort.
sort_end = time.time()

# Print out timings for application.
print("Decryption Total Time:", decryption_end - decryption_start)
print("Sort Total Time:", sort_end - sort_start)