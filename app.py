from flask import Flask, render_template, request, redirect, url_for
import random
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

app = Flask(__name__)

user_score = 0
comp_score = 0
ties = 0

@app.route("/", methods=["GET", "POST"])
def home():
    global user_score, comp_score, ties
    result = ""
    user_choice = ""
    comp_choice = ""
    winner = ""

    if request.method == "POST":
        if "reset" in request.form:
            user_score = 0
            comp_score = 0
            ties = 0
        else:
            user_choice = request.form["choice"]
            comp_choice = random.choice(["rock", "paper", "scissors"])

            if user_choice == comp_choice:
                result = "😐 It's a Tie!"
                ties += 1
            elif (user_choice == "rock" and comp_choice == "scissors") or \
                 (user_choice == "paper" and comp_choice == "rock") or \
                 (user_choice == "scissors" and comp_choice == "paper"):
                result = "✅ You Win!"
                user_score += 1
            else:
                result = "❌ Computer Wins!"
                comp_score += 1

        if user_score == 3:
            winner = "🏆 You Won the Game!"
        elif comp_score == 3:
            winner = "💻 Computer Won the Game!"

    return render_template("index.html",
                           result=result,
                           user_choice=user_choice,
                           comp_choice=comp_choice,
                           user_score=user_score,
                           comp_score=comp_score,
                           winner=winner)

@app.route("/stats")
def stats():
    labels = ["You", "Computer", "Ties"]
    values = [user_score, comp_score, ties]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Game Statistics")
    plt.savefig("static/stats.png")
    plt.close()

    return render_template("stats.html")

if __name__ == "__main__":
    app.run(debug=True)