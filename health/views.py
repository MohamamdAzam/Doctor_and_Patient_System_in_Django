from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import *
import datetime
import uuid
import random
from django.db.models import Avg,Sum,Count,Min,Max

from datetime import timedelta

# Create your views here.
def access(user):
    try:
        user = Doctor.objects.get(user=user)
        if user.status == "pending":
            return False
        else:
            return True
    except:
        try:
            user = Medical.objects.get(user=user)
            if user.status == "pending":
                return False
            else:
                return True
        except:
            try:
                user = Hospital.objects.get(user=user)
                if user.status == "pending":
                    return False
                else:
                    return True
            except:
                pass



def patient_dashboard(request):
    pat = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'patient/patient_dashboard.html',d)

def all_hospital_appointment(request):
    pat = Hospital_Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'patient/all_hospital_appointment.html',d)

def all_doctor_appointment(request):
    pat = Appointment.objects.filter(patient=Patient.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'patient/all_doctor_appointment.html',d)

def all_patient_appointment(request):
    pat = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'doctor/all_patient_appointment.html',d)

def all_patient_invoices(request):
    pat = Appointment.objects.filter(medical=Medical.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'medical/all_patient_invoices.html',d)

def hospital_view_invoices(request):
    pat = Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user))
    d = {'data':pat}
    return render(request,'hospital/hospital_view_invoices.html',d)

def doctor_dashboard(request):
    tod = datetime.date.today()
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user))
    pend = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    c = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user)).count()
    up = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date__gte=tod).exclude(a_date=tod)
    today = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user), a_date=tod)
    t_today = today.count()
    t_pending = pend.count()
    d = {'data': data, 'total': c, 'up': up, 'today': today,'t_today':t_today,'t_pending':t_pending}
    return render(request,'doctor/doctor_dashboard.html',d)

def hospital_dashboard(request):
    tod=datetime.date.today()
    data=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user))
    pend=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),status="pending")
    c=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user)).count()
    up=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),a_date__gte=tod).exclude(a_date=tod)
    today=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),a_date=tod)
    t_today = today.count()
    t_pending = pend.count()
    d={'data':data,'total':c,'up':up,'today':today,'t_today':t_today,'t_pending':t_pending}
    return render(request,'hospital/hospital_dashboard.html',d)

def medical_dashboard(request):
    return render(request,'medical/medical_dashboard.html')

def home(request):
    data=Doctor.objects.all()
    doc = ""
    if request.method == "POST":
        l = request.POST['loc']
        s = request.POST['spe']
        if l and s:
            doc  = Doctor.objects.filter(cl_address__icontains = l,specialist__icontains = s)
        elif not l and s:
            doc  = Doctor.objects.filter(specialist__icontains = s)
        elif l and not s:
            doc  = Doctor.objects.filter(cl_address__icontains = l)
        else:
            doc = Doctor.objects.all()
    try:
        user = User.objects.get(username=request.user)
        error = Patient.objects.get(user=user)
        return redirect('patient_dashboard')
    except:
        try:
            user = User.objects.get(username=request.user)
            error = Doctor.objects.get(user=user)
            return redirect('doctor_dashboard')
        except:
            try:
                user = User.objects.get(username=request.user)
                error = Hospital.objects.get(user=user)
                return redirect('hospital_dashboard')
            except:
                try:
                    user = User.objects.get(username=request.user)
                    error = Medical.objects.get(user=user)
                    return redirect('medical_dashboard')
                except:
                    try:
                        user = User.objects.get(username=request.user)
                        if user.is_staff:
                            return redirect('admin_dashboard')
                    except:
                        pass
    d={'data':data,'doc':doc}
    return render(request,'index.html',d)

