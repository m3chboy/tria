from tria import bcrypt, login_manager, session, Base
from sqlalchemy import Column, Date, Integer, Text, Boolean, desc
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_email):
  present = 0
  query = session.query(User).filter_by(email=user_email).all()
  for emailid in query:
    present = emailid.id
  if present == 0:
    return
  user = User()
  user.id = user_email
  return user


class User(Base, UserMixin):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(Text, nullable=False)
  password = Column(Text, nullable=False)
  admin = Column(Boolean, nullable=False, default=False)


class Form(Base):
  __tablename__ = 'user_form'

  id = Column(Integer, primary_key=True, nullable=False)
  loan = Column(Integer, nullable=False)
  fname = Column(Text, nullable=False)
  sname = Column(Text, nullable=False)
  gender = Column(Text, nullable=False)
  mobile = Column(Text, nullable=False)
  pincode = Column(Integer, nullable=False)
  pan = Column(Text, nullable=False)
  email = Column(Text, nullable=False)
  daytime = Column(Date, nullable=False)


class kycForm(Base):
  __tablename__ = 'kyc_form'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  fname = Column(Text)
  sname = Column(Text)
  mobile = Column(Text)
  pincode = Column(Integer)
  pan = Column(Text)
  email = Column(Text)
  dob = Column(Text)
  address = Column(Text)
  aadhar = Column(Text)
  mstatus = Column(Text)
  gaurdian = Column(Text)
  latitude = Column(Text)
  longitude = Column(Text)

class kycFormid(Base):
  __tablename__ = 'kyc_form_id'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)

class aadharUpload(Base):
  __tablename__ = 'aadhar_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

class incomeUpload(Base):
  __tablename__ = 'income_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

class bankUpload(Base):
  __tablename__ = 'bank_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

class panUpload(Base):
  __tablename__ = 'pan_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

class selfiUpload(Base):
  __tablename__ = 'selfi_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

class otherUpload(Base):
  __tablename__ = 'other_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

class esignUpload(Base):
  __tablename__ = 'esign_upload'

  id = Column(Integer, primary_key=True, nullable=False)
  formid = Column(Text, nullable=False)
  img_data = Column(Text, nullable=False)
  img_type = Column(Text, nullable=False)
  img_name = Column(Text, nullable=False)

def form_db_data():
  query = session.query(Form).order_by(Form.id.desc())
  return query

def kycform_db_data():
  query = session.query(kycForm).order_by(kycForm.id.desc())
  return query

def single_form_data(form_id):
  query = session.query(Form).filter_by(id=form_id).all()
  return query

def single_kycform_data(form_id):
  query = session.query(kycForm).filter_by(formid=form_id).all()
  return query


def username_exist(email):
  user = 0
  query = session.query(User).filter_by(email=email).all()
  for email in query:
    user = email.id
  session.rollback()
  if user == 0:
    return None
  else:
    return user

def kyc_form_exist(formid):
  user = 0
  query = session.query(kycFormid).filter_by(formid=formid).all()
  for form in query:
    user = form.id
  session.rollback()
  if user == 0:
    return None
  else:
    return user

def kyc_form_already(formid):
  user = 0
  query = session.query(kycForm).filter_by(formid=formid).all()
  for form in query:
    user = form.id
  session.rollback()
  if user == 0:
    return None
  else:
    return user


def user_pass(email):
  user = 0
  query = session.query(User).filter_by(email=email).all()
  for email in query:
    user = email.password
  session.rollback()
  if user == 0:
    return None
  else:
    return user


def is_admin(email):
  user = 0
  query = session.query(User).filter_by(email=email).all()
  for email in query:
    user = email.admin
  session.rollback()
  return user

