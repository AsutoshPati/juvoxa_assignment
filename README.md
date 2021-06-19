# Juvoxa assignment
This task has been completed by [Asutosh Pati](https://www.linkedin.com/in/asutoshpati/). This repository can only be
used for review of the assignment by Juvoxa team as a part of recruitment process.
---

## Requirements
* pgadmin 4
* python packages are available in [requirements.txt](./requirements.txt)

## How to use
* Install pgadmin 4 on your system; and note down the user and its corresponding password to access postgresql server.
* Create a database and note down the database name.
* Download this repository and store all python files under a single directory.
* Install required python packages by creating a virtual environment or to the base directory based on your choice.
* Now open [main.py](./main.py) and give your postgres username, password, database name & host at specified place.
* Once above steps are completed; now you are good to go. Just run the [main.py](./main.py).
* After running the [main.py](./main.py) you can start using the api. For your reference 
  [postman collection](https://documenter.getpostman.com/view/14283218/TzeZDRaY) 
  (https://documenter.getpostman.com/view/14283218/TzeZDRaY) has been 
  provided. Please download the collection and start using it.
  
## API
* ### Required API (Hospital)
  * #### Create a new hospital management
    API link -
    > http://127.0.0.1:5555/manage-hospital

    HTTP method - **POST**

    Description - 
    By using this API a hospital management/group can be created which will be further used to onboard a new hospital 
    branch and doctors   
    
    Header parameters -
    ```js
    Content-Type : application/json
    ```
  
    Body parameters -
    ```json
    {
      "management_name": "KIMS group",
      "management_mail": "kims@gmail.com",
      "management_pwd": "kims_pwd"
    }
    ```
    
    Success Response
    
    status code - **201**
    ```json
    {
        "message": "New hospital group added"
    }
    ```
    
  * #### Login for hospital management
    API link -
    > http://127.0.0.1:5555/login

    HTTP method - **POST**

    Description - 
    By using this API a hospital management/group can log in to their account.
    
    Header parameters -
    ```js
    Content-Type : application/json
    ```
  
    Body parameters -
    ```json
    {
      "email": "kims@gmail.com",
      "password": "kims_pwd"
    }
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "user_id": 1,
      "user_token": "2bcc3060",
      "user_type": "M"
    }
    ```
    
  * #### Onboard a new hospital
    API link -
    > http://127.0.0.1:5555/hospital-branch

    HTTP method - **POST**

    Description - 
    By using this API a hospital management/group can create a hospital branch.
    
    Header parameters -
    ```js
    Content-Type : application/json
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```json
    {
      "address": "Patia, Bhubaneswar"
    }
    ```
    
    Success Response
    
    status code - **201**
    ```json
    {
      "message": "New hospital branch added"
    }
    ```
    
  * #### Onboard a doctor
    API link -
    > http://127.0.0.1:5555/doctor/0

    HTTP method - **POST**

    Description - 
    By using this API a hospital management/group can add a new doctor in a hospital branch.
    
    Header parameters -
    ```js
    Content-Type : application/json
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```json
    {
      "name": "Doctor Babu",
      "email": "doctor.shahab@gmail.com",
      "password": "doc_pwd",
      "branch": 1
    }
    ```
    
    Success Response
    
    status code - **201**
    ```json
    {
      "message": "New doctor has been added"
    }
    ```
    
  * #### List all doctors
    API link -
    > http://127.0.0.1:5555/doctor/-1

    HTTP method - **GET**

    Description - 
    By using this API all doctors details from all branches of a specific hospital management/group.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 2,
          "records": [
              {
                  "id": 1,
                  "doctor_name": "Doctor Babu",
                  "doctor_email": "doctor.sahab@gmail.com",
                  "branch": "Patia, Bhubaneswar",
                  "hospital": "KIMS group"
              },
              {
                  "id": 2,
                  "doctor_name": "Mera Doctor",
                  "doctor_email": "mera.doctor@gmail.com",
                  "branch": "Bermunda, Bhubaneswar",
                  "hospital": "KIMS group"
              }
          ]
      }
    }
    ```
    
* ### Required API (Patient)
  * #### New Patient
    API link -
    > http://127.0.0.1:5555/patient/0

    HTTP method - **POST**

    Description - 
    By using this API a patient can be registered in the platform.  
    
    Header parameters -
    ```js
    Content-Type : application/json
    ```
  
    Body parameters -
    ```json
    {
      "name": "Asutosh Pati",
      "email": "asutosh.test@gmail.com",
      "password": "asu_pwd"
    }
    ```
    
    Success Response
    
    status code - **201**
    ```json
    {
      "message": "New patient has been added"
    }
    ```
    
  * #### Patient login
    API link -
    > http://127.0.0.1:5555/login

    HTTP method - **POST**

    Description - 
    By using this API a patient can log in to their account.
    
    Header parameters -
    ```js
    Content-Type : application/json
    ```
  
    Body parameters -
    ```json
    {
      "email": "asutosh.test@gmail.com",
      "password": "asu_pwd"
    }
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "user_id": 1,
      "user_token": "c729fac3",
      "user_type": "P"
    }
    ```
    
  * #### Generate appointment
    API link -
    > http://127.0.0.1:5555/doctor/0

    HTTP method - **POST**

    Description - 
    By using this API a patient can generate appointment with a doctor.
    
    Header parameters -
    ```js
    Content-Type : application/json
    user_id : 1 <user id got from login response>
    user_token: c729fac3 <user token from login response>
    ```
  
    Body parameters -
    ```json
    {
      "doctor": 1
    }
    ```
    
    Success Response
    
    status code - **201**
    ```json
    {
      "message": "Appointment has been generated",
      "prescription_id": 1
    }
    ```
    
  * #### View prescriptions / doctor visits / hospital visits
    API link -
    > http://127.0.0.1:5555/appointment/-1

    HTTP method - **GET**

    Description - 
    By using this API all prescriptions from the specific patient will be shown.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: c729fac3 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 1,
          "records": [
              {
                  "id": 1,
                  "date_time": "19 Jun 2021 14:39:08",
                  "doctor": "Doctor Babu",
                  "hospital_group": "KIMS group",
                  "branch": "Patia, Bhubaneswar",
                  "disease": "Malaria",
                  "findings": "high fever",
                  "suggestions": "bed rest",
                  "medicines": "hydroxy chloroquine 10TAB"
              }
          ]
      }
    }
    ```

