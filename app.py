import os
from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from form import NameForm
import plotly
import json
import plotly.express as px

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'shit!!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1))

    def __repr__(self):
        return f'<Role:{self.name}>'


@app.route('/')
def home():
    # try:
    #     return render_template('index.html', name=session['name'])
    # except:
    #     lst = [1, 2, 3]
    #     return render_template('index.html', lst=lst)
        return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
    form = NameForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            role = Role.query.filter_by(name=form.name.data).first()
            add_role = Role(name=form.name.data, email=form.email.data,
                            age=form.age.data, sex=form.sex.data)
            db.session.add(add_role)
            db.session.commit()
            flash('成功提交', 'success')
            session['name'] = form.name.data
            # session['known'] = False
            return redirect(url_for('home'))

    return render_template('form.html', form=form)


@app.route('/plot')
def plot():
    df = px.data.gapminder().query("continent=='Oceania'")
    fig1 = px.line(df, x="year", y="lifeExp", color='country', title="Life Expectancy")
    df = px.data.medals_wide()
    fig2 = px.bar(df, x="nation", y=["gold", "silver", "bronze"], title="Wide-Form Input")
    df = px.data.iris()
    fig3 = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                         color='species', title="Iris Dataset", width=700, height=600)

    context = {
        'chart1': fig1.to_html(),
        'chart2': fig2.to_html(),
        'chart3': fig3.to_html()
    }
    return render_template('plot.html', **context)


@app.route('/tex', methods=['GET', 'POST'])
def tex():
    latex = r"""When \(a \ne 0\), there are two solutions to \(ax^2 + bx + c = 0\) and they are
                $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$"""
    if request.method == 'POST':
        latex = request.form['latex']
        # print(latex)

    return render_template('tex.html', latex=latex)


if __name__ == '__main__':
    app.run()
