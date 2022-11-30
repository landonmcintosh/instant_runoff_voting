# instant_runoff_voting
Upload a CSV file of ranked choice election results and receive instant round-by-round results and the option to generate a pdf.

<b>CSV File Format:</b>
1. Include Header row, suggested column headers: "First preference", "Second preference," etc. Header row contents do not matter but must exist.
2. Each row after the header row is a "ballot," with each cell containing the name of a candidate, in order of preference.
   EXAMPLE: John Doe, Michelle Smith, etc...
   SPECIAL NOTE: While ballots can contain any number of candidates from 1 up to the total amount of candidates in a race, the first ballot ,ust    contain the names of all candidates!
3. Each instance of a candidate name must be identical, so "john" and "John" would register as different candidates.

<b>Using the Program:</b>
1. Choose any name for the election
2. When entering the csv file name, omit ".csv"

<b> Test Ballots </b>
The testBallots folder contains 7 csv files that can be used to demonstrate the functionality of the software in different conditions.

<b><h3> How Does an Instant Runoff Voting Election (IRV) Work? </b></h2>
In an IRV election, a majority of votes is required to win, as opposed to a plurality.
For elections with more than 2 candidates, 1 candidate often fails to reach an absolute majority of votes.

By ranking candidates, voters' votes are transferred to another candidate after their preferred candidate is eliminated.
Voters may rank any number of candidates, ranging from 1 to the total number of candidates running. In the event that all of the candidates that a voter ranked are eliminated, their ballot is considered "exhausted" and is removed from tabulations, including in determining the majority threshold.

Ultimately, IRV elections ensure a candidate with majority support is elected and allows third-party candidates to run without worrying about drawing votes away from major party/leading candidates.



<b>A Note about the Generate PDF Functionality:</b>

PDF Functionality is not completely developed and can be improved upon. PDF can be maximum of 1 page, and this presents content restrictions in terms of how many rounds can be printed on the pdf, which varies with candidate count.

Also, make sure to have the reportlab python library installed for the PDF report generation, which can be done with the following command:
python3 -m pip install reportlab
