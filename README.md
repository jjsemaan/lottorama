# Lottorama - Lottery Prediction and Analysis Tool

Lottorama is a Python-based tool that helps users analyee historical lottery data and make predictions for future lottery numbers. Lottorama interacts with a Google Sheets document to provide insights into winning numbers, frequency of occurrence, and offers users the option to modify and predict their own numbers for upcoming draws.

**[Live site](https://lottorama-d338fc131061.herokuapp.com/)**

------------------------------------------------------------------

**[Repository](https://github.com/jjsemaan/lottorama/)**

------------------------------------------------------------------

## Features

1. The opportunity to get winning numbers of the most recent Euro Millions draw.
    - When the program is first run a welcome note is displayed followed by the latest winning numbers and app usage instructions.

![Welcome](assets/images/welcome.png)

2. Validates user-entered Euro Millions ticket numbers.
    - Checks if numbers are whole numbers.
    - Checks if numbers are five in total for lotto and two in total for lucky numbers.
    - Checks if numbers are between 1 and 50 for lotto and between 1 and 12 for lucky numbers.
    - Checks if numbers are unique.
    - Checks for letters, spaces and / or multiple commas and returns error.

3. Displays statistics about the frequency of past wins for user-selected numbers.
    - Returns the number of times each number appeared in a winning draw.

![Statistics](assets/images/stats.png)

4. Provides options to modify user-selected numbers and predict new combinations.

5. Generates predictions for future lottery numbers based on historical data.
    - Requests user to keep two numbers while app predicts the remaining three by collecting highest and moderate ranking numbers.
    - Then the app picks two numbers from highest ranking and one number from the moderate ranking collections.

![Prediction](assets/images/predict.png)

6. Offers an interactive and user-friendly command-line interface.

7. Utilises Google Sheets API for data storage and retrieval.

------------------------------------------------------------------

## Technologies

* Python was used as the programming language to make the game.
* Microsoft Power Point was used to create the flow chart showing the game's logic.
* [GitHub](https://github.com/) has been used to store the code, images, and other content. 
* [Heroku](https://dashboard.heroku.com/apps) was used to deploy the game to the web.
* [Git](https://git-scm.com/) was used to track changes made to the project and to commit and push code to the repository.
* Python module [time](https://docs.python.org/3/library/time.html) was used to allow for a delay when acquiring data from Google Sheets. 
* Python module [random](https://docs.python.org/3/library/random.html) was used to select numbers from a list of highest ranking and moderate ranking numbers. 
* Python library [tabulate](https://pypi.org/project/tabulate/) was installed and used to create a table with analytics of winning numbers.
* Python library [colorama](https://pypi.org/project/colorama/) was installed and used to add colors to text throughout the app.
* Python library [gspread](https://pypi.org/project/gspread/) was installed and used to read, write and update data, and connect with Google Sheets API.