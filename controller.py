from flask import Flask, render_template
import stats
import datetime
app = Flask(__name__)


@app.route("/")
def app_root():
    """
    Controller method for the application root.

    :return:
    """
    # TODO: pass in sort column, sort direction, and date
    now = datetime.datetime.now()
    players = stats.get_daily_starting_pitcher_stats(now.year, now.month, now.day)
    players.sort(key=lambda p: p.game_score, reverse=True)
    return render_template("index.html", players=players)


if __name__ == "__main__":
    app.run()
