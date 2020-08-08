from flask import Flask, Response, render_template, request
from datetime import datetime
from time import sleep
import pytz

app = Flask(__name__)
zone = datetime.now()


@app.route('/')
def home():
    return render_template('home.html', zones=pytz.common_timezones)


@app.route('/time_feed')
def time_feed():
    def generate():
        global zone
        yield zone.strftime("%I:%M:%S%p")
        sleep(1)
    return Response(generate(), mimetype='text')


@app.route("/select", methods=['GET', 'POST'])
def select():
    selected_zone = request.form.get('zone_select')
    time_zone = pytz.timezone(selected_zone)
    orgtimeobj = datetime.now()
    newtimeobj = time_zone.localize(orgtimeobj)
    global zone
    zone = newtimeobj
    return render_template('home.html', zones=pytz.common_timezones)


if __name__ == '__main__':
    app.run(debug=True)
