from django.db import models

# Create your models here.
class patient_data(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=10)
    gender = models.CharField(max_length=200)
    medical_issue = models.CharField(max_length=200)
    doctor_name = models.CharField(max_length=200)
    appointment_date = models.CharField(max_length=200)
    appt_time = models.CharField(max_length=200)
    # appointment_date = models.DateField(auto_now_add=True)
    # appt_time = models.TimeField(auto_now_add=True)
    mbl = models.CharField( max_length=13)

    def __str__(self) -> str:
        return self.name

# CREATE DATABASE HMS;
# USE HMS;

# CREATE TABLE Patient(
#     appointmentdate date,
#     appttime time primary key,
#     name varachar(50),
#     age int(50),
#     gender varchar(40),
#     medicalissue varchar(50),
# );

# CREATE TABLE Doctor(
#     name varchar(50),
#     gender varchar(50),
# );