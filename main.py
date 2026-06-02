import argparse

import flask_app

parser = argparse.ArgumentParser(
    prog='Rubik\'s Cube Solver Entry Point',
    description='Start the application'
)

parser.add_argument('-d', '--debug', action='store_true')
parser.add_argument('-p', '--port', type=int, default=5000)
parser.add_argument('-b', '--bind', action='store_true')
parser.add_argument('-a', '--app', type=str, default='flask_app')

if __name__ == '__main__':
    args = parser.parse_args()

    app = flask_app.create_app()
    app.run(debug=args.debug, port=args.port)

