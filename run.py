# Import required libraries
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

# Define the required Google Sheets API scope permissions
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load the credentials from the service account JSON file 'creds.json' 
# and specify the scope
CREDS = Credentials.from_service_account_file('creds.json', scopes=SCOPE)

# Create a new credentials object with the specified scope
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorise the gspread client with the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheets document named 'lottorama-data'
SHEET = GSPREAD_CLIENT.open('lottorama-data')

# Get data from the worksheet named 'euro' and store it as a list of lists
# lotto_data = SHEET.worksheet('euro').get_all_values()

# Print welcome message and instructions for the user
print()
print("Welcome to Lottorama!")
print("Let us help you win the Euro Millions jackpot.")
print()
print("Please enter your favorite Euro Millions ticket numbers.")
print("Enter five numbers, strictly unique, between 1 and 50,")
print("with commas in between and no spaces.")
print("Example: 7,45,34,23,49\n")


def validate_data(values):
    """
    Function to validate user-entered data for Euro Millions ticket numbers of user.

    Args:
    values (str or list): The user-entered numbers as a comma-separated string or list.

    Returns:
    bool: True if the data is valid, False otherwise.
    """

    errors_five_nums = []

    # If the input is a list, convert it to a comma-separated string
    if isinstance(values, list):
        values = ','.join(map(str, values))

    # Check if there are spaces between values and commas
    if any(' ' in value for value in values.split(',')):
        errors_five_nums.append("Error: Spaces not allowed between values and commas.")

    # Convert each value to an integer and check if they are within
    # the range of 1 to 50
    int_values = []
    for value in values.split(','):
        try:
            int_value = int(value)
            int_values.append(int_value)
        except ValueError as ve:
            errors_five_nums.append(f"Error: {ve}")
    
    # Check if exactly 5 values are provided
    if len(int_values) != 5:
        errors_five_nums.append("Error: Exactly 5 values required.")
        print("Error: Exactly 5 values required!")
        print()
        return False

    for value in int_values:
        if not 1 <= value <= 50:
            errors_five_nums.append("Error: Values should be between 1 and 50.")
    
    # Check if the numbers are unique
    if len(set(int_values)) != 5:
        errors_five_nums.append("Error: The 5 numbers should be unique.")

    if errors_five_nums:
        # Print the errors, if any, and return False indicating data is not valid
        print()
        for num in errors_five_nums:
            print(num)
        print()
        print("* Please try again!")
        return False

    # Return True if the data is valid
    return True


def user_lotto_data():
    """
    Function to get lotto figures input from the user.
    Runs a while loop until correct data is entered.

    Returns:
    list: A list of user-entered Euro Millions ticket numbers and lucky numbers.
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
        # Get user input for Euro Millions ticket numbers
        lotto_data_five_nums = []
        data_str_five_nums = input("Enter your five numbers here (separated by commas): ")
        lotto_data_five_nums = data_str_five_nums.split(",")

        # Validate the user-entered data
        if validate_data(lotto_data_five_nums):
            print("Data is valid!")
            break
        else:
            print("Error: Invalid data format.")

    while True:
        # Get user input for the 2 lucky numbers between 1 and 12
        lucky_numbers = []
        lucky_numbers_str = input("Enter your two lucky numbers (separated by commas): ")
        lucky_numbers = lucky_numbers_str.split(",")

        # Validate the user-entered data for lucky numbers
        try:
            lucky_numbers = [int(num) for num in lucky_numbers]
            if all(1 <= num <= 12 for num in lucky_numbers) and len(lucky_numbers) == 2:
                # Check if lucky_numbers are unique
                if len(set(lucky_numbers)) == 2:
                    print("Lucky numbers are valid!")
                    break
                else:
                    print("Error: Lucky numbers should be two unique integers between 1 and 12.")
            else:
                print("Error: Lucky numbers should be two integers between 1 and 12.")
        except ValueError:
            print("Error: Please enter valid integers for lucky numbers.")

    # Combine lotto_data_five_nums and lucky_numbers into a single list with a comma in between
    lotto_data = lotto_data_five_nums + lucky_numbers

    return lotto_data


def push_to_user_workbook(lotto_data):
    """
    Function to push user-entered Euro Millions ticket 
    numbers to the 'user' workbook.

    Args:
    lotto_data_five_nums (list): A list of user-entered 
    Euro Millions ticket numbers.
    """

    try:
        # Access the 'user' worksheet
        user_workbook = SHEET.worksheet("user")

        # Slice the lotto_data list to get the data for cells B1 to H1
        data_for_cells_B1_to_H1 = lotto_data[:7]

        # Insert data to B1 to F1 cells preceded by the string 'Numbers:' at A1
        data_for_cells_B1_to_H1.insert(0, "Numbers:")

        # Update the individual cells within the range B1:F1 with the new data
        for col_index, value in enumerate(data_for_cells_B1_to_H1, start=1):
            user_workbook.update_cell(1, col_index, value)

        print("Your data has been successfully updated in the 'user' workbook!")
    except Exception as e:
        print("An error occurred while pushing data to the 'user' workbook:")
        print(e)


if __name__ == "__main__":
    # Main program execution starts here
    print()
    print("Welcome to Lottorama!")
    print("Let us help you win the Euro Millions jackpot.")
    print()
    print("Please enter your favorite Euro Millions ticket numbers.")
    print("Enter five numbers, strictly unique, between 1 and 50,")
    print("with commas in between and no spaces.")
    print("Example: 7,45,34,23,49\n")

    while True:
        # Get user-entered Euro Millions ticket numbers
        lotto_data = user_lotto_data()

        # Push the data to the 'user' workbook if it is valid
        push_to_user_workbook(lotto_data)
        break
