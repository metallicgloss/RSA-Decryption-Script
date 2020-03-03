import ast
from datetime import datetime
def bubbleSort(array_to_sort):
    array_length = len(array_to_sort)
    for i in range(array_length):
        for j in range(0, array_length - i - 1):
            current = array_to_sort[j].split()
            check = array_to_sort[j + 1].split()
            if datetime.strptime(current[0] + " " + current[1], '%d/%m/%Y %H:%M') > datetime.strptime(check[0] + " " + check[1], '%d/%m/%Y %H:%M'):
                array_to_sort[j], array_to_sort[j + 1] = array_to_sort[j + 1], array_to_sort[j]
    return array_to_sort
communication_log = open("log.txt", "r")
communication_transmissions = ast.literal_eval(communication_log.read())
message_list = []
for message in communication_transmissions:
    factor = []
    message_output = ""
    split_list = []
    for i in range(2, message[0] + 1):
        if(message[0] % i == 0):
            prime_flag = 1
            for j in range(2, (i // 2 + 1)):
                if(i % j == 0):
                    prime_flag = 0
                    break
            if (prime_flag == 1):
                factor.append(i)
    length = (factor[0] - 1) * (factor[1] - 1)
    for i in range(length, length * 3):
        if((i * message[1]) % (length) == 1):
            decryptionkey = i
            break
    split_length = len(str(message[0]))
    for i in range(0, len(message[2]), split_length):
        split_list.append(message[2][i:i + split_length] )
    for character in split_list:
        decrypt = chr((int(character) ** int(decryptionkey)) % int(message[0]))
        message_output = message_output + decrypt
    message_list.append(message_output + " - Private Key: " + str(decryptionkey))
for message in (bubbleSort(message_list)):
    print(message)