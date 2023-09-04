from time import sleep
from secrets import choice
from zxcvbn import zxcvbn


class Generator:
    def __init__(self):
        """
        Initializes the Generator object with an empty list of passwords.
        """
        self.passlist = []

    def _generate_password(self, length):
        """
        Generates a random password of the given length using a combination of alphabets and symbols.
        
        :param length: The length of the password to generate
        :type length: int
        :return: The generated password
        :rtype: str
        """
        
        # Define the character sets to be used in the password generation
        alphabets = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        symbols = '`1234567890-=[]\\;\',./~!@#$%^&*()_+{}|:"<>?'

        # Calculate the number of symbols to be used
        num_symbols = int(length * 0.1)  # 10% of password length

        # Randomly choose alphabets and symbols to form the password
        password = [choice(alphabets) for _ in range(length - num_symbols)]
        password += [choice(symbols) for _ in range(num_symbols)]

        # Shuffle the password characters
        password = self._jumble_string(password)

        return ''.join(password)

    def _jumble_string(self, string):
        """
        Shuffles the characters in a given string.
        
        :param string: The string to shuffle
        :type string: str
        :return: The shuffled string
        :rtype: str
        """
        
        chars = list(string)
        jumbled_string = ''
        l = len(chars)
        
        for i in range(l):
            c = choice(chars)
            chars.remove(c)
            jumbled_string = jumbled_string + c

        return jumbled_string

    def generator(self, n, password_length):
        """
        Generates n passwords of the given length using the _generate_password method.
        
        :param n: The number of passwords to generate
        :type n: int
        """
        if not isinstance(n, int):
            raise TypeError("n must be an integer.")
        if not isinstance(password_length, int):
            raise TypeError("password_length must be an integer.")
        if password_length < 11:
            return []  # Return an empty list if the password length is less than 11
        self.__init__()  # Clear memory to clear out previously generated suggestions
        num_generated = 0  # Counter for the number of generated passwords with score 4
        while num_generated < n:
            password = self._generate_password(password_length)
            insights = zxcvbn(password)
            if insights['score'] == 4:
                self.passlist.append([password,insights['crack_times_seconds']['offline_fast_hashing_1e10_per_second']])
                num_generated += 1

    def get_top_N_passwords(self, N):
        """Returns a subset of the original self.passlist containing the top 'n' suggestions sorted by longest crack times.
        :param n: The upper bound to the number of top passwords to filter out.
        :type n: int
        """
        sorted_passwords = sorted(self.passlist, key=lambda p: p[1], reverse=True)
        return sorted_passwords[:N]

    
    def display_suggestions(self, N):
        """
        Displays the upto N top ranking passwords [if there are N or more, otherwise if less only upto what is present in the list] suggested passwords in a tabular format along with their score and crack time in hours.
        
        :param n: The number of top passwords to display
        :type n: int
        """
        
        # Fetch the top n passwords from the list of generated passwords
        top = self.get_top_N_passwords(N)
        
        # Determine the maximum password length in the top suggestions
        max_length = max(len(password) for password, _ in top)
        
        # Print the header
        print(f'{"Sl.No.":<8} {"suggested password":<{max_length+5}} {"score":<10} {"Vs e^10/sec Hashing[Hrs].":<27}')
        
        # Print the data
        for i, (password, crack_time) in enumerate(top, start=1):
            # Display the index, password, score and crack time in hours
            print(f'{i:<8} {password:<{max_length+5}} {4:<10} {crack_time / 3600:<.4f}')
    


def main():
    """An example of how this class can be used"""
    password_length = 0
    numberOfSuggestions = 0

    while True:
        try:
            password_length = int(input('Set password length between 15 to 25: ').strip())
            if not 15 <= password_length <= 25:
                print('Length must be between 15 and 25. Try again.')
                continue
            else:
                break  # If specified length is within hard-coded constraints
        except ValueError:
            print('Invalid input. Try again.\n\n')

    while True:
        try:
            numberOfSuggestions = int(input('How many suggestions to generate? Enter a value between 1 to 100: ').strip())
            if not 0 < numberOfSuggestions <= 100:
                print('Only values between 1 and 100 (inclusive) are allowed.')
                continue
            else:
                break  # If the number of suggestions requested is within hard-coded limits
        except ValueError:
            print('Invalid input. Try again.\n\n')

    generatorObject = Generator()
    generatorObject.generator(numberOfSuggestions, password_length)
    generatorObject.display_suggestions(10)

    print('\nPress Ctrl+C if you want to exit.\n')
    for i in range(30):
        sleep(.999)
        print(f'\rAutoterminating in {30 - i - 1} seconds', end='', flush=True)


if __name__ == "__main__":
    main()
