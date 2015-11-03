import datetime
import os
import psycopg2 as dbb

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/teams')
def teams():
    now = datetime.datetime.now()
    return render_template('teams.html', current_time=now.ctime())




if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    app.run(host='0.0.0.0', port=int(PORT))
