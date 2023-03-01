from datetime import date
import logging
import sys, os, socket
from flask import Flask, render_template, redirect, request, url_for

from data import Ethnicity, Gender, Participant, Video, Library

hostname = socket.gethostname()
today = date.today().strftime('%Y%m%d')

logging.basicConfig(level = logging.INFO, format = '%(asctime)s %(message)s',
    datefmt = '%H:%M:%S', filename = f"logs/{hostname}_{today}.log", filemode = 'a')


app = Flask(__name__)
app.debug = True

p = Participant()
lib = Library.all()

@app.route("/")
def index():
    global p
    p = Participant()
    return render_template("index.html")


@app.route("/participant", methods = [ 'GET', 'POST' ])
def participant():
    if request.method == "POST":
        global p
        p = Participant(request.form['pid'], request.form['age'],
            request.form['gender'], request.form['ethnicity'])
        p.save()
        logging.info(f"Save participant details for {p.pid}")

        return redirect(url_for("prep"))

    return render_template("participant.html", data = Participant(),
        ethnicities = Ethnicity.members(), genders = Gender.members())


@app.route("/prep")
def prep():
    global p
    if not p.pid:
        return redirect(url_for("index"))

    return render_template("prep.html")


def _getvideo():
    global p
    v = Video.random(vids = lib, seen = p.videos)
    if v:
        return render_template("video.html", video = v, participant = p)
    else:
        try:
            p.save()
            logging.info(f"Finished rating for {p.pid}")

            return render_template('done.html', success_text = 'Data saved successfully')
        except:
            return render_template('done.html', success_text = 'Issue with saving participant data. Please mention this to experimenters')


@app.route("/video", methods = [ 'GET', 'POST' ])
def video():
    global p
    if not p.pid:
        return redirect(url_for("index"))

    if request.method == 'GET':
        return _getvideo()
    else:
        v = Video(request.form['vid'], request.form['psi'])
        r = int(request.form['rating'])
        p.rate(v, r)
        p.save()

        logging.info(f"Save rating {r} for {p.pid} and {v.vid}")
        return _getvideo()


if __name__ == '__main__':
    app.run()
