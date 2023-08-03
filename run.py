# Import required libraries
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import time
from tabulate import tabulate

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
        print("Error: Exactly 5 whole numbers required!")
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
    list: A list of user-entered Euro Millions ticket numbers
    and lucky numbers.
    """

    # Print the last draw date and winning numbers only once at the start
    euro = SHEET.worksheet("euro").get_all_values()
    last_draw = euro[-1]
    print(f"Last draw date: {last_draw[0]}")
    
    winning_numbers_str = ""
    for number in last_draw[1:6]:
        winning_numbers_str += number + ' '
    print(f"Winning numbers: {winning_numbers_str}")
    
    winning_lucky_numbers_str = ""
    for number in last_draw[6:8]:
        winning_lucky_numbers_str += number + ' '
    print(f"Lucky numbers: {winning_lucky_numbers_str}\n")

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
        lucky_numbers_str = input("Enter your two lucky numbers (separated by commas): ")

        # Check if the input contains spaces
        if " " in lucky_numbers_str:
            print("Error: Spaces are not allowed. Please re-enter lucky numbers without spaces.")
            continue

        # Remove spaces from the input string
        lucky_numbers_str = lucky_numbers_str.replace(" ", "")

        # Split the input by commas
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
            print("Error: Please enter only two valid integers for lucky numbers.")

    # Combine lotto_data_five_nums and lucky_numbers into a single list
    # with a comma in between and sort the numbers in ascending order
    lotto_data_five_nums = sorted([int(num) for num in lotto_data_five_nums])
    lucky_numbers = sorted(lucky_numbers)

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

        # Update the individual cells within the range B1:H1 with the new data
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

        # Delay execution by 2 seconds to allow workbook updates
        time.sleep(2)

        # Get user numbers lotto_data_five_nums and lucky_numbers
        # Sort the numbers
        print()
        
        user_ranking = SHEET.worksheet("user-ranking").get_all_values()
        # split into three sublist before creating a table
        numbers_row = user_ranking[0]
        num_list = numbers_row[1:6]
        num_lucky = numbers_row[6:8]
        numbers_list = [num_list]
        lucky_list = [num_lucky]

        rankings_row = user_ranking[-1]
        rank_list = rankings_row[1:6]
        rank_lucky = rankings_row[6:8]
        rankings_list = [rank_list]
        rankings_lucky = [rank_lucky]

        # Print about table
        print("""The below table provides info on repeat wins on 
each of your numbers from previous all-time draws.""")

        # Add blank values to num_lucky and rank_lucky to match 
        # the length of num_list otherwise this lacing to shortest by default
        num_lucky += [""] * (len(num_list) - len(num_lucky))
        rank_lucky += [""] * (len(num_list) - len(rank_lucky))

        # Create a 2D list with each element in a separate row
        data = []
        for i in range(len(num_list)):
            data.append([num_list[i], rank_list[i], num_lucky[i], rank_lucky[i]])

        # Print the table
        headers = ["Numbers", "Wins", "Lucky Numbers", "Wins"]
        print(tabulate(data, headers=headers, tablefmt="pretty"))

        # Convert lists to integers and transpose the results
        num_list = [int(num) for num in num_list]
        rank_list = [int(rank) for rank in rank_list]
        transpose_nums = list(zip(num_list, rank_list))
        transpose_lucky = list(zip(numbers_row[6:8], rankings_row[6:8]))

        # Filter out the pairs by index 1 and store the corresponding index 0 numbers
        popular_numbers = []
        moderately_popular_numbers = []
        least_popular_numbers = []

        try:
            for pair in transpose_nums:
                if pair[1] >= 5:
                    popular_numbers.append(pair[0])
                elif pair[1] == 4:
                    moderately_popular_numbers.append(pair[0])
                elif pair[1] <= 3:
                    least_popular_numbers.append(pair[0])
        except IndexError:
            pass

        # Count the numbers that are greater than or equal to 5
        # Count the numbers that are equal to 4
        # Count the numbers that are less than or equal to 3
        count_popular = len(popular_numbers)
        count_moderately_popular = len(moderately_popular_numbers)
        count_least_popular = len(least_popular_numbers)

        if count_least_popular == 1:
            clp_numbers = "number"
        else:
            clp_numbers = "numbers"

        if count_moderately_popular == 1:
            cmp_numbers = "number"
        else:
            cmp_numbers = "numbers"

        if count_popular == 1:
            cp_numbers = "number"
        else:
            cp_numbers = "numbers"
                        
        # Summary of winning numbers
        print(f"You have {count_popular} {cp_numbers} {popular_numbers} listed in the most popular winning numbers.")
        print(f"You have {count_moderately_popular} {cmp_numbers} {moderately_popular_numbers} listed in the moderately popular winning numbers.")
        print(f"You have {count_least_popular} {clp_numbers} {least_popular_numbers} listed in the least popular winning numbers.")
                
        print(transpose_nums)
        print(transpose_lucky)
        break
