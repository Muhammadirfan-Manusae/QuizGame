from flask import Flask, render_template, request, redirect, session, url_for
from models.game_manager import GameManager
import time
import os
import json

app = Flask(__name__)
app.secret_key = 'quiz-secret'

gm = GameManager("questions.json")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_name = request.form['player_name']
        gm.set_player(player_name)
        session['player_name'] = player_name
        session['score'] = 0
        session['index'] = 0
        session['start_time'] = time.time()
        session['answers'] = []
        return redirect(url_for('question'))
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    index = session.get('index', 0)
    if index >= len(gm.questions):
        return redirect(url_for('result'))

    question = gm.questions[index]

    if request.method == 'POST':
        selected = int(request.form['choice'])
        correct = question.is_correct(selected)
        if correct:
            session['score'] += question.points

        session['answers'].append({
            'text': question.text,
            'choices': question.choices,
            'correct_index': question.correct_index,
            'selected': selected
        })

        session['index'] += 1
        return redirect(url_for('question'))

    return render_template('question.html', question=question, index=index + 1, total=len(gm.questions))

@app.route('/result')
def result():
    name = session.get('player_name', 'ผู้เล่น')
    score = session.get('score', 0)
    answers = session.get('answers', [])
    end_time = time.time()
    duration = round(end_time - session.get('start_time', end_time), 2)

    update_leaderboard(name, score, duration)
    leaderboard = load_leaderboard()

    return render_template('result.html', name=name, score=score, duration=duration, answers=answers, leaderboard=leaderboard)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', leaderboard=load_leaderboard())

def update_leaderboard(name, score, duration):
    path = "leaderboard.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    data.append({'name': name, 'score': score, 'time': duration})
    data = sorted(data, key=lambda x: (-x['score'], x['time']))[:10]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_leaderboard():
    if os.path.exists('leaderboard.json'):
        with open('leaderboard.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

if __name__ == '__main__':
    app.run(debug=True)