* ### Required API (Doctor)
  * #### Doctor login
    API link -
    > http://127.0.0.1:5555/login

    HTTP method - **POST**

    Description - 
    By using this API a doctor can log in to their account.
    
    Header parameters -
    ```js
    Content-Type : application/json
    ```
  
    Body parameters -
    ```json
    {
      "email": "doctor.sahab@gmail.com",
      "password": "doc_pwd"
    }
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "user_id": 1,
      "user_token": "f2ff0697",
      "user_type": "D"
    }
    ``` 
    
  * #### Give prescription
    API link -
    > http://127.0.0.1:5555/appointment/1<prescription-id>

    HTTP method - **PUT**

    Description - 
    By using this API a doctor can give prescription to assigned patient.
    
    Header parameters -
    ```js
    Content-Type : application/json
    user_id : 1 <user id got from login response>
    user_token: f2ff0697 <user token from login response>
    ```
  
    Body parameters -
    ```json
    {
      "disease": "Malaria",
      "findings": "high fever",
      "suggestions": "bed rest",
      "medicines": "hydroxy chloroquine 10TAB"
    }
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": "Prescription provided to patient"
    }
    ```
    
  * #### View prescribed patients
    API link -
    > http://127.0.0.1:5555/appointment/-1

    HTTP method - **GET**

    Description - 
    By using this API all prescribed patients will be shown.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: f2ff0697 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 1,
          "records": [
              {
                  "id": 1,
                  "date_time": "19 Jun 2021 14:39:08",
                  "patient": "Asutosh Pati",
                  "hospital_group": "KIMS group",
                  "branch": "Patia, Bhubaneswar",
                  "disease": "Malaria",
                  "findings": "high fever",
                  "suggestions": "bed rest",
                  "medicines": "hydroxy chloroquine 10TAB"
              }
          ]
      }
    }
    ```
    
  * #### View prescription of patients
    API link -
    > http://127.0.0.1:5555/appointment/1<prescription-id>

    HTTP method - **GET**

    Description - 
    By using this API prescription can be shown for a specific prescription id.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: f2ff0697 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "id": 1,
          "date_time": "19 Jun 2021 14:39:08",
          "patient": "Asutosh Pati",
          "hospital_group": "KIMS group",
          "branch": "Patia, Bhubaneswar",
          "disease": "Malaria",
          "findings": "high fever",
          "suggestions": "bed rest",
          "medicines": "hydroxy chloroquine 10TAB"
      }
    }
    ```
  
