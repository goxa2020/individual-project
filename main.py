from flask import Flask, render_template, request, redirect, flash, session, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Даня_писька'


@app.route('/login', methods=['POST'])
def login_form():
    email = request.form['email']
    password = request.form['psw']
    if 'userLogged' in session:
        return redirect(session['userLogged'])
    if email == 'goxa' and password == '123':
        session['userLogged'] = email
        return redirect(session['userLogged'])
    flash('Аккаунт не найден')
    return render_template('login.html', title='Авторизация')


@app.route('/register', methods=['POST'])
def register_form():
    user = session.get('userLogged')
    if request.form['psw'] == request.form['psw-repeat']:
        session['userLogged'] = request.form['email']
        return redirect('/')
    flash('Ты пипка(пароли не совпали)')
    return render_template('register.html', title='Регистрация', user=user)


@app.route('/log_out', methods=['POST'])
def log_out():
    del session['userLogged']
    return redirect('/')


@app.route('/')
def index():
    user = session.get('userLogged')
    return render_template('mainpage.html', user=user)


@app.route('/register')
def register():
    if 'userLogged' in session:
        return redirect(session['userLogged'])
    return render_template('register.html', title='Регистрация')


@app.route('/login')
def login():
    if 'userLogged' in session:
        return redirect(session['userLogged'])
    return render_template('login.html', title='Авторизация')


@app.route('/<path:profile_page>')
def profile(profile_page):
    user = session.get('userLogged')
    if profile_page in ['goxa', '555', 'qwerty'] or user == profile_page:
        return render_template('profile.html', profile_page=profile_page, user=user, title=profile_page)
    return abort(404)


@app.errorhandler(404)
def not_found(error):
    user = session.get('userLogged')
    return render_template('not_found.html', title='Страница не найдена', user=user), 404


if __name__ == '__main__':
    app.run(debug=True)