def Registeration(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            m = request.POST['mode']
            if m == "Patient":
                Patient.objects.create(user=user)
            if m == "Doctor":
                Doctor.objects.create(user=user,status="pending")
            if m == "Hospital":
                Hospital.objects.create(user=user,status="pending")
            if m == "Medical":
                Medical.objects.create(user=user,status="pending")
            messages.success(request,'You have Registered Successfully')
            return redirect('login')
    else:
        form = SignUpForm()
    d = {'form':form}
    return render(request,'register.html',d)

def Login(request):
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in Successfully')
            return redirect('home')
        else:
            messages.success(request,'Invalid Credential')
            return redirect('login')
    return render(request,'login.html')

def Logout(request):
    logout(request)
    messages.info(request,'You have logged out successfully')
    return redirect('login')

def Patient_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Patient.objects.get(user=user)
    form = PatientForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = PatientForm(request.POST,request.FILES,instance=pat)
        if form.is_valid():
            
            try:
                
                for s in [request.POST['first_name'],request.POST['last_name']]:  
                    for ch in s:
                        if not ch.isalpha():
                            return messages.success(request,'Please enter valid name')
            except:
                pass
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("patient_profile")
    d = {'form':form}
    return render(request,'patient/profile.html',d)

def Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("change_password")
    return render(request,'patient/change_password.html')

def Doctor_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Doctor.objects.get(user=user)
    form = DoctorForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = DoctorForm(request.POST or None,request.FILES or None, instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("doctor_profile")
    d = {'doc':pat,'form':form}
    return render(request,'doctor/profile.html',d)

def Doctor_Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("change_password")
    return render(request,'doctor/change_password.html')

def search_doctor(request):
    data = Doctor.objects.all()
    l = "All"
    g = "All"
    s = "All"
    if request.method == "POST":
        l = ""
        s = ""
        g = ""
        try:
            l = request.POST['location']
        except:
            pass
        try:
            g = request.POST['gender_type']
        except:
            pass
        try:
            s = request.POST['specialist']
        except:
            pass
        data = Doctor.objects.filter(gender__icontains=g,specialist__icontains=s,cl_address__icontains=l)
    d={'data':data,'l':l,'g':g,'s':s}
    return render(request,'patient/search_doctor.html',d)

def appointment(request,pid):
    doctor=Doctor.objects.get(id=pid)
    if request.method == "POST":
        a = request.POST['a_date']
        app=Appointment.objects.create(doctor=doctor,patient=Patient.objects.get(user=request.user),a_date=a,status="pending",p_status="pending")
        messages.success(request,"Appointment Request Sent Successfully")
        return redirect("payment",app.id)
    d={'doctor':doctor}
    return render(request,'patient/appointment.html',d)

def payment(request,pid):
    data=Appointment.objects.get(id=pid)
    if request.method=="POST":
        data.p_status="complete"
        data.save()
        messages.success(request,"Payment Completed Successfully")
        return redirect("booking-success",data.id)
    d={'data':data}
    return render(request,'patient/payment.html',d)

def payment_success(request,pid):
    data=Appointment.objects.get(id=pid)
    d={'data':data}
    return render(request,'patient/booking-success.html',d)

def p_appointment(request):
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="pending")
    d={'data':data}
    return render(request,'patient/p_appoinment.html',d)

def d_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="pending")
    d={'data':data}
    return render(request,'doctor/d_appoinment.html',d)

def update_status(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=Appointment.objects.get(id=pid)
    form=AppointmentForm(request.POST or None,instance=data)
    if request.method=="POST":
        u=request.POST['a_date']
        v=request.POST['a_timing']
        data.a_date=u
        data.a_timing=v
        data.status="confirmed"
        data.save()
        messages.success(request,"Payment Completed Successfully")
        return redirect("d_appointment")
    d={'form':form,'data':data}
    return render(request,'doctor/update_status.html',d)

def confirmed_p_appointment(request):
    tod=datetime.date.today()
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    return render(request,'patient/confirmed_p_appoinment.html',d)

def confirmed_d_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    tod=datetime.date.today()
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    return render(request,'doctor/confirmed_d_appoinment.html',d)

def history_p_appointment(request):
    tod=datetime.date.today()
    data=Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'patient/history_p_appoinment.html',d)

def add_medicine(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data  = Appointment.objects.get(id=pid)
    med = Doctors_Invoice.objects.filter(appointment=data)
    if request.method == "POST":
        m = request.POST['name']
        p = request.POST['presc']
        Doctors_Invoice.objects.create(appointment=data,medicine=m,prescription=p)
        messages.success(request,'One Medicine added')
        return redirect('add_medicine',data.id)
    d = {'med':med}
    return render(request,'doctor/add_medicine.html',d)

def history_d_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    tod=datetime.date.today()
    data=Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'doctor/history_d_appoinment.html',d)

