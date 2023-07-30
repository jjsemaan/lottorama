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
lotto_data = SHEET.worksheet('euro').get_all_values()

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

    for value in int_values:
        if not 1 <= value <= 50:
            errors_five_nums.append("Error: Values should be between 1 and 50.")

    # Check if exactly 5 values are provided
    if len(int_values) != 5:
        errors_five_nums.append("Error: Exactly 5 values required.")
        
    # Check if the numbers are unique
    if len(set(int_values)) != 5:
        errors_five_nums.append("Error: The 5 numbers should be unique.")

    if errors_five_nums:
        # Print the errors, if any, and return False indicating data is not valid
        print()
        for error in errors_five_nums:
            print(error)
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
    list: A list of user-entered Euro Millions ticket numbers.
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
        # lotto_data = SHEET.worksheet('euro').get_all_values()
        data_str = input("Enter your five numbers here: ")
        lotto_data = data_str.split(",")

        # Validate the user-entered data
        if validate_data(lotto_data):
            print("Data is valid!")
            break

    return lotto_data


def push_to_user_workbook(lotto_data):
    """
    Function to push user-entered Euro Millions ticket numbers to the 'user' workbook.

    Args:
    lotto_data (list): A list of user-entered Euro Millions ticket numbers.
    """

    try:
        # Access the 'user' worksheet
        user_workbook = SHEET.worksheet("user")

        # Slice the lotto_data list to get the data for cells B1 to F1
        data_for_cells_B1_to_F1 = lotto_data[:5]

        # Insert data to B1 to F1 cells preceded by the string 'Numbers:' at A1
        data_for_cells_B1_to_F1.insert(0, "Numbers:")

        # Update the individual cells within the range B1:F1 with the new data
        for col_index, value in enumerate(data_for_cells_B1_to_F1, start=1):
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

        # Validate the user-entered data
        if validate_data(lotto_data):
            # Push the data to the 'user' workbook if it is valid and break the loop
            push_to_user_workbook(lotto_data)
            break
