"""App that takes name, age, and favorite softdes ninja."""

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def take_input():

    return render_template('input.html')

@app.route('/profile', methods=["GET","POST"])
def output():
    name = request.form.get('name')
    age = request.form.get('age')
    ninja = request.form.get('ninja')
    if name == "":
        return render_template('error.html')
    elif age == "":
        return render_template('error.html')
    else:
        return render_template('profile.html', name=name, age=age)




if __name__ == '__main__':
    app.run()
