"""
Insta485 index (main) view.

URLs include:
/
"""
import pathlib
import flask
import search


# Show Index
@search.app.route('/', methods=['POST', 'GET'])
def show_index():
    """Show A Page."""

    if flask.request.method == 'POST':
        follow = str(flask.request.form.get("follow"))
        profname = str(flask.request.form.get("username"))
        unfollow = str(flask.request.form.get("unfollow"))
        # print(follow, unfollow, profname)
        # Follow Form
        if follow == "follow":
            print("HERE")
            connection.execute(
                "INSERT INTO following(username1, username2) "
                "VALUES(?, ?) ",
                (logname, profname, )
            )

        # Unfollow Form
        elif unfollow == "unfollow":
            print("HERE")
            connection.execute(
                "DELETE FROM following "
                "WHERE username1=? AND username2=? ",
                (logname, profname, )
            )
    
    # context = {"size": size, "page": page}
    # Get variable arguments
    return flask.render_template("index.html")

# Show User
