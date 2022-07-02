from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Location URL', validators=[DataRequired(), URL()])
    open = StringField('Open Time', validators=[DataRequired()])
    close = StringField('Close Time', validators=[DataRequired()])
    wifi_rating = SelectField('wifi rating', validators=[DataRequired()], choices=[('✘'), ('💪'), ('💪💪'), ('💪💪💪'),
                                ('💪💪💪💪'), ('💪💪💪💪💪') ])
    coffee_rating = SelectField('coffee rating', validators=[DataRequired()], choices=[('✘'), ('☕'), ('☕☕'),('☕☕☕'),('☕☕☕☕'), ('☕☕☕☕☕')])
    power_rating = SelectField('Power rating', validators=[DataRequired()], choices=[('✘'), ('🔌'), ('🔌🔌'),('🔌🔌🔌'),('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a",  encoding='utf-8',
              errors='ignore') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location_url.data},"
                           f"{form.open.data},"
                           f"{form.close.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8',
              errors='ignore') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows, list_length=len(list_of_rows))


if __name__ == '__main__':
    app.run(debug=True)
