from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# ---------- Model ----------
class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    event_name = db.Column(db.String(150), nullable=False)

# ---------- Forms ----------
class AttendeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    event_name = StringField('Event Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# ---------- Routes ----------
@app.route('/')
def index():
    attendees = Attendee.query.all()
    return render_template('index.html', attendees=attendees)

@app.route('/add', methods=['GET', 'POST'])
def add_attendee():
    form = AttendeeForm()
    if form.validate_on_submit():
        attendee = Attendee(
            name=form.name.data,
            email=form.email.data,
            event_name=form.event_name.data
        )
        db.session.add(attendee)
        db.session.commit()
        flash('Attendee added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_attendee.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_attendee(id):
    attendee = Attendee.query.get_or_404(id)
    form = AttendeeForm(obj=attendee)
    if form.validate_on_submit():
        attendee.name = form.name.data
        attendee.email = form.email.data
        attendee.event_name = form.event_name.data
        db.session.commit()
        flash('Attendee updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_attendee.html', form=form)

@app.route('/delete/<int:id>')
def delete_attendee(id):
    attendee = Attendee.query.get_or_404(id)
    db.session.delete(attendee)
    db.session.commit()
    flash('Attendee removed!', 'danger')
    return redirect(url_for('index'))

# ---------- Run Server ----------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
