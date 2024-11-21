from flask import Flask, jsonify, render_template
from poem_generator.poem import generate_poem
from flask_cors import CORS

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app)

print("TEMPLATE PATH!", app.static_folder)

@app.route("/")
def poem_website():
    return render_template("index.html")

@app.route("/generate-poem", methods=["GET"])
def generate_poem_route():
    print("called generate poem")
    poem = generate_poem()
    print("poem generated!")
    return jsonify(poem.jsonify_sentences())

if __name__ == '__main__':
    app.run(debug=True)