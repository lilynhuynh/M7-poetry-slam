from flask import Flask, jsonify, render_template
from poem_generator.poem import generate_poem
from flask_cors import CORS

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app)

@app.route("/")
def poem_website():
    return render_template("index.html")

@app.route("/generate-poem", methods=["GET"])
def generate_poem_route():
    print("Called generate poem")
    poem = generate_poem()
    print("Poem generated!")
    return jsonify(poem.jsonify_sentences())

if __name__ == '__main__':
    app.run(debug=True)