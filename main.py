# -*- coding: utf-8 -*-
"""

    Project Name        : Juvoxa Assignment
    Author              : Asutosh Pati
    Date of Creation    : 17 JUN 2021
    Purpose             : As a part of recruitment process
    Description         : Creating api for simulated hospital management environment.
    Version             : ver 0.0.1

"""

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from sqlalchemy import exc
from user_models import db
from user_models import HospitalManagement, Hospital
from user_models import Doctor, Patient, Prescription
import hashlib


app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

pg_user = 'postgres'    # user name for your postgres
pg_pwd = 'superuser'    # password for postgres user
pg_host = '127.0.0.1'   # hosted IP where postgres is hosted
pg_db = 'juvoxa_task'   # database name in postgres

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{pg_user}:{pg_pwd}@{pg_host}/{pg_db}'


def validate_token(headers, valid_type):
    if 'user_id' not in headers and 'user_token' not in headers:
        return {'message': 'Headers are missing'}, 401
    user_id = headers['user_id']
    user_token = headers['user_token']
    if user_id is None or user_token is None:
        return {'message': 'Headers are missing'}, 401

    user = None
    if valid_type == 'M':
        user = HospitalManagement.query.filter(
            HospitalManagement.id == user_id,
            HospitalManagement.user_token == user_token).first()
    elif valid_type == 'D':
        user = Doctor.query.filter(Doctor.id == user_id, Doctor.doc_token == user_token).first()
    elif valid_type == 'P':
        user = Patient.query.filter(Patient.id == user_id, Patient.pat_token == user_token).first()

    if user is None:
        return {'message': 'Invalid authentication; Access Denied'}, 401


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(404)
def handle_404(e):
    return {'message': 'Requested page not available'}, 404


# @app.errorhandler(500)
# def handle_500(e):
#     return {'message': 'Something went wrong'}, 500


