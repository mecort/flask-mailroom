import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['donor']).get()
        except Donor.DoesNotExist:
            return render_template('add.jinja2',
                                   error='Invalid Donor, '
                                   'please enter a donor that is in the database.')
        donation = Donation(donor=donor,
                            value=int(request.form['amount']))
        donation.save()
        # donations = Donation.select()
        return redirect(url_for('all'))
    return render_template('add.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

