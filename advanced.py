import ast
import time
from multiprocessing import Pool
class Message:
    def __init__(self, public_key, encryption_key, encrypted_message):
        self.public_key = public_key
        self.encryption_key = encryption_key
        self.encrypted_message = encrypted_message
        self._decrypted_message = ""
        self._decryption_key = 0
        self._decrypted_dictionary = {}
        self._length = 0
        self._factors = []
    def calculate_length(self):
        for i in range(3, 500, 2):
            if(self.public_key % i == 0):
                prime_number = True
                for n in range(3, (i // 2 + 1), 2):
                    if(i % n == 0):
                        prime_number = False
                        break
                if (prime_number == True):
                    self._factors.append(i)
        self._length = (self._factors[0] - 1) * (self._factors[1] - 1)
    def calculate_decryption(self):
        for i in range(self._length + 1, self._length * 2, 2):
            if((i * self.encryption_key) % self._length == 1):
                self._decryption_key = i
                break
    def decrypt(self):
        self.calculate_length()
        self.calculate_decryption()
        split_list = []
        for i in range(0, len(self.encrypted_message), len(str(self.public_key))):
            split_list.append(self.encrypted_message[i:i+len(str(self.public_key))])
        with Pool(32) as multi_processor:
            self._decrypted_message = ''.join(multi_processor.map(self.decrypt_character, split_list))
        return [self._decrypted_message, self._decryption_key]
    def decrypt_character(self, character):
        if character not in self._decrypted_dictionary:
            self._decrypted_dictionary[character] = chr((int(character) ** int(self._decryption_key)) % int(self.public_key))
        return self._decrypted_dictionary[character]
if __name__ == '__main__':
    communication_log = open("log.txt", "r")
    communication_transmissions = ast.literal_eval(communication_log.read())
    message_list = []
    decryption_start = time.time()
    for transmission in communication_transmissions:
        message_handler = Message(transmission[0], transmission[1], transmission[2])
        message_output, decryption_key = message_handler.decrypt()
        message_list.append(message_output + " - Private Key: " + str(decryption_key))
    decryption_end = time.time()
    sort_start = time.time()
    for message in (sorted(message_list, key = lambda x: x.split()[0] + " " + x.split()[1])):
        print(message)
    sort_end = time.time()
    print("Decryption Total Time:", decryption_end - decryption_start)
    print("Sort Total Time:", sort_end - sort_start)