def p_search_appointment(request):
    data=""
    u = ""
    v = ""
    if request.method=="POST":
        u=request.POST['from_date']
        v=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(u)
        i2 = datetime.datetime.fromisoformat(v)
        data = Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    d={'data':data,'u':u,'v':v}
    return render(request,'patient/p_search_appoinment.html',d)

def Login_Admin(request):
    error = False
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = True
    d = {'error': error}

    return render(request, 'login.html', d)

def admin_dashboard(request):
    t_doc = Doctor.objects.all().count()
    t_pat = Patient.objects.all().count()
    t_hos = Hospital_Appointment.objects.all().count()
    t_app2 = Appointment.objects.all().count()
    d = {'t_doc':t_doc,'t_pat':t_pat,'t_hos':t_hos,'t_app2':t_app2}
    return render(request,'admin/admin_dashboard.html',d)

def admin_view_appointment(request):
    data=Appointment.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_appointment.html',d)


def admin_hospital_appointment(request):
    data=Hospital_Appointment.objects.all()
    d={'data':data}
    return render(request,'admin/admin_hospital_appointment.html',d)

def admin_view_doctors(request):
    data=Doctor.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_doctors.html',d)

def admin_view_patients(request):
    data=Patient.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_patients.html',d)

def generate_uid():
    uid_no = ""
    digits = [0] * 10
    for i in range(10000):
        x = str(uuid.uuid4().int)[:4]
        for d in x:
            digits[int(d)] += 1
    for i in digits[:4]:
        uid_no+=str(i)
    return uid_no

def health_card(request):
    data=Patient.objects.get(user = request.user)
    if data.health_uid == None:
        while 1:
            uid_no = generate_uid()
            pat = Patient.objects.filter(health_uid=uid_no)
            if pat:
                continue
            else:
                data.health_uid = uid_no
                num = random.randrange(1, 10**3)
                cv_no = str(random.randrange(1, 10**3))
                if len(cv_no) == 2:
                    data.cvv = "1"+cv_no
                elif len(cv_no) == 1:
                    data.cvv = "1"+cv_no+"2"
                elif len(cv_no) == 0:
                    data.cvv = "123"
                else:
                    data.cvv = cv_no
                data.ex_month = int(datetime.date.today().month)
                data.ex_year = int(datetime.date.today().year) + 5
                data.save()
                break
    first = data.health_uid[:4]
    second = data.health_uid[4:8]
    third = data.health_uid[8:12]
    fourth = data.health_uid[12:16]
    d={'data':data,'first':first,'second':second,'third':third,'fourth':fourth}
    return render(request,'patient/health_card.html',d)

def apply_card(request):
    return render(request,'patient/apply_card.html')

def thank_card(request):
    user = Patient.objects.get(user=request.user)
    user.card_status ="pending"
    user.save()
    return render(request,'patient/thank_card.html')

def request_health_card(request):
    pat = Patient.objects.filter(card_status="pending")
    d = {'data':pat}
    return render(request,'admin/request_health_card.html',d)

def grant_card(request,pid):
    pat = Patient.objects.get(id=pid)
    pat.card_status = "accepted"
    pat.save()
    messages.success(request,"You have successfully given to access for health card to "+pat.user.username+ ".!")
    return redirect('all_card_user')

def card_cancelation(request,pid):
    pat = Patient.objects.get(id=pid)
    pat.card_status = None
    pat.health_uid = None
    pat.ex_month = None
    pat.ex_year = None
    pat.cvv = None
    pat.save()
    messages.success(request,"You have successfully Canceled to health card of "+pat.user.username+ ".!")
    return redirect('all_card_user')

def all_card_user(request):
    pat = Patient.objects.filter(card_status="accepted")
    d = {'data':pat}
    return render(request,'admin/all_card_user.html',d)

def cancel_appointment(request,pid):
    pat = Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('p_appointment')


