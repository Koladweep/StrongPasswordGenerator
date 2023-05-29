import secrets
import string
import random
import zxcvbn
from decimal import*

def generate_password(length):
    # Define the character set to be used in the password generation
    #character_set = string.ascii_letters + string.digits + string.punctuation
    qwerty_characters = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~QWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+{}|:\"<>?"
    qwerty_characters = jumble_string(qwerty_characters)
    password = []
    last_char = ''
    while len(password) < length:
        # Choose a random character from the character set
        char = secrets.choice( qwerty_characters)
        # Check if the character meets the conditions for inclusion in the password
        if char != last_char and password.count(char) < 2 and char in qwerty_characters:
            password.append(char)
            last_char = char
            qwerty_characters=jumble_string(qwerty_characters)
    # Convert the password list to a string, jumble it and return
    password=jumble_string(password)#... we are skipping this step to avoid undermining the logic that prevents clustering
    return ''.join(password)
# a method that jumnles the provided string( in our case, the qwerty set of keystrokes to provide an added layer of randomness
def jumble_string(string):
    chars = list(string)
    jumbled_string=''
    l=len(chars)
    for i in range(l):
        c=secrets.choice(chars)
        chars.remove(c)
        jumbled_string=jumbled_string+c
    
    return jumbled_string


passlist = []
# Generate 20 passwords and add them to the passlist
for i in range(20):
    # Choose a random password length between 16 and 20 characters
    password_length = random.randint(16, 20)
    # Generate a password of the chosen length and add it to the passlist
    passlist.append(generate_password(password_length))
print('scores on a scale from 0 to 4 where 0 means bad and 4 means very strong and 3 is average')
#printing scores for each password suggestion along with estimated time to crack using standard brute force tests
for i in passlist:
  insights=zxcvbn.zxcvbn(i)
  print(f"suggestion: {i}, score:{insights['score']}, cracktime offline fasthashing 1e10 per second: {insights['crack_times_display']['offline_fast_hashing_1e10_per_second']}")
