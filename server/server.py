from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open("./grouped_news.json") as f:
    data = json.load(f)

with open("./newsdata.json") as f:
    newsdata = list(json.load(f).values())


@app.route("/api/news_raw")
def gen_news_data():
    return newsdata


@app.route("/api/news")
def get_news():
    group_id = request.args.get("group")
    if group_id:
        # Return news object with the given group ID
        news_object = data[int(group_id) - 1]  # Implement this function to retrieve the news object by group ID
        if news_object:
            return news_object
        else:
            return f"No news object found with group ID {group_id}", 404
    else:
        # Return all news objects
        return data


if __name__ == "__main__":
    app.run(debug=True)
