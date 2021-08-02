from flask_sqlalchemy import SQLAlchemy
import hashlib
import uuid
from datetime import datetime

db = SQLAlchemy()


class HospitalManagement(db.Model):
    """
    Model for Hospital Managers.

    This model will be used to store the hospital management users; information like their name, email id, password and
    tokens will stored. The password will be stored in encrypted format for security reasons. Unique ids will be
    assigned to every manager once the data is stored.

    Attributes
    ----------
    id: int,
        Auto incremented unique id for every manager.
    user_name: str,
        Manager's full name.
    user_mail: str,
        Manager's email ID; will be also used for authentication.
    user_pwd: str,
        Manager's encrypted (SHA512) password.
    user_token: str,
        System for provided token for verification.

    """
    __tablename__ = 'hospital_management'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_mail = db.Column(db.String(100), unique=True, nullable=False)
    user_pwd = db.Column(db.String(512), nullable=False)
    user_token = db.Column(db.String(8), nullable=False)

    def __init__(self, name: str, mail: str, pwd: str):
        """
        The constructor for HospitalManagement class.

        Parameters
        ----------
        name: str,
            Name provided by hospital manager.
        mail: str,
            E-mail id provided by hospital manager.
        pwd: str,
            Password provided by hospital manager; will be encrypted with SHA512 before storing.

        Returns
        -------
        None.

        """
        self.user_name = name
        self.user_mail = mail
        pwd = hashlib.sha512(pwd.encode())
        self.user_pwd = pwd.hexdigest()
        self.user_token = str(uuid.uuid4())[:8]


class Hospital(db.Model):
    """
    Model for Hospital.

    This model will be used to store the hospital info; information like management group, location of hospital. The
    management group will referred from HospitalManagement model to know which hospital belongs to which management
    group to avoid conflicts.

    Attributes
    ----------
    id: int,
        Auto incremented unique id for every hospital.
    management_group: int,
        Manager's id referred from hospital management to know that the hospital belongs to which management group.
    location: str,
        Manager's email ID; will be also used for authentication.

    """
    __tablename__ = 'hospital'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    management_group = db.Column(db.Integer, db.ForeignKey('hospital_management.id',
                                                           ondelete='CASCADE'))
    location = db.Column(db.String(500), nullable=False)

    def __init__(self, manager_id: int, address: str):
        """
        The constructor for HospitalManagement class.

        Parameters
        ----------
        manager_id: int,
            Provided hospital manager id.
        address: str,
            Location address of hospital provided.

        Returns
        -------
        None.

        """
        self.management_group = manager_id
        self.location = address


class Doctor(db.Model):
    """
    Model for Doctor.

    This model will be used to store the doctors information; information like their name, email id, password, token and
    working hospital will be stored. The password will be stored in encrypted format for security reasons. Unique ids
    will be assigned to every doctor once the data is stored.

    Attributes
    ----------
    id: int,
        Auto incremented unique id for every doctor.
    doc_name: str,
        Doctor's full name.
    doc_mail: str,
        Doctor's email ID; will be also used for authentication.
    doc_pwd: str,
        Doctor's encrypted (SHA512) password.
    doc_token: str,
        System for provided token for verification.
    doc_hospital: int,
        Hospital id where doctor is currently employed.

    """
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doc_name = db.Column(db.String(100), nullable=False)
    doc_mail = db.Column(db.String(100), unique=True, nullable=False)
    doc_pwd = db.Column(db.String(512), nullable=False)
    doc_token = db.Column(db.String(8), nullable=False)
    doc_hospital = db.Column(db.Integer, db.ForeignKey('hospital.id', ondelete='CASCADE'))

    def __init__(self, name: str, mail: str, pwd: str, branch: int):
        """
        The constructor for Doctor class.

        Parameters
        ----------
        name: str,
            Name provided by doctor.
        mail: str,
            E-mail id provided by doctor.
        pwd: str,
            Password provided by doctor; will be encrypted with SHA512 before storing.
        branch: int,
            Hospital id where doctor is currently employed.

        Returns
        -------
        None.

        """
        self.doc_name = name
        self.doc_mail = mail
        pwd = hashlib.sha512(pwd.encode())
        self.doc_pwd = pwd.hexdigest()
        self.doc_token = str(uuid.uuid4())[:8]
        self.doc_hospital = branch


class Patient(db.Model):
    """
    Model for Patient.

    This model will be used to store the patients information; information like their name, email id, password, and
    token will be stored. The password will be stored in encrypted format for security reasons. Unique ids
    will be assigned to every patient once the data is stored.

    Attributes
    ----------
    id: int,
        Auto incremented unique id for every patient.
    pat_name: str,
        Patient's full name.
    pat_mail: str,
        Patient's email ID; will be also used for authentication.
    pat_pwd: str,
        Patient's encrypted (SHA512) password.
    pat_token: str,
        System for provided token for verification.

    """
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    pat_name = db.Column(db.String(100), nullable=False)
    pat_mail = db.Column(db.String(100), unique=True, nullable=False)
    pat_pwd = db.Column(db.String(512), nullable=False)
    pat_token = db.Column(db.String(8), nullable=False)

    def __init__(self, name, mail, pwd):
        """
        The constructor for Patient class.

        Parameters
        ----------
        name: str,
            Name provided by patient.
        mail: str,
            E-mail id provided by patient.
        pwd: str,
            Password provided by patient; will be encrypted with SHA512 before storing.

        Returns
        -------
        None.

        """
        self.pat_name = name
        self.pat_mail = mail
        pwd = hashlib.sha512(pwd.encode())
        self.pat_pwd = pwd.hexdigest()
        self.pat_token = str(uuid.uuid4())[:8]


class Prescription(db.Model):
    """
    Model for Prescription.

    This model will be used to store the prescription related information; information like doctor id, patient id, date
    & time of prescription generation, disease information, observation/findings of disease, suggestions (lab tests,
    exercise etc.) and prescribed medicines. Basically it connects patient with their doctors through this prescription.

    Attributes
    ----------
    id: int,
        Auto incremented unique id for every patient.
    doc_id: int,
        Doctor's id, to whom appointment has been taken.
    pat_id: int,
        Patient's id; who has taken appointment.
    dt_tm: datetime,
        Date & time when the appointment has been generated.
    disease: str,
        Disease found during check/observation.
    findings: str,
        Description of observation/findings.
    suggestions: str,
        Suggestions given by the doctor.
    medicines: str,
        Medicines suggested by doctor.

    """
    __tablename__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('doctor.id', ondelete='CASCADE'))
    pat_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'))
    dt_tm = db.Column(db.DateTime, nullable=False)
    disease = db.Column(db.String(500))
    findings = db.Column(db.String(1000))
    suggestions = db.Column(db.String(1000))
    medicines = db.Column(db.String(1000))

    def __init__(self, doctor: int, patient: int):
        """
        The constructor for Patient class.

        Parameters
        ----------
        doctor: int,
            Doctor's id, to whom appointment has been taken.
        patient: int,
            Patient's id; who has taken appointment.

        Returns
        -------
        None.

        """
        self.doc_id = doctor
        self.pat_id = patient
        self.dt_tm = datetime.now()
        self.disease = ''
        self.findings = ''
        self.suggestions = ''
        self.medicines = ''
