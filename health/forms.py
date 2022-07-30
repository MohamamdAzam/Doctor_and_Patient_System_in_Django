from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['blood_group','mobile','address','dob','image']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['experience','specialist','service','clinic','cl_address','daystiming','timing','gender','biography','mobile','address','dob','image','price']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['a_date','a_timing','status','p_status']

class Hospital_AppointmentForm(forms.ModelForm):
    class Meta:
        model = Hospital_Appointment
        fields = ['a_date','a_timing','status','p_status']

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['mobile','name','nom_doctor','nom_beds','foundation_date','timing','owner_name','days_time','address','image','biography']


class MedicalForm(forms.ModelForm):
    class Meta:
        model = Medical
        fields = ['mobile','name','foundation_date','timing','days_time','address','image','experience']

