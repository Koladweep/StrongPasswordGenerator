from time import sleep
from secrets import choice
from zxcvbn import zxcvbn
from pandas import DataFrame as DF

class Generator:
    def __init__(self):
        self.passlist = []
        self.results = []
        self.df = DF()
        self.password_length=0
    def _generate_password(self,length):
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
        self.__init__()#clearing memory to clear out previously generated suggestions
        self.password_length=password_length
        self.passlist = [self._generate_password(password_length) for _ in range(n)]
        self.strengthEvaluator()

    def strengthEvaluator(self):
        """Accepts a list of passwords and returns insights in the form of list of the passwords and their score
        [on a scale of 0 to 4] and respective cracktime estimates at different brute force speeds."""
        self.results = []
        for i, password in enumerate(self.passlist):
            if not isinstance(password, str):
                raise ValueError("The Password list must contain string literals")

            insights = zxcvbn(password)
            self.results.append({
                'Sl.No.': i + 1,
                'suggested password': password,
                'score': insights['score'],
                '@100/hr': insights['crack_times_display']['online_throttling_100_per_hour'],
                '@36,000/hr': insights['crack_times_display']['online_no_throttling_10_per_second'],
                '@196,000/hr': insights['crack_times_display']['offline_slow_hashing_1e4_per_second'],
                '@792.9M/hr': insights['crack_times_display']['offline_fast_hashing_1e10_per_second']
            })

        self.df = DF(self.results)

    def get_top_passwords(self, n):
        """returns a subset of the original self.results containing top n suggestions sorted in descending order of strength"""
        df = self.df[self.df['score'] == 4]
        df = df.sort_values(by='score', ascending=False)  # Sort in descending order based on 'score'
        top_passwords = df.head(n).to_dict('records')  # Convert the top 'n' rows to a list of dictionaries
        return top_passwords

    def display_suggestions(self, n):#displays top n suggestions
        # Print the header
        if not isinstance(n,int):
            raise ValueError("n must be integer type")
        print(f'{"Sl.No.":<8} {"suggested password":<{self.password_length+5}} {"score":<10} {"@100/hr":<10} {"@36,000/hr":<10} {"@196,000/hr":<10} {"@792.9M/hr":<10}')
        top = self.get_top_passwords(n)
        # Print the data
        for row in top:
            print(f'{row["Sl.No."]:<8} {row["suggested password"]:{self.password_length+5}} {row["score"]:<10} {row["@100/hr"]:<10} {row["@36,000/hr"]:<10} {row["@196,000/hr"]:<13} {row["@792.9M/hr"]:<10}')

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
                break#if specified length is within hard coded constraints
        except ValueError:
            print('Invalid input. Try again.\n\n')

    while True:
        try:
            numberOfSuggestions = int(input('How many suggestions to generate? Enter a value between 1 to 100: ').strip())
            if not 0 < numberOfSuggestions <= 100:
                print('Only values between 1 and 100 (inclusive) are allowed.')
                continue
            else:
                break#if number of suggestions requested is within hard-coded limits
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
