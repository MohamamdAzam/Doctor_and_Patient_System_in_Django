from django.db import models
from django.contrib.auth.models import User

# Create your models here.
blood_group=[('-A','-A'),
('+A','+A'),
('-B','-B'),
('+B','+B'),
('-AB','-AB'),
('+AB','+AB'),
('-O','-O'),
('+O','+O'),
]

gender=[('Male','Male'),
('Female','Female'),
('Other','Other'),
]

class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blood_group = models.CharField(max_length=10,choices=blood_group,null=True)
    health_uid = models.CharField(max_length=16,null=True)
    ex_year= models.CharField(max_length=10,null=True)
    ex_month= models.CharField(max_length=10,null=True)
    cvv = models.CharField(max_length=10,null=True)
    mobile = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=100,null=True)
    card_status = models.CharField(max_length=100,null=True)
    dob = models.DateField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    status = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    specialist = models.CharField(max_length=100, null=True)
    service = models.CharField(max_length=100, null=True)
    clinic = models.CharField(max_length=100, null=True)
    cl_address = models.CharField(max_length=100, null=True)
    daystiming = models.CharField(max_length=100, null=True)
    timing = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=100,choices=gender,null=True)
    biography = models.TextField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username

class Hospital(models.Model):
    status = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100, null=True)
    nom_doctor = models.CharField(max_length=100, null=True)
    nom_beds = models.CharField(max_length=100, null=True)
    foundation_date = models.DateField(null=True)
    timing = models.CharField(max_length=100, null=True)
    owner_name = models.CharField(max_length=100, null=True)
    days_time = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    biography = models.TextField(null=True)
    image = models.FileField(null=True)

    def _str_(self):
        return self.user.username

class Medical(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100,null=True)
    days_time = models.CharField(max_length=100, null=True)
    timing = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    foundation_date = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)

    def _str_(self):
        return self.name

class Appointment(models.Model):
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    medical=models.ForeignKey(Medical, on_delete=models.CASCADE, null=True)
    a_date=models.DateField(null=True)
    a_timing=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    p_status=models.CharField(max_length=100,null=True)

    def _str_(self):
        return self.doctor.user.username+" "+self.patient.user.username

class Hospital_Appointment(models.Model):
    hospital=models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    a_date=models.DateField(null=True)
    a_timing=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,null=True)
    p_status=models.CharField(max_length=100,null=True)
    price=models.CharField(max_length=100,null=True)

    def str(self):
        return self.hospital.name+" "+self.patient.user.username

class Doctors_Invoice(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    medicine = models.CharField(max_length=100,null=True)
    prescription = models.CharField(max_length=100,null=True)
    price = models.CharField(max_length=100,null=True)

    def _str_(self):
        return self.apponitment.doctor.user.username + " " + self.apponitment.patient.user.username + " " + self.medicine


class Adminstration(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.user.username

class Prescription(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.CharField(max_length=100,null=True,blank=True)
    days = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    price = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.appoint.doctor.user.username+" "+self.appoint.patient.user.username

class Medical_Record(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    disc = models.CharField(max_length=100,null=True,blank=True)
    file = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.appoint.doctor.user.username+" "+self.appoint.patient.user.username

class Billing_Record(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    amount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.appoint.doctor.user.username+" "+self.appoint.patient.user.username