class Election:
    def __init__(self, office):
        self.office = office
        self.candidates = []
        self.ballot_bank = []
        self.votes_cast = 0
        self.current_sums = []
        self.exhausted = 0
        self.original_votes = 0

    def get_name(self):
        return self.office

    def get_candidates(self):
        return self.candidates

    def get_ballots(self):
        return self.ballot_bank

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def add_ballot(self, ballot):
        self.ballot_bank.append(ballot)

    def clear_vote(self):
        self.votes_cast = 0

    def cast_r1_vote(self):
        self.votes_cast += 1
        self.original_votes += 1

    def get_original_votes(self):
        return self.original_votes

    def cast_vote(self):
        self.votes_cast += 1

    def total_votes_cast(self):
        return self.votes_cast

    def majority_thresh(self):
        return self.votes_cast // 2 + 1

    def reset_sums(self):
        self.current_sums = []

    def reset_exhausted(self):
        self.exhausted = 0

    def add_exhausted(self):
        self.exhausted += 1

    def get_exhausted(self):
        return self.exhausted

    def determine_min(self):
        mins = []
        self.reset_sums()
        for candidate in self.candidates:
            if candidate.get_vote_count() > 0:
                self.current_sums.append(candidate.get_vote_count())
        cur_min = min(self.current_sums)
        for candidate in self.candidates:
            if candidate.get_vote_count() == cur_min:
                mins.append(candidate)
        return mins
