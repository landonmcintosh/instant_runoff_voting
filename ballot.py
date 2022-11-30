class Ballot:
    def __init__(self, vote, status=0):
        self.status = int(status)
        self.vote = vote

    def ballot_status_up(self):
        self.status += 1

    def get_ballot_status(self):
        return self.status

    def cur_irv_vote(self):
        return self.vote[self.status]

    def set_exhausted(self):
        self.vote.append('Exhausted')