def get_image(table_db, id):
  session.rollback()
  if table_db == 'aadhar_cpy':
    query = session.query(aadharUpload).filter_by(formid=id).all()

  elif table_db == 'pan_cpy':
    query = session.query(panUpload).filter_by(formid=id).all()

  elif table_db == 'selfi_cpy':
    query = session.query(selfiUpload).filter_by(formid=id).all()

  elif table_db == 'income_cpy':
    query = session.query(incomeUpload).filter_by(formid=id).all()

  elif table_db == 'bank_cpy':
    query = session.query(bankUpload).filter_by(formid=id).all()
  elif table_db == 'other_cpy':
    query = session.query(otherUpload).filter_by(formid=id).all()

  elif table_db == 'esign_cpy':
    query = session.query(esignUpload).filter_by(formid=id).order_by(esignUpload.id.desc())

  else:
    session.rollback()
  return query


def reg_account(email, password):
  register_data = User(email=email, password=password)
  db_res = session.add(register_data)
  try:
    session.commit()
  except:
    session.rollback()
    raise
  return db_res


def save_form(loan, fname, sname, gender, mobile, pincode, pan, email,
              daytime):
  form_data = Form(loan=loan,
                   fname=fname,
                   sname=sname,
                   gender=gender,
                   mobile=mobile,
                   pincode=pincode,
                   pan=pan,
                   email=email,
                   daytime=daytime)
  db_res = session.add(form_data)
  try:
    session.commit()
  except:
    session.rollback()
    raise
  return db_res

def save_kyc_form_db (formid, fname, sname, mobile, email, pincode, pan, dob, address, aadhar, mstatus, gaurdian, latitude, longitude):
  form_data = kycForm(formid=formid,
                      fname=fname,
                      sname=sname,
                      mobile=mobile,
                      pincode=pincode,
                      pan=pan,
                      email=email,
                      dob=dob,
                      address=address,
                      aadhar=aadhar,
                      mstatus=mstatus,
                      gaurdian=gaurdian,
                      latitude=latitude,
                      longitude=longitude)
  db_res = session.add(form_data)
  try:
    session.commit()
  except:
    session.rollback()
    raise
  return db_res


def create_form_id_db(id):
  form_data = kycFormid(formid=id)
  db_res = session.add(form_data)
  try:
    session.commit()
  except:
    session.rollback()
    raise
  return db_res

def upload_file_db(table_db, formid, img_data, img_type, img_name):

  if table_db == 'aadhar_upload':
    form_data = aadharUpload(formid=formid, 
                             img_data=img_data, 
                             img_type=img_type, 
                             img_name=img_name)
  elif table_db == 'pan_upload':
    form_data = panUpload(formid=formid, 
                          img_data=img_data, 
                          img_type=img_type, 
                          img_name=img_name)
  elif table_db == 'selfi_upload':
    form_data = selfiUpload(formid=formid, 
                            img_data=img_data, 
                            img_type=img_type, 
                            img_name=img_name)
  elif table_db == 'bank_upload':
    form_data = bankUpload(formid=formid, 
                           img_data=img_data, 
                           img_type=img_type, 
                           img_name=img_name)
  elif table_db == 'income_upload':
    form_data = incomeUpload(formid=formid, 
                             img_data=img_data, 
                             img_type=img_type, 
                             img_name=img_name)

  elif table_db == 'esign_upload':
    form_data = esignUpload(formid=formid, 
                             img_data=img_data, 
                             img_type=img_type, 
                             img_name=img_name)

  elif table_db == 'other_upload':
    form_data = otherUpload(formid=formid, 
                            img_data=img_data, 
                            img_type=img_type, 
                            img_name=img_name)
  else:
    return None
  db_res = session.add(form_data)
  try:
    session.commit()
  except:
    session.rollback()
    raise
  return db_res

def user(email):
  session.rollback()
  query = session.query(User).filter_by(email=email).all()
  return query


def password_encrypt(plain_pass):
  password_hash = bcrypt.generate_password_hash(plain_pass).decode('utf-8')
  return password_hash


def password_decrypt(password_hash, plain_pass):
  password_hash = bcrypt.check_password_hash(password_hash, plain_pass)
  return password_hash
