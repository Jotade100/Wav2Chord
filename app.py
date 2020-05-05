from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def main():
   return render_template('index.html', texto="HOLA")

@app.route("/processAudio/", methods=["POST"])
def procesarAudio():
   return render_template('index.html', texto="HOLA")

if __name__ == "__main__":
    app.run(debug=True)