from tria import app
from flask import render_template, request, redirect
from tria.test import username_exist, user_pass, reg_account, password_encrypt, password_decrypt, User, form_db_data, is_admin, save_form, single_form_data
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date


@app.route("/")
def home():
  return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
  current_userid = current_user.id
  if is_admin(current_userid):
    form_db = form_db_data()
    return render_template('dashboard.html', form_db=form_db)


@app.route("/login", methods=['POST', 'GET'])
def login_page():
  if request.method == 'POST':
    form = request.form
    email = form.get('email')
    password = form.get('password')
    username_exist_check = username_exist(email)
    if username_exist_check:
      db_pass = user_pass(email)
      if password_decrypt(db_pass, password):
        user = User()
        user.id = email
        login_user(user)
        return redirect('/dashboard')
  return render_template('login.html')


@app.route("/register", methods=["POST", "GET"])
def user_register():
  if request.method == 'POST':
    form = request.form
    email = form.get('email')
    password = form.get('password')
    username_exist_check = username_exist(email)
    if username_exist_check:
      return redirect('/login')
    else:
      encrypted_pass = password_encrypt(password)
      register = reg_account(email, encrypted_pass)
      if register == None:
        return 'Account created successfully'
      else:
        return 'error'
  return render_template("register.html")


@app.route('/form', methods=['POST', 'GET'])
def form_page():
  if request.method == 'POST':
    form = request.form
    amount = form.get('amount')
    fname = form.get('fname')
    sname = form.get('sname')
    gender = form.get('gender')
    mobile = form.get('mobile')
    pincode = form.get('pincode')
    pan = form.get('pan')
    email = form.get('email')
    daytime = date.today()
    save_form(amount, fname, sname, gender, mobile, pincode, pan, email, daytime)
    return redirect('/')
  return render_template('entry.html')


@app.route('/formdata')
@login_required
def form_data_page():
  current_userid = current_user.id
  if is_admin(current_userid):
    form_db = form_db_data()
    return render_template('data.html', form_db=form_db)
  return redirect('/dashboard')

@app.route('/data/<form_id>')
@login_required
def single_form_page(form_id):
  current_userid = current_user.id
  if is_admin(current_userid):
    single_form = single_form_data(form_id)
    print(single_form)
    if single_form:
      print('hello')
      return render_template('single.html', single_form=single_form)
    else:
      return '<h1>Not able to find that form in database</h1> <a href="/formdata">Go back to Dashboard</a>'
  return redirect('/dashboard')


@app.route('/logout')
def logout():
  logout_user()
  return redirect('/')

@app.route('/table', methods=['POST', 'GET'])
def table_page():
  if request.method == 'POST':
    image = request.files['file']
    return str(image)
  return render_template('table.html')