from flask import Flask, Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def home():
    return render_template('home.html')
