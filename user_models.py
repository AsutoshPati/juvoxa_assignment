from flask_sqlalchemy import SQLAlchemy
import hashlib
import uuid
from datetime import datetime

db = SQLAlchemy()


class HospitalManagement(db.Model):
    __tablename__ = 'hospital_management'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    user_pwd = db.Column(db.String(512), nullable=False)
    user_token = db.Column(db.String(8), nullable=False)

    def __init__(self, name, mail, pwd):
        self.user_name = name
        self.user_mail = mail
        pwd = hashlib.sha512(pwd.encode())
        self.user_pwd = pwd.hexdigest()
        self.user_token = str(uuid.uuid4())[:8]


class Hospital(db.Model):
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    management_group = db.Column(db.Integer, db.ForeignKey('hospital_management.id',
                                                           ondelete='CASCADE'))
    location = db.Column(db.String(500), nullable=False)

    def __init__(self, manager_id, address):
        self.management_group = manager_id
        self.location = address


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_mail = db.Column(db.String(100), unique=True, nullable=False)
    doc_pwd = db.Column(db.String(512), nullable=False)
    doc_token = db.Column(db.String(8), nullable=False)
    doc_hospital = db.Column(db.Integer, db.ForeignKey('hospital.id', ondelete='CASCADE'))

    def __init__(self, name, mail, pwd, branch):
        self.doc_name = name
        self.doc_mail = mail
        pwd = hashlib.sha512(pwd.encode())
        self.doc_pwd = pwd.hexdigest()
        self.doc_token = str(uuid.uuid4())[:8]
        self.doc_hospital = branch


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    pat_name = db.Column(db.String(100), nullable=False)
    pat_mail = db.Column(db.String(100), unique=True, nullable=False)
    pat_pwd = db.Column(db.String(512), nullable=False)
    pat_token = db.Column(db.String(8), nullable=False)

    def __init__(self, name, mail, pwd):
        self.pat_name = name
        self.pat_mail = mail
        pwd = hashlib.sha512(pwd.encode())
        self.pat_pwd = pwd.hexdigest()
        self.pat_token = str(uuid.uuid4())[:8]


class Prescription(db.Model):
    __tablename__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'))
    pat_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'))
    dt_tm = db.Column(db.DateTime, nullable=False)
    disease = db.Column(db.String(500))
    findings = db.Column(db.String(1000))
    suggestions = db.Column(db.String(1000))
    medicines = db.Column(db.String(1000))

    def __init__(self, doctor, patient):
        self.doc_id = doctor
        self.pat_id = patient
        self.dt_tm = datetime.now()
        self.disease = ''
        self.findings = ''
        self.suggestions = ''
        self.medicines = ''