* ### Bonus API
  * #### All hospital management/group
    API link -
    > http://127.0.0.1:5555/manage-hospital

    HTTP method - **GET**

    Description - 
    By using this API all hospital management/group details will be shown.
    
    Header parameters -
    ```js
    None
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 1,
          "records": [
              {
                  "id": 1,
                  "management_name": "KIMS group",
                  "management_email": "kims@gmail.com"
              }
          ]
      }
    }
    ```
    
  * #### All hospital branches
    API link -
    > http://127.0.0.1:5555/manage-hospital

    HTTP method - **GET**

    Description - 
    By using this API all branches under a hospital management/group will be shown.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_branches": 2,
          "branches": [
              {
                  "id": 1,
                  "Address": "Patia, Bhubaneswar"
              },
              {
                  "id": 2,
                  "Address": "Bermunda, Bhubaneswar"
              }
          ]
      }
    }
    ```
    
  * #### Doctor info
    API link -
    > http://127.0.0.1:5555/doctor/-1

    HTTP method - **GET**

    Description - 
    By using this API all doctors details will be shown under a hospital management/group.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 2,
          "records": [
              {
                  "id": 1,
                  "doctor_name": "Doctor Babu",
                  "doctor_email": "doctor.sahab@gmail.com",
                  "branch": "Patia, Bhubaneswar",
                  "hospital": "KIMS group"
              },
              {
                  "id": 2,
                  "doctor_name": "Mera Doctor",
                  "doctor_email": "mera.doctor@gmail.com",
                  "branch": "Bermunda, Bhubaneswar",
                  "hospital": "KIMS group"
              }
          ]
      }
    }
    ```
    
  * #### Registered patients
    > http://127.0.0.1:5555/patient/-1

    HTTP method - **GET**

    Description - 
    By using this API all patients details will be shown.
    
    Header parameters -
    ```js
    None
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 1,
          "records": [
              {
                  "id": 1,
                  "patient_name": "Asutosh Pati",
                  "patient_email": "asutosh.test@gmail.com"
              }
          ]
      }
    }
    ```
    
  * #### Prescription list
    API link -
    > http://127.0.0.1:5555/appointment/-1

    HTTP method - **GET**

    Description - 
    By using this API all prescriptions will be shown by user type; if user is from management, all prescriptions from
    same hospital group / management will be shown. if user is a doctor, all prescriptions will be shown given by the 
    doctor. if user is a patient, all prescriptions will be shown generated by patient.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "num_records": 1,
          "records": [
              {
                  "id": 1,
                  "date_time": "19 Jun 2021 14:39:08",
                  "patient": "Asutosh Pati",
                  "doctor": "Doctor Babu",
                  "hospital_group": "KIMS group",
                  "branch": "Patia, Bhubaneswar",
                  "disease": "Malaria",
                  "findings": "high fever",
                  "suggestions": "bed rest",
                  "medicines": "hydroxy chloroquine 10TAB"
              }
          ]
      }
    }
    ```
    
  * #### Single prescription
    API link -
    > http://127.0.0.1:5555/appointment/1<prescription-id>

    HTTP method - **GET**

    Description - 
    By using this API prescription will be shown by user type; if user is from management, if prescribed from same
    hospital group / management will be shown. if user is a doctor, if prescribed by doctor will be shown. if user is a
    patient, if prescription belongs to the patient will be shown.
    
    Header parameters -
    ```js
    user_id : 1 <user id got from login response>
    user_token: 2bcc3060 <user token from login response>
    ```
  
    Body parameters -
    ```js
    None
    ```
    
    Success Response
    
    status code - **200**
    ```json
    {
      "message": {
          "id": 1,
          "date_time": "19 Jun 2021 14:39:08",
          "patient": "Asutosh Pati",
          "doctor": "Doctor Babu",
          "hospital_group": "KIMS group",
          "branch": "Patia, Bhubaneswar",
          "disease": "Malaria",
          "findings": "high fever",
          "suggestions": "bed rest",
          "medicines": "hydroxy chloroquine 10TAB"
      }
    }
    ```

## How to use
**Alternatively you can use [juvoxa_task](./juvoxa_task) file to get mu test data. Just import it in pgadmin4**
* Create a hospital management/group.
* Create hospital branches under hospital management/group; after logging in with hospital management/group user.
* Add doctors to hospital branches; after logging in with hospital management/group user.
* Register new patients.
* Generate an appointment with a doctor; after logging in with patient user.
* Now a doctor can give prescription on a generated appointment; after logging in with doctor user.
* Prescription will be shown dynamically for each type of user; based on which type of user is logged in.

## Architecture decision
**The project architecture has been designed by keeping simplicity, optimization and basic requirements in mind.**

* First the requirement has been analysed. According to the requirements models have been decided and relationship
  between models has been decided.
  
* Hospital Management needed to create hospital branches as well as to onboard doctors to a specific branch. Because a 
  hospital management can have their hospital branches at different locations.
  
* Hospital branch is needed to store the location and other details about that particular branch. By keeping simplicity 
  into mind only the location has been stored.
  
* Coming to the doctor; doctor can give prescription which is in middle of the whole project.

* A patient is much more needed who can take appointment with a doctor and get prescribed by a doctor.

![ER diagram of database](./md%20images/ER%20db.JPG)