from flask import Flask, render_template
from threading import Thread

app = Flask('')


@app.route('/')
def index():
  return "Your bot is ready"


def run():
  app.run(host='0.0.0.0', port=80)


def keep_alive():
  server = Thread(target=run)
  server.start()
