# Import required libraries
import gspread
from google.oauth2.service_account import Credentials
import time
import random
from tabulate import tabulate
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# Define the required Google Sheets API scope permissions
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

"""
Load the credentials from the service account JSON file 'creds.json'
and specify the scope
"""
CREDS = Credentials.from_service_account_file('creds.json', scopes=SCOPE)

# Create a new credentials object with the specified scope
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorise the gspread client with the scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Open the Google Sheets document named 'lottorama-data'
SHEET = GSPREAD_CLIENT.open('lottorama-data')


def validate_data(values):
    """
    Function to validate user-entered data for
    Euro Millions ticket numbers of user.

    Args:
    values (str or list): The user-entered numbers
    as a comma-separated string or list.

    Returns:
    bool: True if the data is valid, False otherwise.
    """

    errors_five_nums = []

    # If the input is a list, convert it to a comma-separated string
    if isinstance(values, list):
        values = ','.join(map(str, values))

    # Check if there are spaces between values and commas
    if any(' ' in value for value in values.split(',')):
        errors_five_nums.append(
            Fore.RED + Style.BRIGHT +
            "Error: Spaces not allowed between values and commas."
            )

    """
    Convert each value to an integer and check if they are within
    the range of 1 to 50
    """
    int_values = []
    for value in values.split(','):
        try:
            int_value = int(value)
            int_values.append(int_value)
        except ValueError as ve:
            errors_five_nums.append(
                f"{Fore.RED}{Style.BRIGHT}Error: {ve}"
                )

    # Check if exactly 5 values are provided
    if len(int_values) != 5:
        errors_five_nums.append(
            Fore.RED + Style.BRIGHT + "Error: Exactly 5 values required."
            )
        print(
            Fore.RED + Style.BRIGHT +
            "Error: Exactly 5 whole numbers required! \n"
            )
        return False

    for value in int_values:
        if not 1 <= value <= 50:
            errors_five_nums.append(
                Fore.RED + Style.BRIGHT +
                "Error: Values should be between 1 and 50."
                )

    # Check if the numbers are unique
    if len(set(int_values)) != 5:
        errors_five_nums.append(
            Fore.RED + Style.BRIGHT +
            "Error: The 5 numbers should be unique."
            )

    if errors_five_nums:
        """
        Print the errors, if any, and return False 
        indicating data is not valid
        """
        for num in errors_five_nums:
            print(num)
        print("\n" + Fore.YELLOW + "* Please try again!")
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
    print(f"{Fore.BLACK}{Back.YELLOW}Last draw date: {last_draw[0]}")

    winning_numbers_str = ""
    for number in last_draw[1:6]:
        winning_numbers_str += number + ' '
    print(f"{Fore.YELLOW}{Back.CYAN}Winning numbers: {winning_numbers_str}")

    winning_lucky_numbers_str = ""
    for number in last_draw[6:8]:
        winning_lucky_numbers_str += number + ' '
    print(
        f"{Fore.YELLOW}{Back.CYAN}Lucky numbers: {winning_lucky_numbers_str}"
        )
    print("\n")

    # Instructions
    print(f"{Back.YELLOW}{Fore.BLACK}Instructions:")
    print(
        f"{Back.CYAN}{Fore.YELLOW}Enter five numbers, strictly unique, " +
        "between 1 and 50."
        )
    print(f"{Back.CYAN}{Fore.YELLOW}with commas in between and no spaces.")
    print(f"{Back.CYAN}{Fore.YELLOW}Example: 7,45,34,23,49")
    print("\n")

    while True:
        # Get user input for Euro Millions ticket numbers
        lotto_data_five_nums = []
        data_str_five_nums = input(
            Fore.GREEN + Style.BRIGHT +
            "Enter your five numbers here (separated by commas): "
            )
        lotto_data_five_nums = data_str_five_nums.split(",")

        # Validate the user-entered data
        if validate_data(lotto_data_five_nums):
            print(Back.GREEN + Fore.WHITE + "Five numbers accepted!")
            break
        else:
            print(Fore.RED + Style.BRIGHT + "Error: Invalid data format.")

    while True:
        # Get user input for the 2 lucky numbers between 1 and 12
        lucky_numbers_str = input(
            Fore.GREEN + Style.BRIGHT +
            "Enter your two lucky numbers (separated by commas): "
            )

        # Check if the input contains spaces
        if " " in lucky_numbers_str:
            print(
                Fore.RED + Style.BRIGHT +
                "Error: Spaces are not allowed. " +
                "Please re-enter lucky numbers without spaces."
                )
            continue

        # Remove spaces from the input string
        lucky_numbers_str = lucky_numbers_str.replace(" ", "")

        # Split the input by commas
        lucky_numbers = lucky_numbers_str.split(",")

        # Validate the user-entered data for lucky numbers
        try:
            lucky_numbers = [int(num) for num in lucky_numbers]
            if all(
                1 <= num <= 12 for num in lucky_numbers
                    ) and len(lucky_numbers) == 2:
                # Check if lucky_numbers are unique
                if len(set(lucky_numbers)) == 2:
                    print(Back.GREEN + Fore.WHITE + "Lucky numbers accepted!")
                    break
                else:
                    print(
                        Fore.RED + Style.BRIGHT +
                        "Error: Lucky numbers should " +
                        "be two unique integers between 1 and 12."
                        )
            else:
                print(
                    Fore.RED + Style.BRIGHT +
                    "Error: Lucky numbers should be two integers " +
                    "between 1 and 12."
                    )
        except ValueError:
            print(
                Fore.RED + Style.BRIGHT +
                "Error: Please enter only two " +
                "integers for lucky numbers."
                )

    """
    Combine lotto_data_five_nums and lucky_numbers into a single list
    with a comma in between and sort the numbers in ascending order
    """
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

    except Exception as e:
        print(
            Fore.RED +
            "An error occurred while pushing data to the 'user' workbook:"
            )
        print(e)


