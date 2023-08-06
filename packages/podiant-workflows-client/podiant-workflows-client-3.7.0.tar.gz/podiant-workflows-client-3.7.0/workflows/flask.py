from flask import Flask
from workflows.logging import setup_logging
from workflows.views import endpoint


app = Flask(__name__)
app.route('/', methods=['POST'])(endpoint)
setup_logging(app=app)
