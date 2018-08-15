
from flask import Flask, render_template
from services import Index

app = Flask(__name__, template_folder='resources/templates/')
app.debug = True

service = Index()


@app.route('/')
def index():
    return render_template('index.html', title=service.get_title())


if __name__ == '__main__':
    app.run('0.0.0.0')