def doctor_cancel_appointment(request,pid):
    pat = Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('d_appointment')

def cancel_hospital_appointment(request,pid):
    pat = Hospital_Appointment.objects.get(id=pid)
    pat.delete()
    messages.success(request,'Appointment Cancelled Successfully')
    return redirect('h_appointment')

def patient_invoices(request,pid,task):
    pat = Appointment.objects.get(id=pid)
    data=""
    total = 0
    try:
        data = Billing_Record.objects.filter(appoint=pat)
        total = str(data.aggregate(Sum('amount')))[14:][:-1]
    except:
        pass
    med = Doctors_Invoice.objects.filter(appointment=pat)
    total1 = str(med.aggregate(Sum('price')))[14:][:-1]
    d = {'pat':pat,'med':med,'total':total,'task':task}
    return render(request,'invoices.html',d)


def admin_patient_invoices(request,pid):
    pat = Appointment.objects.get(id=pid)
    med = Prescription.objects.filter(appoint=pat)
    total = str(med.aggregate(Sum('price')))[14:][:-1]
    d = {'pat':pat,'med':med,'total':total}
    return render(request,'admin/doctor_invoices.html',d)

def admin_hospital_invoices(request,pid):
    pat = Hospital_Appointment.objects.get(id=pid)
    d = {'pat':pat}
    return render(request,'admin/hospital_invoice.html',d)

def patient_hospital_invoices(request,pid):
    pat = Hospital_Appointment.objects.get(id=pid)
    d = {'pat':pat}
    return render(request,'patient/hospital_invoice.html',d)


def Hospital_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Hospital.objects.get(user=user)
    form = HospitalForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = HospitalForm(request.POST or None,request.FILES or None, instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("hospital_profile")
    d = {'doc':pat,'form':form}
    return render(request,'hospital/profile.html',d)


def Hospital_Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("hospital_change_password")
    return render(request,'hospital/change_password.html')


def search_hospital(request):
    data = Hospital.objects.all()
    l = "All"
    n = "All"
    if request.method == "POST":
        l = ""
        n = ""
        try:
            l = request.POST['address']
        except:
            pass
        try:
            n = request.POST['name']
        except:
            pass
        data = Hospital.objects.filter(address__icontains=l,name__icontains=n,)
    d={'data':data,'l':l,'n':n,}
    return render(request,'patient/search_hospital.html',d)

def hospital_appointment(request,pid):
    hospital=Hospital.objects.get(id=pid)
    if request.method == "POST":
        a = request.POST['a_date']
        app=Hospital_Appointment.objects.create(hospital=hospital,patient=Patient.objects.get(user=request.user),a_date=a,status="pending",p_status="pending")
        messages.success(request,"Appointment Request Sent Successfully")
        return redirect("hospital_payment",app.id)
    d={'hospital':hospital}
    return render(request,'patient/hospital_appointment.html',d)

def hospital_payment(request,pid):
    data=Hospital_Appointment.objects.get(id=pid)
    if request.method=="POST":
        data.p_status="complete"
        data.save()
        messages.success(request,"Payment Completed Successfully")
        return redirect("hospital_booking-success",data.id)
    d={'data':data}
    return render(request,'patient/hospital_payment.html',d)

def hospital_payment_success(request,pid):
    data=Hospital_Appointment.objects.get(id=pid)
    d={'data':data}
    return render(request,'patient/hospital_booking-success.html',d)

def hospital_view_appintment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('hospital_profile')
    data=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),status="pending",)
    d={'data':data}
    return render(request,'hospital/hospital_view_appoinment.html',d)

def hospital_update_status(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('hospital_profile')
    data=Hospital_Appointment.objects.get(id=pid)
    form=Hospital_AppointmentForm(request.POST or None,instance=data)
    if request.method=="POST":
        u=request.POST['a_date']
        v=request.POST['a_timing']
        data.a_date=u
        data.a_timing=v
        data.status="confirmed"
        data.save()
        messages.success(request,"Payment Completed Successfully")
        return redirect("hospital_view_appointment")
    d={'form':form,'data':data}
    return render(request,'hospital/hospital_update_status.html',d)

def hospital_view_confirmed_appintment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('hospital_profile')
    data=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),status="confirmed",)
    d={'data':data}
    return render(request,'hospital/hospital_view_confirmed_appoinment.html',d)

