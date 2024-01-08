import argparse
import os
from flask import Flask

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the root URL ("/")
@app.route('/')
def hello_world():
    return f"Hello world, from Flask!"

def main():
    parser = argparse.ArgumentParser(description='Simple Flask "Hello World" app with a customizable port.')
    parser.add_argument('-p', '--port', type=int, default=5000, help='Port number to run the app (default: 5000)')
    args = parser.parse_args()

    # Run the Flask app on the specified port
    app.run(port=args.port)

if __name__ == '__main__':
    main()
