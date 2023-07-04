from time import sleep
from secrets import choice
from zxcvbn import zxcvbn
#from pandas import DataFrame as DF
password_length = 0
while not (17 <= password_length <= 25):
    try:
        password_length = int(input('Set password length between 17 to 25: '))
    except:
        print('Invalid input. Enter a value between 17 and 25.\n\n')

def generate_password(length):
    # Define the character set to be used in the password generation
    qwerty_characters = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~QWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+{}|:\"<>?"
    qwerty_characters = jumble_string(qwerty_characters)
    password = []
    last_char = ''
    while len(password) < length:
        # Choose a random character from the character set
        char = choice(qwerty_characters)
        # Check if the character meets the conditions for inclusion in the password
        if char != last_char and password.count(char) < 2 and char in qwerty_characters:
            password.append(char)
            last_char = char
            qwerty_characters = jumble_string(qwerty_characters)
    # Convert the password list to a string, jumble it and return
    password = jumble_string(password)  # ... we are skipping this step to avoid undermining the logic that prevents clustering
    return ''.join(password)

# a method that jumbles the provided string (in our case, the qwerty set of keystrokes to provide an added layer of randomness)
def jumble_string(string):
    chars = list(string)
    jumbled_string = ''
    l = len(chars)
    for i in range(l):
        c = choice(chars)
        chars.remove(c)
        jumbled_string = jumbled_string + c

    return jumbled_string


passlist = []
# Generate 20 passwords and add them to the passlist
for i in range(20):
    # Generate a password of the chosen length and add it to the passlist
    passlist.append(generate_password(password_length))

print('\nScores on a scale of 0 to 4 and respective cracktime estimates for the suggested passwords\n\n')

# Create an empty list to store the results
results = []

# Calculate scores for each password suggestion along with estimated time to crack using standard brute force tests
for i in range(20):
    insights = zxcvbn(passlist[i])

    results.append({'Sl.No.':i+1,
        'suggested password': passlist[i],
        'score': insights['score'],'@100/hr':insights['crack_times_display']['online_throttling_100_per_hour'], '@36,000/hr':insights['crack_times_display']['online_no_throttling_10_per_second'], '@196,000/hr':insights['crack_times_display']['offline_slow_hashing_1e4_per_second'], '@792.9M/hr':insights['crack_times_display']['offline_fast_hashing_1e10_per_second']})

# Print the header
print(f'{"Sl.No.":<10} {"suggested password":<20} {"score":<10} {"@100/hr":<15} {"@36,000/hr":<15} {"@196,000/hr":<15} {"@792.9M/hr":<15}')

# Print the data
for row in results:
    print(f'{row["Sl.No."]:<10} {row["suggested password"]:<20} {row["score"]:<10} {row["@100/hr"]:<15} {row["@36,000/hr"]:<15} {row["@196,000/hr"]:<15} {row["@792.9M/hr"]:<15}')

print('\nPress ctrl+c if you want to exit.\n')
for i in range(30):
    sleep(.999)
    print(f'\r Autoterminating in {30 - i - 1} seconds', end='', flush=True)
