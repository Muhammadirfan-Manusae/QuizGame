class Question:
    def __init__(self, text, choices, correct_index, points):
        self.text = text
        self.choices = choices
        self.correct_index = correct_index
        self.points = points

    def is_correct(self, choice_index):
        return choice_index == self.correct_index
