# Import required modules for program.
import ast
import time
from multiprocessing import Pool

# --------------------------------------------------------------------------- #
#                                  CONTENTS                                   #
#                            1. Message Class                                 #
#                            2. Main Program Init                             #
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
#                               1. Message Class                              #
# --------------------------------------------------------------------------- #

# Define primary class to handle message functions.
class Message:

    # ----------------------------------------------------------------------- #
    #                            1. Core Functions                            #
    #                                                                         #
    #                                __init__                                 #
    #                Initialises message details for the class.               #
    #                                                                         #
    #                             calculate_length                            #
    #  Checks odd numbers up to 500 to find two prime factors of public key.  #
    #                                                                         #
    #                           calculate_decryption                          #
    #      Executes mathmatical calculation to determine decryption key.      #
    #                                                                         #
    #                                 decrypt                                 #
    #         Splits encrypted message into characters, decrypts each.        #
    # ----------------------------------------------------------------------- #

    # Initialise message class and variables.
    def __init__(self, public_key, encryption_key, encrypted_message):
        self.public_key = public_key
        self.encryption_key = encryption_key
        self.encrypted_message = encrypted_message
        self._decrypted_message = ""
        self._decryption_key = 0
        self._decrypted_dictionary = {}
        self._length = 0
        self._factors = []

    # Calculate the length that corresponds to public key.
    def calculate_length(self):
        # Algorithm loop to find two prime numbers that go into the public key, the prime factors.
        # Assisted by references (3, 4, 5).
        for i in range(3, 500, 2):
            # Count from numbers 3 to fixed number for excise of 500. Loop in steps of 2 to skip even numbers.

            if(self.public_key % i == 0):
                # If the primary key, when modded by the loop number, has a remainder of 0.

                # Set prime_flag to
                prime_number = True
                for n in range(3, (i // 2 + 1), 2):
                    # Loop from number 3 to one more than the square root of parent loop number in steps of 2 to skip even numbers.

                    if(i % n == 0):
                        # If the parent loop number, when divided by the loop number, has a remainder of 0.

                        # Reset prime flag to 0 and break loop.
                        prime_number = False
                        break

                if (prime_number == True):
                    # If prime flag has not been cancelled, append factor to list.
                    self._factors.append(i)

        # RSA Mathmatical Calculation
        # Calculate key length for future calculations
        # Assisted by reference (1).
        self._length = (self._factors[0] - 1) * (self._factors[1] - 1)

    # Calculate the decryption key (private key).
    def calculate_decryption(self):
        # Algorithm loop to find decryption key.
        for i in range(self._length + 1, self._length * 2, 2):
            # Loop from length + 1 (odd number) to 2 times the length. Loops in steps of 2 to skip all even numbers that would never be prime.

            # Mathmatical calculation to validate key.
            if((i * self.encryption_key) % self._length == 1):
                # If loop number times the encryption key, modded by the length returns a value of 1.

                # Set decryption key and break loop.
                self._decryption_key = i
                break

    # Decrypt message.
    def decrypt(self):
        # Call methods to generate the length and decryption key that match public key.
        self.calculate_length()
        self.calculate_decryption()

        split_list = []

        for i in range(0, len(self.encrypted_message), len(str(self.public_key))):
            # For every set of characters, append to list.

            # Append to list the section of the string.
            # Assisted by reference (2).
            split_list.append(self.encrypted_message[i:i+len(str(self.public_key))])

        # Leverage Python MultiProcessing technique to make use of additional application threads.
        # The calculation performed by decrypt_character is extremely CPU intensive calculation (takes >98% of the total program execution time) due to scale of numbers.
        # Within CPU limitations, split processing of decryption into different threads. Current value decrypts 32 characters at a time.
        with Pool(32) as multi_processor:
            # Join together the array returned from running decrypt_character in parralell. Passes list of characters to function.
            # Assisted by references (7, 9, 10).
            self._decrypted_message = ''.join(multi_processor.map(self.decrypt_character, split_list))

        # Return data.
        return [self._decrypted_message, self._decryption_key]

    def decrypt_character(self, character):
        # Function to be leveraged during multi-processing. Decrypts character using decryption key.

        # Assisted by reference (6).
        if character not in self._decrypted_dictionary:
            # If character is not present in the dictionary, it hasn't been decrypted before.
            # If character has already been decrypted, will skip over CPU intensive calculation and read directly from dictionary.

            # Perform the decryption on the character, convert the result into a plaintext string from ASCII.
            # Assisted by reference (1).
            self._decrypted_dictionary[character] = chr((int(character) ** int(self._decryption_key)) % int(self.public_key))

        # Return decrypted character.
        return self._decrypted_dictionary[character]
# --------------------------------------------------------------------------- #
#                             2. Main Program Init                            #
# --------------------------------------------------------------------------- #

if __name__ == '__main__':

    # Load communication log file, parse string contents to list format.
    communication_log = open("log.txt", "r")
    communication_transmissions = ast.literal_eval(communication_log.read())

    # Initialise blank list that will store all messages.
    message_list = []

    # Set start time for decryption.
    decryption_start = time.time()

    for transmission in communication_transmissions:
        # For each message within the communication log, loop.

        # Initialise message object.
        message_handler = Message(transmission[0], transmission[1], transmission[2])

        # Execute decryption method on object.
        message_output, decryption_key = message_handler.decrypt()

        # Append whole message to list.
        message_list.append(message_output + " - Private Key: " + str(decryption_key))

    # Restart time under new variable.
    sort_start, decryption_end = time.time()

    # Use sorted method to sort list based on the date + time.
    # Method uses timsort, mix of merge and insertion sort. Efficient for larger data sets.
    # Assisted by reference (7).
    for message in (sorted(message_list, key = lambda x: x.split()[0] + " " + x.split()[1])):
        print(message)

    # End time for sort.
    sort_end = time.time()

    # Print out timings for application.
    print("Decryption Total Time:", decryption_end - decryption_start)
    print("Sort Total Time:", sort_end - sort_start)
