"""
Insta485 index (main) view.

URLs include:
/
"""
import json
import flask
import requests
import search


# Show Index
@search.app.route('/', methods=['GET'])
def show_index():
    """Show the Index page."""
    print("reading in")
    connection = search.model.get_db()
    weight = flask.request.args.get("w", default="", type=str)
    query = flask.request.args.get("q", default="", type=str)
    weight = weight.strip()
    query = query.strip()

    if query.isspace():
        context = {"results": []}
        return flask.render_template("index.html", **context)

    if weight != "":
        # "http://localhost:8001/api/v1/hits/?q="
        baseurl = search.app.config["INDEX_API_URL"]
        baseurl = baseurl + "?q="
        print("query is ", query)
        if " " in query:
            query = query.replace(" ", "+")
        url = baseurl + str(query) + "&w=" + str(weight)
        url.strip()
        print("url is " + url)
        context = requests.get(url).json()
        print("Context: ")
        print(json.dumps(context, indent=4))
        hits = context["hits"]
        hit_list = []
        count = 0
        for key in hits:
            if count == 10:
                break
            hit_list.append(key["docid"])
            count += 1

        # print("hit_list ", hit_list)

        cur = connection.execute(
            "SELECT docid, title, summary "
            "FROM Documents "
        )
        docs = cur.fetchall()

        final_hits = []
        for hit in hit_list:
            for doc in docs:
                if doc["docid"] == hit:
                    if not doc["summary"]:
                        doc["summary"] = "No summary available"
                    doc["title"] = doc["title"].lstrip()
                    final_hits.append(doc)

        print("final hits: ", json.dumps(final_hits, indent=4))
        context = {"results": final_hits}

        return flask.render_template("index.html", **context)

    context = {"search_results": False}
    return flask.render_template("index.html", **context)

# Show User
# OH questions:
    # how to start the server/setup
    # url's for index and search
    # search interface walkthrough
