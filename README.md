# Lottorama - Lottery Prediction and Analysis Tool

Lottorama is a Python-based tool that helps users analyee historical lottery data and make predictions for future lottery numbers. Lottorama interacts with a Google Sheets document to provide insights into winning numbers, frequency of occurrence, and offers users the option to modify and predict their own numbers for upcoming draws.

**[Live site](https://lottorama-d338fc131061.herokuapp.com/)**

------------------------------------------------------------------

**[Repository](https://github.com/jjsemaan/lottorama/)**

------------------------------------------------------------------

## Features

1. The opportunity to get winning numbers of the most recent Euro Millions draw.
    - When the program is first run a welcome note is displayed followed by the latest winning numbers and app usage instructions.

![Welcome](Docs/welcome.png)

2. Validates user-entered Euro Millions ticket numbers.
    - Checks if numbers are whole numbers.
    - Checks if numbers are five in total for lotto and two in total for lucky numbers.
    - Checks if numbers are between 1 and 50 for lotto and between 1 and 12 for lucky numbers.
    - Checks if numbers are unique.
    - Checks for letters, spaces and / or multiple commas and returns error.

3. Displays statistics about the frequency of past wins for user-selected numbers.
    - Returns the number of times each number appeared in a winning draw.

![Statistics](Docs/stats.png)

4. Provides options to modify user-selected numbers and predict new combinations.

5. Generates predictions for future lottery numbers based on historical data.
    - Requests user to keep two numbers while app predicts the remaining three by collecting highest and moderate ranking numbers.
    - Then the app picks two numbers from highest ranking and one number from the moderate ranking collections.

![Prediction](Docs/predict.png)

6. Offers an interactive and user-friendly command-line interface.

7. Utilises Google Sheets API for data storage and retrieval.