class Candidate:
    def __init__(self, name):
        self.name = name
        self.votes = 0

    def get_name(self):
        return self.name

    def get_vote_count(self):
        return self.votes

    def add_vote(self):
        self.votes += 1

    def reset(self):
        self.votes = 0
