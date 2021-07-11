from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '59eb5820bce3227f5308d8e82fa62e97'

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html', title="login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Cuenta creada para {form.username.data}!", "success")
        return redirect(url_for('home'))

    return render_template('register.html', title="register", form=form)


if __name__ == '__main__':
    app.run(debug=True)