def hospital_view_history_appintment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('hospital_profile')
    tod=datetime.date.today()
    data=Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),a_date__lte=tod,)
    d={'data':data}
    return render(request,'hospital/hospital_view_history_appoinment.html',d)

def hospital_search_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('hospital_profile')
    data=""
    u = ""
    v = ""
    if request.method=="POST":
        try:
            u=request.POST['from_date']
            v=request.POST['to_date']
            i1 = datetime.datetime.fromisoformat(u)
            i2 = datetime.datetime.fromisoformat(v)
            data = Hospital_Appointment.objects.filter(hospital=Hospital.objects.get(user=request.user),a_date_gte=datetime.date(i1.year,i1.month,i1.day),a_date_lte=datetime.date(i2.year,i2.month,i2.day))
        except:
            pass
    d={'data':data,'u':u,'v':v}
    return render(request,'hospital/hospital_search_appoinment.html',d)

def patient_search_by_id(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('hospital_profile')
    data=""
    i=""
    appointment=""
    hos_appointment=""
    if request.method=="POST":
        i=request.POST['uid']
        try:
            data=Patient.objects.get(health_uid=i)
            appointment = Appointment.objects.filter(patient=data)
            hos_appointment = Hospital_Appointment.objects.filter(patient=data)
        except:
            messages.success(request,'Invalid Card Number')
    d={'data':data,'i':i,'appointment':appointment,'hos_appointment':hos_appointment}
    return render(request,'hospital/patient_search_by_id.html',d)



# Medical

def Medical_Profile(request):
    user = User.objects.get(id=request.user.id)
    pat = Medical.objects.get(user=user)
    form = MedicalForm(request.POST or None,instance=pat)
    if request.method == "POST":
        form = MedicalForm(request.POST or None,request.FILES or None, instance=pat)
        if form.is_valid():
            form.save()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            messages.success(request,'Profile Updated Successfully')
            return redirect("medical_profile")
    d = {'doc':pat,'form':form}
    return render(request,'Medical/profile.html',d)

def Medical_Change_Password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        d = request.POST['pwd3']
        if c == d:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(d)
            u.save()
            messages.success(request,'Password Changed Successfully')
            return redirect("medical_change_password")
    return render(request,'medical/change_password.html')

def medical_patient_search_by_id(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    data=""
    i=""
    appointment=""
    hos_appointment=""
    if request.method=="POST":
        i=request.POST['uid']
        try:
            data=Patient.objects.get(health_uid=i)
            appointment = Appointment.objects.filter(patient=data)
            hos_appointment = Hospital_Appointment.objects.filter(patient=data)
        except:
            messages.success(request,'Invalid Card Number')
    d={'data':data,'i':i,'appointment':appointment,'hos_appointment':hos_appointment}
    return render(request,'medical/patient_search_by_id.html',d)

def admin_view_hospitals(request):
    data=Hospital.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_hospital.html',d)

def admin_view_medicals(request):
    data=Medical.objects.all()
    d={'data':data}
    return render(request,'admin/admin_view_medical.html',d)


def medical_invoices(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    pat = Appointment.objects.get(id=pid)
    med = Prescription.objects.filter(appoint=pat)
    total = str(med.aggregate(Sum('price')))[14:][:-1]
    d = {'pat':pat,'med':med,'total':total}
    return render(request,'medical/invoices.html',d)

def hospital_invoices2(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    pat = Hospital_Appointment.objects.get(id=pid)
    d = {'pat':pat}
    return render(request,'hospital/hospital_invoice2.html',d)

def add_price_hospital(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    pat = Hospital_Appointment.objects.get(id=pid)
    if request.method == "POST":
        p = request.POST['price']
        pat.price = p
        pat.save()
        messages.success(request,'Add Price Successfully')
        return redirect('hospital_view_invoices')
    d = {'pat':pat}
    return render(request,'hospital/add_price_hospital.html',d)

def doctor_invoices(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    pat = Appointment.objects.get(id=pid)
    med = Doctors_Invoice.objects.filter(appointment=pat)
    total = str(med.aggregate(Sum('price')).values)
    d = {'pat':pat,'med':med,'total':total}
    return render(request,'doctor/invoices.html',d)

def medical_add_medicine(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('medical_profile')
    data  = Appointment.objects.get(id=pid)
    med = Prescription.objects.filter(appoint=data)
    count = med.count()
    if request.method == "POST":
        for i in med:
            p = request.POST["price"+str(i.id)]
            i = request.POST["id"+str(i.id)]
            doc = Prescription.objects.get(id=i)
            doc.price = p
            doc.save()
        data.medical = Medical.objects.get(user=request.user)
        data.save()
        messages.success(request,'Price Updated Successfully')
        return redirect('medical_invoices',data.id)
    d = {'med':med,'data':data}
    return render(request,'medical/add_medicine.html',d)

def d_search_appointment(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=""
    u = ""
    v = ""
    if request.method=="POST":
        u=request.POST['from_date']
        v=request.POST['to_date']
        i1 = datetime.datetime.fromisoformat(u)
        i2 = datetime.datetime.fromisoformat(v)
        data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),a_date__gte=datetime.date(i1.year,i1.month,i1.day),a_date__lte=datetime.date(i2.year,i2.month,i2.day))
    d={'data':data,'u':u,'v':v}
    return render(request,'doctor/d_search_appoinment.html',d)

def confirmed_h_appointment(request):
    tod=datetime.date.today()
    data=Hospital_Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="confirmed",a_date__gte=tod)
    d={'data':data}
    return render(request,'patient/confirmed_h_appoinment.html',d)

def h_appointment(request):
    data=Hospital_Appointment.objects.filter(patient=Patient.objects.get(user=request.user),status="pending")
    d={'data':data}
    return render(request,'patient/h_appoinment.html',d)

def history_h_appointment(request):
    tod=datetime.date.today()
    data=Hospital_Appointment.objects.filter(patient=Patient.objects.get(user=request.user),a_date__lte=tod)
    d={'data':data}
    return render(request,'patient/history_h_appoinment.html',d)

def doctor_status(request,pid):
    pat = Doctor.objects.get(id=pid)
    if pat.status=="pending":
        pat.status = "accept"
        pat.save()
        messages.success(request,'Selected Doctor granted to Permission')
    else:
        pat.status = "pending"
        pat.save()
        messages.success(request, 'Selected Doctor Withdraw to Permission')
    return redirect('admin_view_doctors')


def hospital_status(request,pid):
    pat = Hospital.objects.get(id=pid)
    pat.status = "accept"
    pat.save()
    messages.success(request,'Selected Hospital granted to Permission')
    return redirect('admin_view_hospitals')

def medical_status(request,pid):
    pat = Medical.objects.get(id=pid)
    pat.status = "accept"
    pat.save()
    messages.success(request,'Selected Medical granted to Permission')
    return redirect('admin_view_medicals')

def doctor_patient_search_by_id(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=""
    i=""
    appointment=""
    hos_appointment=""
    if request.method=="POST":
        i=request.POST['uid']
        try:
            data=Patient.objects.get(health_uid=i)
            appointment = Appointment.objects.filter(patient=data)
            hos_appointment = Hospital_Appointment.objects.filter(patient=data)
        except:
            messages.success(request,'Invalid Card Number')
    d={'data':data,'i':i,'appointment':appointment,'hos_appointment':hos_appointment}
    return render(request,'doctor/doctor_patient_search_by_id.html',d)

def admin_patient_search_by_id(request):
    data=""
    i=""
    appointment=""
    hos_appointment=""
    if request.method=="POST":
        i=request.POST['uid']
        try:
            data=Patient.objects.get(health_uid=i)
            appointment = Appointment.objects.filter(patient=data)
            hos_appointment = Hospital_Appointment.objects.filter(patient=data)
        except:
            messages.success(request,'Invalid Card Number')
    d={'data':data,'i':i,'appointment':appointment,'hos_appointment':hos_appointment}
    return render(request,'admin/admin_patient_search_by_id.html',d)

def admin_profile(request):
    return render(request,'admin/profile.html')

def edit_admin_profile(request):
    data = Adminstration.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            f = request.POST['fname']
            l = request.POST['lname']
            m = request.POST['mobile']
            a = request.POST['address']
            e = request.POST['email']
            try:
                i = request.FILES['images']
                data.image = i
                data.save()
            except:
                pass
            data.user.first_name = f
            data.user.last_name = l
            data.user.email = e
            data.address = a
            data.mobile = m
            data.image = i
            data.user.save()
            data.save()
            messages.success(request,'Profile Updated Successfully')
        except:
            pass
        try:
            n = request.POST['pwd1']
            c = request.POST['pwd2']
            d = request.POST['pwd3']
            if c == d:
                u = User.objects.get(username__exact=request.user.username)
                u.set_password(d)
                u.save()
                messages.success(request, 'Password Changed Successfully')
        except:
            pass
    return redirect('admin_profile')

def my_patient(request):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Appointment.objects.filter(doctor=Doctor.objects.get(user=request.user),status="confirmed")
    d = {'data':data}
    return render(request,'doctor/my_patient.html',d)

def doc_patient_dashboard(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Patient.objects.get(id=pid)
    data2 = Doctor.objects.get(user=request.user)
    pat = Appointment.objects.filter(patient = data)
    pat2 = Appointment.objects.filter(patient = data,doctor=data2,a_date = datetime.date.today()).first()
    if not pat2:
        pat2 = 0
    else:
        pat2 = pat2.id
    d = {'data': pat,'pat':data,'pat2':pat2}
    return render(request,'doctor/doc_patient_dashboard.html',d)


def add_presc(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data  = Appointment.objects.get(id=pid)
    if request.method == "POST":
        m = request.POST['name']
        p = request.POST['presc']
        d = request.POST['days']
        t = request.POST.getlist('time[]')
        Prescription.objects.create(appoint=data,name=m,quantity=p,days=d,time=t)
        messages.success(request,'One Prescription added')
        return redirect('add_prescription',data.id)

def add_prescription(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data=""
    try:
        data  = Appointment.objects.get(id=pid)
    except:
        pass
    if request.method == "POST":
        messages.success(request,'One Medicine added')
        return redirect('doc_patient_dashboard',data.patient.id)
    d = {'data':data}
    return render(request,'doctor/add-prescription.html',d)

def add_medical(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = ""
    try:
        data = Appointment.objects.get(id=pid)
    except:
        pass
    if request.method == "POST":
        m = request.POST['desc']
        d = request.POST['date']
        p = request.FILES['file']
        Medical_Record.objects.create(appoint=data,disc=m,file=p,date=d)
        messages.success(request,'Medical Record Added Successfully')
        return redirect('doc_patient_dashboard',data.patient.id)

def add_bil(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Appointment.objects.get(id=pid)
    if request.method == "POST":
        m = request.POST['title']
        p = request.POST['amount']
        Billing_Record.objects.create(appoint=data,title=m,amount=p)
        messages.success(request,'One Medicine added')
        return redirect('add_bill',data.id)

def add_bill(request,pid):
    if not access(request.user):
        messages.success(request,'Update Your Profile and Wait for Verification')
        return redirect('doctor_profile')
    data = Appointment.objects.get(id=pid)
    if request.method == "POST":
        messages.success(request,'One Billing Record added Successfully')
        return redirect('doc_patient_dashboard',data.patient.id)
    d = {'data':data}
    return render(request,'doctor/add-billing.html',d)

def delete_bill(request,pid):
    data = Billing_Record.objects.get(id=pid)
    data.delete()
    messages.success(request,'Biiling Record deleted successfully')
    return redirect('add_bill',data.appoint.id)

def delete_presc(request,pid):
    data = Prescription.objects.get(id=pid)
    data.delete()
    messages.success(request,'Prescription deleted successfully')
    return redirect('add_prescription',data.appoint.id)

def delete_patient(request,pid):
    data = Patient.objects.get(id=pid)
    data.delete()
    messages.success(request,'Patient deleted successfully')
    return redirect('admin_view_patients')

