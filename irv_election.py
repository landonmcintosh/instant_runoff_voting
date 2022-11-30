# Landon McIntosh
# 2022
# IRV VOTING SOFTWARE

from election import Election
from candidate import Candidate
from ballot import Ballot

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

from datetime import date

import csv


def main():
    global report
    current = True
    candidate_count = 0
    election_status = 0
    winner = ''
    report = False

    # for report
    today = date.today()

    while current:
        print()
        print('-'*50)
        print()
        print()
        print('Welcome to IRV Election')
        print('Created by Landon McIntosh')
        print()
        print('select (1) for Instant Runoff Voting Tabulation \n'
              'select (2) to Read Instructions')
        print()
        print()
        print('-'*50)
        menu_selection = int(input('Select: '))
        if menu_selection == 1:
            election_name = input('Election Name: ')
            election = Election(election_name)
            print()

            print()
            csv_file = input('CSV File Name: ') + '.csv'
            print('-' * 50)

            # IMPORT BALLOTS CSV
            with open(csv_file, mode='r') as current_file:
                csv_reader = csv.reader(current_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    elif line_count == 1:
                        # DEFINES CANDIDATES
                        cur_can = 0
                        current_adding_vote = []
                        for cell in range(len(row)):
                            election.add_candidate(Candidate(row[cur_can]))
                            cur_can += 1
                            candidate_count += 1

                            # ADD BALLOT FOR LINE 1
                            current_adding_vote.append(row[cell])
                        election.add_ballot(Ballot(current_adding_vote))
                        line_count += 1
                    else:
                        # ADDS BALLOT FOR EACH LINE
                        current_adding_vote = []
                        for i in range(len(row)):
                            current_adding_vote.append(row[i])
                        election.add_ballot(Ballot(current_adding_vote))
                        line_count += 1

            # allows exhausted option by adding it to end of all ballots
            for ballot in election.get_ballots():
                ballot.set_exhausted()

            print(f'Processed {line_count-1} ballots.')



            election_status += 1

            print()

            # tabulation of ballots
            print('Tabulating Ballots...')

            current_round_ballot_bank = []
            for ballot in election.get_ballots(): # adds current vote to ballot bank for each ballot
                current_round_ballot_bank.append(ballot.cur_irv_vote())

            for vote in current_round_ballot_bank:
                for candidate in election.get_candidates():  # adds vote to candidate count
                    if vote == candidate.get_name():
                        candidate.add_vote()
                        election.cast_r1_vote()
                        break

            election_status += 1

            print()
            print('-' * 50)
            print(f'{election.get_name()} Results')
            print('-' * 50)
            print('-' * 50)
            print(f'{election.total_votes_cast()} votes cast')
            print(f'{election.total_votes_cast()} votes cast')
            print('-' * 50)
            print('-' * 50)

            # text file for use in report generation
            with open(f'{election.get_name()}_election.txt', 'w') as txtfile:

                txtfile.write(f'{election.get_name()} Results \n\n')
                txtfile.write(f'Processed {line_count - 1} ballots.\n')
                txtfile.write(f'{election.total_votes_cast()} votes cast\n')
                txtfile.write(f'{election.total_votes_cast()} votes cast\n')
                txtfile.write('ROUND 1 RESULTS\n')
                txtfile.write('-' * 50)
                txtfile.write('\n')
                txtfile.write(f'{"candidate":12} | {"votes":5} | {"pct":4}\n')
                txtfile.write('-' * 50)
                txtfile.write('\n')

            print('ROUND 1 RESULTS')
            print('-' * 50)

            print(f'{"candidate":12} | {"votes":5} | {"pct":4}')
            print('-' * 50)
            for candidate in election.get_candidates():
                print(f'{candidate.get_name():12} | {candidate.get_vote_count():5} |'
                      f' {(candidate.get_vote_count() / election.total_votes_cast()*100):4} %')
                with open(f'{election.get_name()}_election.txt', 'a') as txtfile:
                    txtfile.write(f'{candidate.get_name():12} | {candidate.get_vote_count():5} |'
                          f' {(candidate.get_vote_count() / election.total_votes_cast()*100):4} %\n')

                if candidate.get_vote_count() >= election.majority_thresh():  # checks for winner
                    winner = candidate.get_name()
                    winning_votes = candidate.get_vote_count()
                    election_status = 4
            print('-' * 50)
            if election_status == 4:  # if winner determined, finalizes election
                print('A WINNER HAS BEEN DETERMINED')
                print('-' * 50)
                print(f'{winner} has won the {election.get_name()} election.')
                print(f'{winner} received {winning_votes} votes out of {election.total_votes_cast()} votes cast, \n'
                      f'reaching the majority threshold of {election.majority_thresh()} votes.')
                print(f'{winner} received {winning_votes / election.total_votes_cast() * 100:4}% of votes cast.')
                print('-' * 50)
                current = False

                # for report
                with open(f'{election.get_name()}_election.txt', 'a') as txtfile:
                    txtfile.write('Winner Determined in Round 1\n')
                    txtfile.write(f'{winner} has won the {election.get_name()} election.\n')
                    txtfile.write(f'{winner} received {winning_votes} votes out of {election.total_votes_cast()} votes cast, \n'
                          f'reaching the majority threshold of {election.majority_thresh()} votes.\n')
                    txtfile.write(f'{winner} received {winning_votes / election.total_votes_cast() * 100:4}% of votes cast.\n')
                    txtfile.write('\n\n')
            else:
                print('-' * 50)
                runoff = True
                cur_round = 2
                eliminated_cands = []
                while runoff:

                    election.clear_vote()
                    election.reset_exhausted()

                    for candidate in election.determine_min():
                        eliminated_cands.append(candidate.get_name())

                    # reset totals
                    for candidate in election.get_candidates():
                        candidate.reset()

                    # TABULATION RUNOFF
                    current_round_ballot_bank = []
                    for ballot in election.get_ballots():

                        while ballot.cur_irv_vote() in eliminated_cands:
                            ballot.ballot_status_up()

                        while ballot.cur_irv_vote() == '':
                            ballot.ballot_status_up()

                        if ballot.cur_irv_vote() == 'Exhausted':
                            election.add_exhausted()
                        else:
                            current_round_ballot_bank.append(ballot.cur_irv_vote())

                    for vote in current_round_ballot_bank:
                        for candidate in election.get_candidates():
                            if vote == candidate.get_name():
                                candidate.add_vote()
                                election.cast_vote()

                    ### RECYCLE

                    print(f'ROUND {cur_round} RESULTS')
                    print('-' * 50)
                    print('-' * 50)
                    print(f'{election.total_votes_cast()} ballots counted')
                    print(f'{election.get_exhausted()} ballots exhausted')
                    print(f'{election.majority_thresh()} votes needed for majority')
                    print('-' * 50)
                    print(f'{"candidate":12} | {"votes":5} | {"pct":4}')
                    print('-' * 50)

                    # for report
                    with open(f'{election.get_name()}_election.txt', 'a') as txtfile:
                        txtfile.write(f'ROUND {cur_round} RESULTS\n')
                        txtfile.write(f'{election.total_votes_cast()} ballots counted\n')
                        txtfile.write(f'{election.get_exhausted()} ballots exhausted\n')
                        txtfile.write(f'{election.majority_thresh()} votes needed for majority\n')
                        txtfile.write(f'{"candidate":12} | {"votes":5} | {"pct":4}\n')
                        txtfile.write('-' * 50)
                        txtfile.write('\n')

                    for candidate in election.get_candidates():
                        print(
                            f'{candidate.get_name():12} | {candidate.get_vote_count():5} | '
                            f'{(candidate.get_vote_count() / (election.total_votes_cast()) * 100):4} %')
                        with open(f'{election.get_name()}_election.txt', 'a') as txtfile:
                                txtfile.write(f'{candidate.get_name():12} | {candidate.get_vote_count():5} | '
                                f'{(candidate.get_vote_count() / (election.total_votes_cast()) * 100):4} %\n')

                        if candidate.get_vote_count() >= election.majority_thresh():
                            winner = candidate.get_name()
                            winning_votes = candidate.get_vote_count()
                            election_status = 4
                    print('-' * 50)
                    if election_status == 4:
                        print('A WINNER HAS BEEN DETERMINED')
                        print('-' * 50)
                        print(f'{winner} has won the {election.get_name()} election.')
                        print(f'{winner} received {winning_votes} votes out of \n'
                              f'{election.total_votes_cast()} votes counted in the final round, \n'
                              f'reaching the majority threshold of {election.majority_thresh()} votes.')
                        print(
                            f'{winner} received {(winning_votes / election.total_votes_cast() * 100):4}% of votes counted.')
                        print('-' * 50)
                        print(
                            f'{election.get_original_votes()} ballots cast, {election.get_exhausted()} ballots exhausted.')
                        print(
                            f'{winner} received {(winning_votes / election.get_original_votes() * 100):4}% of votes cast')
                        print('-' * 50)
                        print('Thank you for using IRV Election - Landon McIntosh')
                        print('-' * 50)

                        # for report
                        with open(f'{election.get_name()}_election.txt', 'a') as txtfile:
                            txtfile.write(f'A winner has been dermined in round {cur_round}.\n')
                            txtfile.write('-' * 50)
                            txtfile.write('\n')
                            txtfile.write(f'{winner} has won the {election.get_name()} election.\n')
                            txtfile.write(f'{winner} received {winning_votes} votes out of \n'
                                  f'{election.total_votes_cast()} votes counted in the final round, \n'
                                  f'reaching the majority threshold of {election.majority_thresh()} votes.\n')
                            txtfile.write(
                                f'{winner} received {(winning_votes / election.total_votes_cast() * 100):4}% of votes counted.\n')
                            txtfile.write('-' * 50)
                            txtfile.write('\n')
                            txtfile.write(
                                f'{election.get_original_votes()} ballots cast, {election.get_exhausted()} ballots exhausted.\n')
                            txtfile.write(
                                f'{winner} received {(winning_votes / election.get_original_votes() * 100):4}% of votes cast\n')
                            txtfile.write('-' * 50)
                            txtfile.write('\n')
                            txtfile.write('Thank you for using IRV Election - Landon McIntosh')

                        runoff = False
                        current = False
                        report = True
                    else:
                        cur_round += 1

        elif menu_selection == 2:
            print()
            print('-'*50)
            print()
            print('Instructions')
            print('This program tabulates/canvasses Instant Runoff-Voting Votes')
            print('To create the proper .csv input, follow these steps: \n\n'
                  '1. Create a Spreadsheet with a header row with preferences \n'
                  '\t example: 1st pref | 2nd pref | 3rd pref etc... \n'
                  '\n'
                  '2. In each row, enter a voters choices, matching with the prefs. \n\n'
                  '3. Export the spreadsheet as a .csv and upload to the program!\n\n'
                  'Notes: Each appearance of each candidate\'s name must be identical\n'
                  '\t for example "Joe" and "joe" would not be counted as the same candidate.\n\n'
                  '\tThe second CSV line (first ballot) must rank all candidates.\n\n'
                  '\tWhen typing in a file name, omit ".csv" ')
            print('-'*50)
            print('IMPORTANT: for IRV to output a pdf document, please execute this command in terminal once:\n'
                  'python3 -m pip install reportlab')

            print()

        while report:
            print('-'*50)
            print()
            print()
            print('Welcome to IRV Election Report Generation')
            print()
            current2 = True

            while current2:
                print('Select (G) to Generate a PDF Election Report')
                print('Select (Q) to Quit')
                rep_select = str(input('Make a Selection: '))
                if rep_select == 'g' or rep_select =='G':
                    print('Generating Report')
                    print(f'file name: {election.get_name()}_election_report.pdf added to drive.')
                    election_report = canvas.Canvas(f'{election.get_name()}_election_report.pdf', pagesize=letter)
                    width, height = letter  # keep for later
                    election_report.setFont('Helvetica', 16)
                    election_report.drawString(60, height - 100, f'Election Report: {election.get_name()}')
                    election_report.setFont('Helvetica', 12)
                    election_report.drawString(400, height-100, f'Generated on {today.strftime("%B %d, %Y")}')

                    with open(f'{election.get_name()}_election.txt', "r") as estxt:
                        lines = estxt.readlines()

                    curset = 14
                    sset = 60

                    for line in lines:
                        if curset >= 46 * 14:
                            curset = 14
                            sset = 300
                        election_report.drawString(sset, height - (100 + curset), line)
                        curset += 14
                    election_report.save()
                    current2 = False
                    report = False

                elif rep_select =='q' or rep_select =='Q':
                    current2 = False
                    report = False


if __name__ == '__main__':
    main()
