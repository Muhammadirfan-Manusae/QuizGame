import json
from .question import Question
from .player import Player

class GameManager:
    def __init__(self, question_file):
        self.questions = self.load_questions(question_file)
        self.player = None

    def set_player(self, name):
        self.player = Player(name)

    def load_questions(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Question(q['question'], q['choices'], q['correct_index'], q.get('points', 1)) for q in data]
