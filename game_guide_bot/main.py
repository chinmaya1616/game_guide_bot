from flask import Flask, render_template, request
import requests

app = Flask(__name__,template_folder='template')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    game_name = request.form.get("game_name")
    if not game_name:
        return render_template("result.html", error="Please enter a game name.")

    # Fetch game details
    game_data = get_game_info(game_name)
    if not game_data:
        return render_template("result.html", error="Sorry, no information found for this game.")

    return render_template("result.html", game=game_name, info=game_data)


def get_game_info(game_name):
    """
    Fetch game details using the Wikipedia API.
    """
    try:
        # Wikipedia API request
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{game_name}")
        if response.status_code == 200:
            data = response.json()
            return {
                "title": data.get("title", game_name),
                "description": data.get("extract", "No detailed information available."),
                "image": data.get("thumbnail", {}).get("source", None)
            }
    except Exception as e:
        print(f"Error fetching game info: {e}")
    return None


if __name__ == "__main__":
    app.run(debug=True)