def play_lottorama_game():
    while True:
        # Main program execution starts here
        print(
            "\n" + Back.YELLOW + Fore.BLACK + Style.BRIGHT +
            "Welcome to Lottorama!"
            )
        print(
            Fore.YELLOW + Back.CYAN +
            "Let us try predicting the next Euro Millions jackpot."
            )
        print(
            "\n" +
            Fore.MAGENTA + Style.BRIGHT + "Gathering data! Please wait... \n"
            )

        while True:
            # Get user-entered Euro Millions ticket numbers
            lotto_data = user_lotto_data()

            # Push the data to the 'user' workbook if it is valid
            push_to_user_workbook(lotto_data)

            # Delay execution by 5 seconds to allow workbook updates
            print(
                Fore.MAGENTA + Style.BRIGHT +
                "\nGathering data! Please wait 5 seconds..."
                )
            time.sleep(5)

            # Get user numbers lotto_data_five_nums and lucky_numbers
            user_ranking = SHEET.worksheet("user-ranking").get_all_values()

            # split into three sublist before creating a table
            numbers_row = user_ranking[0]
            num_list = numbers_row[1:6]
            num_lucky = numbers_row[6:8]
            lucky_list = [num_lucky]

            rankings_row = user_ranking[-1]
            rank_list = rankings_row[1:6]
            rank_lucky = rankings_row[6:8]

            # Print about table
            print(
                Fore.YELLOW +
                "\nThe below table provides info on repeat wins on\n" +
                "each of your numbers from previous all-time draws."
                )

            """
            Add blank values to num_lucky and rank_lucky to match 
            the length of num_list otherwise this lacing to 
            shortest by default
            """
            num_lucky += [""] * (len(num_list) - len(num_lucky))
            rank_lucky += [""] * (len(num_list) - len(rank_lucky))

            # Create a 2D list with each element in a separate row
            data = []
            for i in range(len(num_list)):
                data.append(
                    [num_list[i], rank_list[i], num_lucky[i], rank_lucky[i]]
                    )

            # Print the table
            headers = ["Numbers", "Wins", "Lucky Numbers", "Wins"]
            print(tabulate(data, headers=headers, tablefmt="pretty"))

            # Convert lists to integers and transpose the results
            num_list = [int(num) for num in num_list]
            rank_list = [int(rank) for rank in rank_list]
            transpose_nums = list(zip(num_list, rank_list))

            lucky_list = [int(num) for num in numbers_row[6:8]]
            rank_lucky = [int(rank) for rank in rankings_row[6:8]]
            transpose_lucky = list(zip(lucky_list, rank_lucky))

            """
            Filter out the pairs by index 1 and store
            the corresponding index 0 numbers
            """
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

            # Count the length of these lists
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

            """
            Count the numbers that are greater than or equal to 5
            Count the numbers that are equal to 4
            Count the numbers that are less than or equal to 3
            """
            popular_lucky_nums = []
            moderately_popular_lucky_nums = []
            least_popular_lucky_nums = []

            try:
                for pair in transpose_lucky:
                    if pair[1] >= 7:
                        popular_lucky_nums.append(pair[0])
                    elif pair[1] == 6:
                        moderately_popular_lucky_nums.append(pair[0])
                    elif pair[1] <= 5:
                        least_popular_lucky_nums.append(pair[0])
            except IndexError:
                pass
            
            count_popular_lucky = len(popular_lucky_nums)
            count_moderately_popular_lucky = len(moderately_popular_lucky_nums)
            count_least_popular_lucky = len(least_popular_lucky_nums)

            if count_least_popular_lucky == 1:
                clpl_numbers = "number"
            else:
                clpl_numbers = "numbers"

            if count_moderately_popular_lucky == 1:
                cmpl_numbers = "number"
            else:
                cmpl_numbers = "numbers"

            if count_popular_lucky == 1:
                cpl_numbers = "number"
            else:
                cpl_numbers = "numbers"
                            
            # Summary of winning numbers
            print()
            print("Table Summary:")
            print(f"You have {count_popular} {cp_numbers} {popular_numbers} \
listed in the most popular winning numbers.")
            print(f"You have {count_moderately_popular} {cmp_numbers} \
{moderately_popular_numbers} listed in the moderately popular winning numbers.")
            print(f"You have {count_least_popular} {clp_numbers} \
{least_popular_numbers} listed in the least popular winning numbers.")
            print()
            # Summary of lucky winning numbers
            print(f"You have {count_popular_lucky} {cpl_numbers} \
{popular_lucky_nums} listed in the most popular lucky winning numbers.")
            print(f"You have {count_moderately_popular_lucky} {cmpl_numbers} \
{moderately_popular_lucky_nums} listed in the moderately popular lucky winning numbers.")
            print(f"You have {count_least_popular_lucky} {clpl_numbers} \
{least_popular_lucky_nums} listed in the least popular winning numbers.")
            
            # Prompt for user's choice to quit or modify
            print()
            print("Now that you have statistics about your numbers,")

            while True:
                user_input = input("Enter 'Q' to quit, 'M' to modify or 'R' to start allover! ")
                print()
                # Validate user input for quit, modify, or repeat
                user_input_lower = user_input.lower()
                if user_input_lower == 'q':
                    print("Good Luck Winning the Euro Millions!")
                    return  # Exit the function and terminate the game
                elif user_input_lower == 'm':
                    while True:
                        preferred_numbers_input = input("From your chosen numbers "
                                                        f"{num_list}\n"
                                                        "Enter two to keep, separated by commas and we will predict the remaining three: ")
                        
                        # Validate user input for preferred numbers
                        preferred_numbers = preferred_numbers_input.split(',')
                        preferred_numbers = [
                            num.strip() for num in preferred_numbers
                            ]

                        # Check if there are any empty values between commas
                        preferred_numbers = preferred_numbers_input.split(',')
                        if any(num == '' for num in preferred_numbers):
                            print("Error: Empty values between commas are not allowed.")
                            continue

                        elif len(preferred_numbers) != len(set(preferred_numbers)):
                            print("Error: Preferred numbers must be unique.")
                            continue

                        # Check if the input contains only numbers from the original list
                        valid_numbers = set(map(str, num_list))
                        if all(num in valid_numbers for num in preferred_numbers) and len(preferred_numbers) == 2:
                            print("Thank you for modifying your preferred numbers!")

                            # get the 50 lotto numbers and their rankings
                            num_ranks = SHEET.worksheet("num-ranks").get_all_values()
                            all_nums = num_ranks[0]
                            all_num_stats = num_ranks[1]

                            # Convert lists to integers and transpose the results
                            all_nums = [int(num) for num in all_nums]
                            all_num_stats = [int(rank) for rank in all_num_stats]
                            transpose_all_nums = list(zip(all_nums, all_num_stats))

                            high_ranks = []
                            moderate_ranks = []
                            least_ranks = []

                            try:
                                for pair in transpose_all_nums:
                                    if pair[1] >= 5:
                                        high_ranks.append(pair[0])
                                    elif pair[1] == 4:
                                        moderate_ranks.append(pair[0])
                                    elif pair[1] <= 3:
                                        least_ranks.append(pair[0])
                            except IndexError:
                                pass

                            print()
                            print(
                                f"All time repeat winning numbers are: {high_ranks}"
                                )

                            # Convert preferred_numbers to a set
                            preferred_numbers_set = set(int(num) for num in preferred_numbers)

                            """
                            Pick 2 random numbers from high ranking and 
                            1 random number from moderate ranking listed 
                            imported from Google sheets
                            """
                            available_numbers_high_ranks = [num for num in high_ranks if num not in preferred_numbers_set]
                            random_numbers_high_ranks = random.sample(available_numbers_high_ranks, 2)

                            available_numbers_moderate_ranks = [num for num in moderate_ranks if num not in preferred_numbers_set and num not in random_numbers_high_ranks]

                            """
                            Ensure that random_number_moderate_ranks is None 
                            if available_numbers_moderate_ranks is empty
                            """
                            random_number_moderate_ranks = random.choice(available_numbers_moderate_ranks) if available_numbers_moderate_ranks else None

                            # Combine all five numbers into a list named initial_predicted_numbers
                            initial_predicted_numbers = preferred_numbers + random_numbers_high_ranks
                            if random_number_moderate_ranks is not None:
                                initial_predicted_numbers.append(random_number_moderate_ranks)

                            # Convert all elements to integers using list comprehension
                            predicted_numbers = [int(num) for num in initial_predicted_numbers]
                            #Sort predicted numbers
                            sorted_predicted_numbers = sorted(predicted_numbers)
                            print(f"Your Predicted winning numbers are: {sorted_predicted_numbers}")
                            print("This version of the App does not provide predictions for lucky numbers.")
                            
                            # Prompt for user's choice to play again
                            print()
                            play_again_input = input("Do you wish to play again? Enter Y for yes and N for no: ")

                            # Convert user input to lowercase for case insensitivity
                            play_again_input_lower = play_again_input.lower()

                            if play_again_input_lower == 'n':
                                print("Good bye! And Good luck winning the Euro Millions.")
                                return  # Exit the main loop if the user chooses not to play again

                            elif play_again_input_lower != 'y':
                                print("Invalid input. Please enter Y for yes or N for no.")
                            else:
                                print("Starting a new game...")
                                break

                        else:
                            print("Error: Enter exactly two preferred numbers separated by commas "
                                "from the above list.")
                    break
                    
                elif user_input_lower == 'r':
                    print("Starting a new game...")
                    break
                else:
                    print(Fore.RED + Style.BRIGHT + "Error: Invalid input.")
        continue


if __name__ == "__main__":
    play_lottorama_game()