from time import sleep
from secrets import choice
from zxcvbn import zxcvbn
#from pandas import DataFrame as DF
class generator():
    def __init__(self) -> None:
        self.passlist=[]
        self.results=[]
    def _generate_password(self,length):
        # Define the character set to be used in the password generation
        qwerty_characters = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./~QWERTYUIOPASDFGHJKLZXCVBNM!@#$%^&*()_+{}|:\"<>?"
        qwerty_characters = self._jumble_string(qwerty_characters)
        password = []
        last_char = ''
        while len(password) < length:
            # Choose a random character from the character set
            char = choice(qwerty_characters)
            #avoiding adjacant character duplication and repetation more than 20 percent of character count
            if char != last_char and password.count(char) <length//5 and char in qwerty_characters:
                password.append(char)
                last_char = char
                qwerty_characters = self._jumble_string(qwerty_characters)
        # Convert the password list to a string, jumble it and return
        password = self._jumble_string(password)  # ... we are skipping this step to avoid undermining the logic that prevents clustering
        return ''.join(password)

    # a method that jumbles the provided string (in our case, the qwerty set of keystrokes to provide an added layer of randomness)
    def _jumble_string(self,string):
        chars = list(string)
        jumbled_string = ''
        l = len(chars)
        for i in range(l):
            c = choice(chars)
            chars.remove(c)
            jumbled_string = jumbled_string + c

        return jumbled_string


    def generator(self,n,password_length):
        if not isinstance(n, int):
            raise TypeError("n must be an integer.")
        if not isinstance(password_length, int):
            raise TypeError("password_length must be an integer.")
        # Generate n passwords and add them to the passlist
        for i in range(n):
            # Generate a password of the chosen length and add it to the passlist
            self.passlist.append(self._generate_password(password_length))
        self.strengthEvaluator()
    


    def strengthEvaluator(self):
        '''Accepts a list of passwords and returns insights in the form of list of the passwords and their score [on a scale of 0 to 4] and respective cracktime estimates at different brute force speeds.'''
        for password in self.passlist:
            if not isinstance(password,str):
                raise ValueError("The Password list must contain string literals")
        # Create an empty list to store the results
        # Calculate scores for each password suggestion along with estimated time to crack using standard brute force tests
        for i in range(len(self.passlist)):
            insights = zxcvbn(self.passlist[i])
            self.results.append({'Sl.No.':i+1,
                'suggested password': self.passlist[i],
                'score': insights['score'],'@100/hr':insights['crack_times_display']['online_throttling_100_per_hour'], '@36,000/hr':insights['crack_times_display']['online_no_throttling_10_per_second'], '@196,000/hr':insights['crack_times_display']['offline_slow_hashing_1e4_per_second'], '@792.9M/hr':insights['crack_times_display']['offline_fast_hashing_1e10_per_second']})
    def displaysuggestions(self):
        # Print the header
        print(f'{"Sl.No.":<10} {"suggested password":<20} {"score":<10} {"@100/hr":<15} {"@36,000/hr":<15} {"@196,000/hr":<15} {"@792.9M/hr":<15}')

        # Print the data
        for row in self.results:
            print(f'{row["Sl.No."]:<10} {row["suggested password"]:<20} {row["score"]:<10} {row["@100/hr"]:<15} {row["@36,000/hr"]:<15} {row["@196,000/hr"]:<15} {row["@792.9M/hr"]:<15}')

def main():
    class CustomError(Exception):
        pass
    password_length = 0
    numberOfSuggestions=0
    class CustomError(Exception):
        pass

    while True:
        try:
            password_length = int(input('Set password length between 17 to 25: ').strip())
            if not 17 <= password_length <= 25:
                raise CustomError('Length must be between 17 and 25. Try again.')
            if 17 <= password_length <= 25:
                break  # Break the loop if valid input is provided

        except ValueError:
            print('Invalid input. Try again.\n\n')
        
        except CustomError as e:
            print('Error:', str(e), '\n\n')

    while True:
        try:
            numberOfSuggestions = int(input('How many suggestions to generate? Enter a value between 1 to 100: ').strip())
            if not 0 < numberOfSuggestions <= 100:
                raise CustomError('Only values between 1 and 100 (inclusive) are allowed.')
            if 0 < numberOfSuggestions <= 100:
                break  # Break the loop if valid input is provided
        
        except ValueError:
            print('Invalid input. Try again.\n\n')
        
        except CustomError as e:
            print('Error:', str(e), '\n\n')

    generatorObject=generator()
    generatorObject.generator(numberOfSuggestions,password_length)
    generatorObject.displaysuggestions()    
    print('\nPress ctrl+c if you want to exit.\n')
    for i in range(30):
        sleep(.999)
        print(f'\r Autoterminating in {30 - i - 1} seconds', end='', flush=True)
if __name__ == "__main__":
    main()
