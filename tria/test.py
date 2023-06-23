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
  

# query = session.query(User).all()
# for row in query:
#    print (row.password,row.email)
# ch = 0
# query = session.query(User).filter_by(email='muhe@gmail.com').all()
# for email in query:
#   ch = email.id
# print(ch)

def form_db_data():
  query = session.query(Form).order_by(Form.id.desc())
  return query

def single_form_data(form_id):
  query = session.query(Form).filter_by(id=form_id).all()
  return query

def username_exist(email):
  user = 0
  query = session.query(User).filter_by(email=email).all()
  for email in query:
    user = email.id
  if user == 0:
    return None
  else:
    return user

def user_pass(email):
  user = 0
  query = session.query(User).filter_by(email=email).all()
  for email in query:
    user = email.password
  if user == 0:
    return None
  else:
    return user

def is_admin(email):
  user = 0
  query = session.query(User).filter_by(email=email).all()
  for email in query:
    user = email.admin
  return user

def reg_account(email, password):
  register_data = User(email=email,
                       password=password
                      )
  db_res = session.add(register_data)
  session.commit()
  return db_res

def save_form(loan, fname, sname, gender, mobile, pincode, pan, email, daytime):
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
  session.commit()
  return db_res

def user(email):
  query = session.query(User).filter_by(email=email).all()
  return query
  

def password_encrypt(plain_pass):
  password_hash = bcrypt.generate_password_hash(plain_pass).decode('utf-8')
  return password_hash

def password_decrypt(password_hash, plain_pass):
  password_hash = bcrypt.check_password_hash(
    password_hash, plain_pass
  )
  return password_hash
