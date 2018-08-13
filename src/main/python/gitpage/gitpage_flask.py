
from flask import Flask, render_template
from services import Index

application = Flask(__name__, template_folder='gitpage/templates')
application.debug = True

service = Index()


def start_flask():
    application.run()


@application.route('/')
def index():
    return render_template('index.html', title=service.get_title())
