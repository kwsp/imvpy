#!/usr/bin/env python3
import argparse

from imv.main import app

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="0.0.0.0", help="Server host")
parser.add_argument("--port", type=int, default=7070, help="Server port")
parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
args = parser.parse_args()

print(args)

app.run(debug=args.debug, host=args.host, port=args.port)
