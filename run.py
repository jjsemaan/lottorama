import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json', scopes=SCOPE)
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('lottorama-data')

# Get data
lotto_data = SHEET.worksheet('euro').get_all_values()

# print(lotto_data)
print()
print("Welcome to Lottorama!")
print("Let us help you win the Euro Millions jackpot.")
print()
print("Please enter your favorite Euro Millions ticket numbers.")
print("Enter five numbers, strictly uniqe, between 1 and 50,")
print("with commas in between and no spaces.")
print("Example: 7,45,34,23,49\n")


def validate_data(values):
    """
    Check if exactly 5 values are entered.
    Check if values are strictly between 1 to 50.
    Check if these can be converted to integers.
    Check if the numbers are unique.
    Check if there are no spaces between values and commas.
    """
    errors = []

    # If the input is a list, convert it to a comma-separated string
    if isinstance(values, list):
        values = ','.join(map(str, values))

    # Check if there are spaces between values and commas
    if any(' ' in value for value in values.split(',')):
        errors.append("Error: Spaces are not allowed between values and commas.")

    # Convert each value to an integer and check if they are within the range of 1 to 50
    int_values = []
    for value in values.split(','):
        try:
            int_value = int(value)
            int_values.append(int_value)
        except ValueError as ve:
            errors.append(f"Error: {ve}")

    for value in int_values:
        if not 1 <= value <= 50:
            errors.append("Error: Values should be between 1 and 50.")

    # Check if exactly 5 values are provided
    if len(int_values) != 5:
        errors.append("Error: Exactly 5 values required.")
        
    # Check if the numbers are unique
    if len(set(int_values)) != 5:
        errors.append("Error: The 5 numbers should be unique.")

    if errors:
        print()
        for error in errors:
            print(error)
        print()
        print("* Please try again!")
        return False

    return True


def get_lotto_data():
    """
    Get lotto figures input from the user
    Run while loop until correct data is input
    """

    # Print the last draw date and winning numbers only once at the start
    euro = SHEET.worksheet("euro").get_all_values()
    last_draw = euro[-1]
    print(f"Last draw date: {last_draw[0]}")
    
    winning_numbers_str = ""
    for number in last_draw[1:6]:
        winning_numbers_str += number + ' '
    print(f"Winning numbers: {winning_numbers_str}\n")

    while True:
        
        data_str = input("Enter your five numbers here: ")
        lotto_data = data_str.split(",")

        if validate_data(lotto_data):
            print("Data is valid!")
            break

    return lotto_data


get_lotto_data()

