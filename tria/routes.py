from tria import app
from flask import render_template, request, redirect, Response, send_file
from tria.test import username_exist, user_pass, reg_account, password_encrypt, password_decrypt, User, form_db_data, is_admin, save_form, single_form_data, create_form_id_db, kyc_form_exist, upload_file_db, get_image, save_kyc_form_db, kycform_db_data, single_kycform_data, kyc_form_already
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
import uuid
from io import BytesIO

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
  return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
  current_userid = current_user.id
  if is_admin(current_userid):
    form_db = form_db_data()
    kycform_db = kycform_db_data()
    return render_template('dashboard.html', 
                           form_db=form_db, 
                           kycform_db=kycform_db)


@app.route("/login-tria", methods=['POST', 'GET'])
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


@app.route("/tria-g-register", methods=["POST", "GET"])
@login_required
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
    save_form(amount, fname, sname, gender, mobile, pincode, pan, email,
              daytime)
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

@app.route('/kycformdata')
@login_required
def kycform_data_page():
  current_userid = current_user.id
  if is_admin(current_userid):
    form_db = kycform_db_data()
    return render_template('kycdata.html', form_db=form_db)
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

@app.route('/kycdata/<form_id>')
@login_required
def single_kycform_page(form_id):
  current_userid = current_user.id
  if is_admin(current_userid):
    single_form = single_kycform_data(form_id)
    if single_form:
      return render_template('kycsingle.html', single_form=single_form)
    else:
      return '<h1>Not able to find that form in database</h1> <a href="/formdata">Go back to Dashboard</a>'
  return redirect('/dashboard')

@app.route('/logout')
def logout():
  logout_user()
  return redirect('/')


@app.route('/kycform/<formid>', methods=['POST', 'GET'])
def table_page(formid):
  form_exist = kyc_form_exist(formid)
  if form_exist:
    kyc_already = kyc_form_exist(formid)
    if request.method == 'POST':
        form = request.form
        fname = form.get('fname')
        sname = form.get('sname')
        mobile = form.get('mobile')
        pincode = form.get('pincode')
        pan = form.get('pan')
        email = form.get('email')
        dob = form.get('dob')
        address = form.get('address')
        aadhar = form.get('aadhar')
        mstatus = form.get('mstatus')
        gaurdian = form.get('gaurdian')
        latitude = form.get('latitude')
        longitude = form.get('longitude')
        save_kyc_form_db(formid, 
                         fname, 
                         sname, 
                         mobile, 
                         email, 
                         pincode, 
                         pan, 
                         dob, 
                         address, 
                         aadhar, 
                         mstatus, 
                         gaurdian, 
                         latitude, 
                         longitude)
        return 'ok'
    return render_template('kycform.html', formid=formid)

    return 'Form was already submitted', 401
  return 'form not exist'

@app.route('/kyc/<doc_type>/<form_id>', methods=['POST', 'GET'])
def kyc_page(doc_type, form_id):
  if request.method == 'POST':
    if doc_type not in request.files:
      return 'error while uploading the image', 400
    image = request.files[doc_type]
    if image.filename == '':
      return 'error while uploading the image', 400

    if image and allowed_file(image.filename):
      file_extension = image.filename.rsplit('.', 1)[1].lower()
      new_filename = f"{form_id}.{file_extension}"
      mimetype = image.mimetype
      upload_file_local = upload_file_db(doc_type, form_id, image.read(), mimetype, new_filename)
      if not upload_file_local:
        return 'uploaded', 200
    return 'error', 400

@app.route('/image/<table_name>/<id>')
@login_required
def image_page(table_name, id):
  image = get_image(table_name, id)
  print(image)
  if not image:
    return 'Image not found', 404
  img_stream = BytesIO(image[-1].img_data)
  headers = {
        'Content-Type': image[-1].img_type,
        'Content-Disposition': 'inline;filename=' + image[-1].img_name
    }
  return Response(img_stream.getvalue(), 
                  headers=headers)
  return send_file(BytesIO(image[-1].img_data), 
                   download_name=image[-1].img_name, 
                   as_attachment=True )

@app.route('/create-form')
@login_required
def create_form_page():
  formid = uuid.uuid1()
  create_form_id_db(formid)
  return str(formid)