from flask import Flask
from routes.main import main
from routes.distance import distance_page

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(distance_page)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")