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
    now = datetime.datetime.now()
    players = stats.get_daily_starting_pitcher_stats(now.year, now.month, now.day)
    return render_template("index.html", players=players)


if __name__ == "__main__":
    app.run()
