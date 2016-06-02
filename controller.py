from flask import Flask, render_template, abort, request
import stats
import datetime

app = Flask(__name__)
_sort_col_lookup = {'game_score': lambda p: p.game_score,
                    'name': lambda p: p.name_display_first_last,
                    'ip': lambda p: p.out / 3,
                    'h': lambda p: p.h,
                    'r': lambda p: p.r,
                    'er': lambda p: p.er,
                    'bb': lambda p: p.bb,
                    'so': lambda p: p.so}


@app.route("/", methods=['GET'])
def app_root():
    """
    Controller method for the application root.

    :return:
    """
    now = datetime.datetime.now()
    return get_stats(now.year, now.month, now.day)


@app.route("/<int:year>/<int:month>/<int:day>", methods=['GET'])
def get_stats(year=0, month=0, day=0):
    """
    Controller method to fetch the stats page for a given date.

    :return:
    """
    try:
        date = datetime.datetime(year=year, month=month, day=day)
    except ValueError:
        abort(404)

    sort_col = request.args.get('sort_col', default='game_score')
    if not _sort_col_lookup[sort_col]:
        abort(404)

    reverse = request.args.get('reverse', default=True)
    page = request.args.get('page', default=0, type=int)
    if page < 0:
        abort(404)

    page_size = request.args.get('page_size', default=50, type=int)
    if page_size < 0 or page_size > 100:
        abort(404)
    # end validation

    players = _get_game_scores(date, sort_col, reverse, page, page_size)
    return render_template("index.html", players=players)


def _get_game_scores(date, sort_col='game_score', reverse=True, page=0, page_size=50):
    """
    Gets the game scores per pitcher.

    :param date: Date to fetch game scores for
    :param sort_col: Which stat to sort on
    :param reverse: Whether to reverse the sort order
    :param page: Which page of game scores to fetch
    :param page_size: Size of the page to fetch
    :return: game scores
    """
    players = stats.get_daily_starting_pitcher_stats(date.year, date.month, date.day)
    if len(players) is 0:
        return players

    # secondary sort by name, so our sorts are always deterministic
    players = sorted(players, key=lambda p: p.name_display_first_last)

    # sort by requested column
    # TODO: validate the sort_col is legit
    players = sorted(players, key=_sort_col_lookup[sort_col], reverse=reverse)

    # TODO: validate the page bounds
    page_start = page * page_size
    page_end = page_start + page_size
    return players[page_start:page_end]


if __name__ == "__main__":
    app.run()
