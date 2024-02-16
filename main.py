from flask import Flask, render_template, request, redirect, flash, session, abort
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Даня_крутой'


@app.route('/login', methods=['POST'])
def login_form():
    email = request.form['email']
    password = request.form['psw']
    if 'userLogged' in session:
        return redirect(session['userLogged'])
    if email == 'goxa@com' and password == '123':
        session['userLogged'] = email
        return redirect(email)
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


@app.route('/log_out', methods=['GET', 'POST'])
def log_out():
    if session['userLogged']:
        del session['userLogged']
    return redirect('/')


@app.route('/')
def index():
    user = session.get('userLogged')
    return render_template('mainpage.html', user=user)


@app.route('/registration')
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


@app.route('/about')
def about():
    user = session.get('userLogged')
    return render_template('about.html', title='О нас', user=user, about_active='active')


@app.route('/<profile_page>')
def profile(profile_page):
    user = session.get('userLogged')
    if profile_page in ['goxa', 'goxa@com', '555', 'qwerty'] or user == profile_page:
        return render_template('profile.html', profile_page=profile_page, user=user, title=profile_page)
    return abort(404, profile_page)


@app.errorhandler(404)
def not_found(error: NotFound):
    page = error.description
    page = (page if len(page) <= 20 else '')
    user = session.get('userLogged')
    return render_template('not_found.html', title='Страница не найдена', user=user, page=page), 404


if __name__ == '__main__':
    app.run(debug=True)