class HospitalManager(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('management_name', type=str, required=True,
                            help='Management can not be created without management name')
        parser.add_argument('management_mail', type=str, required=True,
                            help='Management can not be created without an email')
        parser.add_argument('management_pwd', type=str, required=True,
                            help='Give strong password to make management account safe')
        args = parser.parse_args()
        try:
            manager = HospitalManagement(args['management_name'], args['management_mail'],
                                         args['management_pwd'])
            db.session.add(manager)
            db.session.commit()
        except exc.IntegrityError:
            return {'message': 'Email already in use'}, 400
        except:
            return {'message': 'Some unknown error occurred'}, 500
        else:
            return {'message': 'New hospital group added'}, 201

    @staticmethod
    def get():
        hosp_managers = HospitalManagement.query.all()
        if len(hosp_managers) > 0:
            manager_list = []
            for manager in hosp_managers:
                curr_manager = {'id': manager.id}
                curr_manager.update({'management_name': manager.user_name})
                curr_manager.update({'management_email': manager.user_mail})
                manager_list.append(curr_manager)
            return {'message': {'num_records': len(hosp_managers), 'records': manager_list}}
        return {'message': 'No managers have been registered yet'}


class Login(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help='Registered email should be provided')
        parser.add_argument('password', type=str, required=True,
                            help='Valid password should be given for specified email')
        args = parser.parse_args()

        pwd = hashlib.sha512(args['password'].encode())
        pwd = pwd.hexdigest()

        return_msg = None

        manager = HospitalManagement.query.filter(
            HospitalManagement.user_mail == args['email'],
            HospitalManagement.user_pwd == pwd).first()
        if manager is not None:
            return_msg = {'user_id': manager.id, 'user_token': manager.user_token,
                          'user_type': 'M'}

        doctor = Doctor.query.filter(Doctor.doc_mail == args['email'],
                                     Doctor.doc_pwd == pwd).first()
        if doctor is not None:
            return_msg = {'user_id': doctor.id, 'user_token': doctor.doc_token,
                          'user_type': 'D'}

        patient = Patient.query.filter(Patient.pat_mail == args['email'],
                                       Patient.pat_pwd == pwd).first()
        if patient is not None:
            return_msg = {'user_id': patient.id, 'user_token': patient.pat_token,
                          'user_type': 'P'}

        if return_msg is not None:
            return return_msg
        else:
            return {'message': 'Invalid email or password or usertype'}, 400


class HospitalBranch(Resource):
    @staticmethod
    def post():
        validated_msg = validate_token(request.headers, 'M')
        if validated_msg is not None:
            return validated_msg

        user_id = request.headers['user_id']
        parser = reqparse.RequestParser()
        parser.add_argument('address', type=str, required=True,
                            help='Provide new hospital location address')
        args = parser.parse_args()
        try:
            hospital = Hospital(int(user_id), args['address'])
            db.session.add(hospital)
            db.session.commit()
        except:
            return {'message': 'Some unknown error occurred'}, 500
        else:
            return {'message': 'New hospital branch added'}, 201

    @staticmethod
    def get():
        validated_msg = validate_token(request.headers, 'M')
        if validated_msg is not None:
            return validated_msg

        user_id = request.headers['user_id']
        hospitals = Hospital.query.filter(Hospital.management_group == user_id).all()
        if len(hospitals) > 0:
            branch_list = []
            for hospital in hospitals:
                curr_branch = {'id': hospital.id}
                curr_branch.update({'Address': hospital.location})
                branch_list.append(curr_branch)
            return {'message': {'num_branches': len(branch_list), 'branches': branch_list}}
        else:
            return {'message': 'No branches has been created yet'}


class DoctorsData(Resource):
    @staticmethod
    def post(doc_id):
        validated_msg = validate_token(request.headers, 'M')
        if validated_msg is not None:
            return validated_msg

        if doc_id != '0':
            return {'message': 'Doctor id needs to be 0 to add new doctor'}, 400

        user_id = request.headers['user_id']
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Doctor name must be specified')
        parser.add_argument('email', type=str, required=True,
                            help='Doctor email must be specified')
        parser.add_argument('password', type=str, required=True,
                            help='A password is needed to make account safe')
        parser.add_argument('branch', type=int, required=True,
                            help='Assign doctor to a branch')
        args = parser.parse_args()
        try:
            hospital = Hospital.query.filter(Hospital.id == args['branch'],
                                             Hospital.management_group == user_id).first()
            if hospital is None:
                return {'message': 'Unable to find this hospital branch'}, 400

            doctor = Doctor(args['name'], args['email'], args['password'], args['branch'])
            db.session.add(doctor)
            db.session.commit()
        except exc.IntegrityError:
            return {'message': 'Email already in use'}, 400
        except:
            return {'message': 'Some unknown error occurred'}, 500
        else:
            return {'message': 'New doctor has been added'}, 201

    @staticmethod
    def get(doc_id):
        try:
            doc_id = int(doc_id)
        except ValueError:
            return {'message': 'Invalid doctor id'}, 400

        if doc_id == -1:
            validated_msg = validate_token(request.headers, 'M')
            if validated_msg is not None:
                return validated_msg

            user_id = request.headers['user_id']
            results = db.session.query(Doctor, Hospital, HospitalManagement).join(
                Hospital, Hospital.id == Doctor.doc_hospital).join(
                HospitalManagement, HospitalManagement.id == Hospital.management_group).add_columns(
                Doctor.id, Doctor.doc_name, Doctor.doc_mail, Hospital.location,
                HospitalManagement.user_name).filter(HospitalManagement.id == user_id).all()

            if len(results) > 0:
                doctor_list = []
                for result in results:
                    curr_row = {'id': result[-5]}
                    curr_row.update({'doctor_name': result[-4]})
                    curr_row.update({'doctor_email': result[-3]})
                    curr_row.update({'branch': result[-2]})
                    curr_row.update({'hospital': result[-1]})
                    doctor_list.append(curr_row)
                return {'message': {'num_records': len(doctor_list), 'records': doctor_list}}
            return {'message': 'No doctors have been registered yet'}
        else:
            result = db.session.query(Doctor, Hospital, HospitalManagement).join(
                Hospital, Hospital.id == Doctor.doc_hospital).join(
                HospitalManagement, HospitalManagement.id == Hospital.management_group).add_columns(
                Doctor.id, Doctor.doc_name, Doctor.doc_mail, Hospital.location,
                HospitalManagement.user_name).filter(Doctor.id == doc_id).first()
            if result is not None:
                curr_row = {'id': result[-5]}
                curr_row.update({'doctor_name': result[-4]})
                curr_row.update({'branch': result[-2]})
                curr_row.update({'hospital': result[-1]})
                return {'message': curr_row}
            return {'message': 'No doctor found with this id'}


class PatientsData(Resource):
    @staticmethod
    def post(pat_id):
        if pat_id != '0':
            return {'message': 'Patient id needs to be 0 to create new patient'}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Patient name must be specified')
        parser.add_argument('email', type=str, required=True,
                            help='Patient email must be specified')
        parser.add_argument('password', type=str, required=True,
                            help='A password is needed to make account safe')
        args = parser.parse_args()
        try:
            patient = Patient(args['name'], args['email'], args['password'])
            db.session.add(patient)
            db.session.commit()
        except exc.IntegrityError:
            return {'message': 'Email already in use'}, 400
        except:
            return {'message': 'Some unknown error occurred'}, 500
        else:
            return {'message': 'New patient has been added'}, 201

    @staticmethod
    def get(pat_id):
        try:
            pat_id = int(pat_id)
        except ValueError:
            return {'message': 'Invalid patient id'}, 400

        if pat_id == -1:
            patients = Patient.query.all()
            if len(patients) > 0:
                patient_list = []
                for patient in patients:
                    curr_patient = {'id': patient.id}
                    curr_patient.update({'patient_name': patient.pat_name})
                    curr_patient.update({'patient_email': patient.pat_mail})
                    patient_list.append(curr_patient)
                return {'message': {'num_records': len(patient_list), 'records': patient_list}}
            return {'message': 'No patients have been registered yet'}
        else:
            patient = Patient.query.filter(Patient.id == pat_id).first()
            if patient is not None:
                curr_patient = {'id': patient.id}
                curr_patient.update({'patient_name': patient.pat_name})
                return {'message': curr_patient}
            return {'message': 'No patient found with this id'}


class PrescriptionData(Resource):
    @staticmethod
    def post(rx_id):
        validated_msg = validate_token(request.headers, 'P')
        if validated_msg is not None:
            return validated_msg

        user_id = request.headers['user_id']
        if rx_id != '0':
            return {'message': 'Prescription id needs to be 0 to create appointment'}, 400

        parser = reqparse.RequestParser()
        parser.add_argument('doctor', type=int, required=True,
                            help='Doctor id must be specified')
        args = parser.parse_args()
        try:
            prescription = Prescription(args['doctor'], user_id)
            db.session.add(prescription)
            db.session.commit()
        except:
            return {'message': 'Some unknown error occurred'}, 500
        else:
            return {'message': 'Appointment has been generated',
                    'prescription_id': prescription.id}, 201

    @staticmethod
    def get(rx_id):
        try:
            rx_id = int(rx_id)
        except ValueError:
            return {'message': 'Invalid patient id'}, 400

        user_type = None
        if validate_token(request.headers, 'P') is None:
            user_type = 'P'
        elif validate_token(request.headers, 'D') is None:
            user_type = 'D'
        elif validate_token(request.headers, 'M') is None:
            user_type = 'M'
        else:
            return {'message': 'Invalid authentication; Access Denied'}, 401

        user_id = request.headers['user_id']
        if rx_id == -1:
            query = db.session.query(Prescription, Patient, Doctor,
                                     Hospital, HospitalManagement).join(
                Patient, Prescription.pat_id == Patient.id).join(
                Doctor, Prescription.doc_id == Doctor.id).join(
                Hospital, Hospital.id == Doctor.doc_hospital).join(
                HospitalManagement, HospitalManagement.id == Hospital.management_group)
            if user_type == 'P':
                results = query.filter(Prescription.pat_id == user_id).all()
                if len(results) > 0:
                    prescriptions = []
                    for result in results:
                        curr_rx = {'id': result[0].id}
                        curr_rx.update({'date_time':
                                        result[0].dt_tm.strftime('%d %b %Y %H:%M:%S')})
                        curr_rx.update({'doctor': result[2].doc_name})
                        curr_rx.update({'hospital_group': result[4].user_name})
                        curr_rx.update({'branch': result[3].location})
                        curr_rx.update({'disease': result[0].disease})
                        curr_rx.update({'findings': result[0].findings})
                        curr_rx.update({'suggestions': result[0].suggestions})
                        curr_rx.update({'medicines': result[0].medicines})
                        prescriptions.append(curr_rx)
                    return {'message': {'num_records': len(prescriptions), 'records': prescriptions}}
                return {'message': 'No prescriptions found'}
            elif user_type == 'D':
                results = query.filter(Prescription.doc_id == user_id).all()
                if len(results) > 0:
                    prescriptions = []
                    for result in results:
                        curr_rx = {'id': result[0].id}
                        curr_rx.update({'date_time':
                                        result[0].dt_tm.strftime('%d %b %Y %H:%M:%S')})
                        curr_rx.update({'patient': result[1].pat_name})
                        curr_rx.update({'hospital_group': result[4].user_name})
                        curr_rx.update({'branch': result[3].location})
                        curr_rx.update({'disease': result[0].disease})
                        curr_rx.update({'findings': result[0].findings})
                        curr_rx.update({'suggestions': result[0].suggestions})
                        curr_rx.update({'medicines': result[0].medicines})
                        prescriptions.append(curr_rx)
                    return {'message': {'num_records': len(prescriptions), 'records': prescriptions}}
                return {'message': 'No prescriptions found'}
            elif user_type == 'M':
                results = query.filter(HospitalManagement.id == user_id).all()
                if len(results) > 0:
                    prescriptions = []
                    for result in results:
                        curr_rx = {'id': result[0].id}
                        curr_rx.update({'date_time':
                                        result[0].dt_tm.strftime('%d %b %Y %H:%M:%S')})
                        curr_rx.update({'patient': result[1].pat_name})
                        curr_rx.update({'doctor': result[2].doc_name})
                        curr_rx.update({'hospital_group': result[4].user_name})
                        curr_rx.update({'branch': result[3].location})
                        curr_rx.update({'disease': result[0].disease})
                        curr_rx.update({'findings': result[0].findings})
                        curr_rx.update({'suggestions': result[0].suggestions})
                        curr_rx.update({'medicines': result[0].medicines})
                        prescriptions.append(curr_rx)
                    return {'message': {'num_records': len(prescriptions), 'records': prescriptions}}
                return {'message': 'No prescriptions found'}
        else:
            query = db.session.query(Prescription, Patient, Doctor,
                                     Hospital, HospitalManagement).join(
                Patient, Prescription.pat_id == Patient.id).join(
                Doctor, Prescription.doc_id == Doctor.id).join(
                Hospital, Hospital.id == Doctor.doc_hospital).join(
                HospitalManagement, HospitalManagement.id == Hospital.management_group)
            if user_type == 'P':
                result = query.filter(Prescription.pat_id == user_id,
                                      Prescription.id == rx_id).first()
                if result is not None:
                    curr_rx = {'id': result[0].id}
                    curr_rx.update({'date_time':
                                    result[0].dt_tm.strftime('%d %b %Y %H:%M:%S')})
                    curr_rx.update({'doctor': result[2].doc_name})
                    curr_rx.update({'hospital_group': result[4].user_name})
                    curr_rx.update({'branch': result[3].location})
                    curr_rx.update({'disease': result[0].disease})
                    curr_rx.update({'findings': result[0].findings})
                    curr_rx.update({'suggestions': result[0].suggestions})
                    curr_rx.update({'medicines': result[0].medicines})
                    return {'message': curr_rx}
                return {'message': 'No prescriptions found'}
            elif user_type == 'D':
                result = query.filter(Prescription.doc_id == user_id,
                                      Prescription.id == rx_id).first()
                if result is not None:
                    curr_rx = {'id': result[0].id}
                    curr_rx.update({'date_time':
                                    result[0].dt_tm.strftime('%d %b %Y %H:%M:%S')})
                    curr_rx.update({'patient': result[1].pat_name})
                    curr_rx.update({'hospital_group': result[4].user_name})
                    curr_rx.update({'branch': result[3].location})
                    curr_rx.update({'disease': result[0].disease})
                    curr_rx.update({'findings': result[0].findings})
                    curr_rx.update({'suggestions': result[0].suggestions})
                    curr_rx.update({'medicines': result[0].medicines})
                    return {'message': curr_rx}
                return {'message': 'No prescriptions found'}
            elif user_type == 'M':
                result = query.filter(HospitalManagement.id == user_id,
                                      Prescription.id == rx_id).first()
                if result is not None:
                    curr_rx = {'id': result[0].id}
                    curr_rx.update({'date_time':
                                    result[0].dt_tm.strftime('%d %b %Y %H:%M:%S')})
                    curr_rx.update({'patient': result[1].pat_name})
                    curr_rx.update({'doctor': result[2].doc_name})
                    curr_rx.update({'hospital_group': result[4].user_name})
                    curr_rx.update({'branch': result[3].location})
                    curr_rx.update({'disease': result[0].disease})
                    curr_rx.update({'findings': result[0].findings})
                    curr_rx.update({'suggestions': result[0].suggestions})
                    curr_rx.update({'medicines': result[0].medicines})
                    return {'message': curr_rx}
                return {'message': 'No prescriptions found'}

    @staticmethod
    def put(rx_id):
        try:
            rx_id = int(rx_id)
        except ValueError:
            return {'message': 'Invalid patient id'}, 400

        validated_msg = validate_token(request.headers, 'D')
        if validated_msg is not None:
            return validated_msg

        user_id = request.headers['user_id']
        parser = reqparse.RequestParser()
        parser.add_argument('disease', type=str, required=True,
                            help='Disease must be specified')
        parser.add_argument('findings', type=str, required=True,
                            help='Findings must be specified')
        parser.add_argument('suggestions', type=str, required=True,
                            help='Suggestions must be specified')
        parser.add_argument('medicines', type=str, required=True,
                            help='Medicines must be specified')
        args = parser.parse_args()
        try:
            prescription = Prescription.query.get(rx_id)
            prescription.disease = args['disease']
            prescription.findings = args['findings']
            prescription.suggestions = args['suggestions']
            prescription.medicines = args['medicines']
            db.session.commit()
        except:
            return {'message': 'Some unknown error occurred'}, 500
        else:
            return {'message': 'Prescription provided to patient'}


if __name__ == '__main__':
    db.init_app(app)
    api.add_resource(HospitalManager, '/manage-hospital')
    api.add_resource(Login, '/login')
    api.add_resource(HospitalBranch, '/hospital-branch')
    api.add_resource(PatientsData, '/patient/<string:pat_id>')
    api.add_resource(DoctorsData, '/doctor/<string:doc_id>')
    api.add_resource(PrescriptionData, '/appointment/<string:rx_id>')
    app.run('0.0.0.0', 5555)
