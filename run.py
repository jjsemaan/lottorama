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


def validate_data(values):
    """
    Check if exactly 5 values are entered.
    Check if values are strictly between 1 to 50
    Check if these can be converted to integers
    """
    try:
        # Convert each value to an integer and check if they are within the range of 1 to 50
        int_values = [int(value) for value in values]
        for value in int_values:
            if not 1 <= value <= 50:
                raise ValueError("Values should be between 1 and 50.")
        
        if len(values) != 5:
            raise ValueError(
                f"Exactly 5 values required and you provided only {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}\n")
        return False
   
    return True


def get_lotto_data():
    """
    Get lotto figures input from the user
    Run while loop until correct data is input
    """
    while True:
        print()
        print("Welcome to Lottorama!")
        print("Let us help you win the Euro Millions jackpot.")
        print()

        euro = SHEET.worksheet("euro").get_all_values()
        last_draw = euro[-1]

        # Print the first element of last_draw (index 0)
        print(f"Last draw date: {last_draw[0]}")

        # Print the rest of the elements in the list (index 1 to 5)
        winning_numbers_str = ""
        for number in last_draw[1:6]:
            winning_numbers_str += number + ' '

        # Print the winning numbers on the same line
        print(f"Winning numbers: {winning_numbers_str}")
        print()  # Add an empty row

        print("Please enter your favorite Euro Millions ticket numbers.")
        print("Numbers should be five numbers separated by commas.")
        print("Example: 7,45,34,23,49\n")
        print()  # Add an empty row

        data_str = input("Enter your data here:\n")
        lotto_data = data_str.split(",")

        if validate_data(lotto_data):
            print("Data is valid!")
            break

    return lotto_data


get_lotto_data()

