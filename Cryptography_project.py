import string
import random
import math


"""
SYMMETRIC
ENCRYPTION
FUNCTIONS
"""


def vigenere(text='', key='', typ='d'):
    # error handing for incorrect input
    if not text:
        print('Needs text')
        return
    if not key:
        print('Needs key')
        return
    if typ not in ('d', 'e'):
        print('Type must be "d" or "e"')
        return

    # unicode for chars in text and key
    keyLength = len(key)
    keyInts = [ord(i) for i in key]
    textInts = [ord(i) for i in text]
    returnString = ''

    # replace each letter of the original text according to the Vigenère table
    # depending on decode or encode set adder negative or positive
    for i in range(len(textInts)):
        adder = keyInts[i % keyLength]
        if typ == 'd':
            adder *= -1

        v = (textInts[i] - 32 + adder) % 95

        returnString += chr(v + 32)

    return returnString


def symmetricEncryption(messageSymmetric):
    # generate a key
    # two random numbers
    randomString = ''.join(random.choices(string.ascii_letters, k=256))
    randomString2 = ''.join(random.choices(string.ascii_letters, k=256))
    # then encrypt a string with them
    key = vigenere(randomString, randomString2, "e")

    encrypted = vigenere(messageSymmetric, key, 'e')
    decrypted = vigenere(encrypted, key, 'd')
    print("\nInitial message:")
    print(messageSymmetric, "\n")
    print("Your message after it was encrypted with secret key:")
    print(encrypted, "\n")
    print("Your message after it is decrypted with secret key:")
    print(decrypted, "\n")
    return 1


"""
ASYMMETRIC
ENCRYPTION
FUNCTIONS
"""


# global vars
# "prime" is the set of prime numbers
prime = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
         109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
         233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
         367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
         499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
         643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
         797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
         947, 953, 967, 971, 977, 983, 991, 997}
publicKey = 0
privateKey = 0
n = None


# pick a random prime number and remove it
# from the set of primes because p can't equal q
def getRandomPrime():
    global prime
    # random num
    rand = random.randint(0, len(prime) - 1)
    iterator = iter(prime)
    # iterate to the random prime with random number
    for _ in range(rand):
        next(iterator)

    # return and remove
    randPrime = next(iterator)
    prime.remove(randPrime)
    return randPrime


def makeKeys():
    # get primes
    global publicKey, privateKey, n
    p = getRandomPrime()
    q = getRandomPrime()

    # calculating n
    # n = p * q
    n = p * q

    # calculating totient, t
    totient = (p - 1) * (q - 1)

    # selecting public key, e
    e = 2
    while True:
        if math.gcd(e, totient) == 1:
            break
        e += 1

    publicKey = e

    # selecting private key, d
    # d = (k*Φ(n) + 1) / e for some integer k
    d = 2
    while True:
        if (d * e) % totient == 1:
            break
        d += 1

    privateKey = d


def encrypt(messageE):
    global publicKey, n
    e = publicKey
    encrypted_text = 1
    # encrypt using the public key (sender)
    while e > 0:
        encrypted_text *= messageE
        encrypted_text %= n
        e -= 1
    return encrypted_text


def decrypt(messageD):
    global privateKey, n
    d = privateKey
    decrypted = 1
    # decrypt using the private key (receiver)
    while d > 0:
        decrypted *= messageD
        decrypted %= n
        d -= 1
    return decrypted


# convert chars to ASCII value, then encode.
def encoder(messageEncode):
    encoded = []
    # calling the encrypting function in encoding function
    for letter in messageEncode:
        encoded.append(encrypt(ord(letter)))
    return encoded


# decode number to get ASCII then convert back to character.
def decoder(messageDecode):
    s = ''
    # calling the decrypting function decoding function
    for num in messageDecode:
        s += chr(decrypt(num))
    return s


def asymmetricEncryption(messageAsymmetric):
    # call function ONCE to make keys
    makeKeys()
    coded = encoder(messageAsymmetric)

    print("\nInitial message:")
    print(messageAsymmetric, "\n")
    print("The encoded message after being encrypted by public key:")
    print(''.join(str(p) for p in coded), "\n")
    print("The encoded message after being decrypted by private key:")
    print(''.join(str(p) for p in decoder(coded)), "\n")
    return 1


"""
HASHING
FUNCTION
"""


# hashing function
def hashFunction(messageHashing):
    # initialize hash value
    hashValue = 0

    # loop through string passed into function
    for i in range(len(message)):
        # add ascii value of each character to hash value
        hashValue += ord(message[i])
    #  raises hash value to the power of the last character in the string
    hashValue **= ord(message[len(message) - 1])

    # converts hash into string
    hashValue = str(hashValue)

    # prints first 16 characters of the number
    print("\nInitial message:")
    print(messageHashing, "\n")
    print("The hash value for the given message is:")
    print(hashValue[:16], "\n")

    return 1


"""
TESTING
FUNCTIONS
"""


# function that takes user input that decides type of encryption to be used
def typeOfEncryption():
    answer = 0
    while answer < 1 or answer > 4:
        print("Pick which type of Encryption you want to use:")
        print("For Symmetric Encryption, Type \"1\" ")
        print("For Asymmetric Encryption, Type \"2\" ")
        print("For Hashing, Type \"3\" ")
        print("To Stop Testing, Type \"4\" ")
        try:
            answer = int(input())
            if answer < 1 or answer > 4:
                print("Please enter 1, 2, 3, or 4 corresponding to your choice. ")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    if answer == 1:
        print("You chose Symmetric Encryption!")
        return 1
    elif answer == 2:
        print("You chose Asymmetric Encryption!")
        return 2
    elif answer == 3:
        print("You chose Hashing!")
        return 3
    else:
        return 4


# function to get valid user input
def getUserInput(x):
    if x == 1:
        userIn = input("Enter the string to be encrypted:")

        while userIn == "":
            print("You must enter a valid message.")

            userIn = input("Enter the string to be encrypted:")
    else:
        userIn = input("Enter the string to be hashed:")

        while userIn == "":
            print("You must enter a valid message.")

            userIn = input("Enter the string to be encrypted:")

    return userIn


"""
MAIN
"""


choice = 0
while choice != 4:
    choice = typeOfEncryption()
    if choice == 1:
        message = getUserInput(1)
        if symmetricEncryption(message) == 1:
            print("Symmetric Encryption Complete!\n")

    elif choice == 2:
        message = getUserInput(1)
        if asymmetricEncryption(message) == 1:
            print("Symmetric Encryption Complete!\n")

    elif choice == 3:
        message = getUserInput(2)
        if hashFunction(message) == 1:
            print("Hashing Complete!\n")
    else:
        print("Testing Completed! Terminating...")
