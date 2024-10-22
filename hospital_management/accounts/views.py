from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import patient_data
from django.shortcuts import get_object_or_404

def home(request):
    if request.user.is_authenticated:
        patient_Details = patient_data.objects.all()
        return render(request, 'home.html', { 'username': request.user.username, 'patient_Details':patient_Details})
    return render(request, 'home.html')

def delete_patient_data(request, patient_id):
    if request.user.is_authenticated:
        patient = get_object_or_404(patient_data, id=patient_id)
        patient.delete()
        messages.info(request, "Patient data deleted successfully.")
    return redirect('home')


def add_patient_data(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            age = request.POST['age']
            gender = request.POST['gender']
            medical_issue = request.POST['medical_issue']
            doctor_name = request.POST['doctor_name']
            mbl = request.POST['mbl']
            appointment_date = request.POST['appointment_date']
            appt_time = request.POST['appt_time']
            new_entry = patient_data(name=name, age=age, gender=gender, medical_issue=medical_issue, doctor_name=doctor_name,mbl=mbl,appointment_date=appointment_date,appt_time=appt_time)
            new_entry.save()
            messages.info(request,"Appointment Scheduled")
        return redirect('home') 
    return redirect('home')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pword = request.POST['password']
        try:
            # Fetch the user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

        # Authenticate using the fetched username
        user = auth.authenticate(username=user.username, password=pword)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request,"login.html")
def register(requests):
    if requests.method == 'POST':
        fstname = requests.POST['first_name']
        lstname = requests.POST['last_name']
        usrnm = requests.POST['username']
        email = requests.POST['email']
        pass1 = requests.POST['password1']
        pass2 = requests.POST['password2']
        if pass1==pass2:
            if User.objects.filter(username=usrnm).exists():
                # print('username taken')
                messages.info(requests,"username taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                # print("email taken")
                messages.info(requests,"email taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username=usrnm, first_name = fstname, last_name = lstname,email=email, password=pass1)
                user.save()
                print('user created')
                return redirect('login')
        else:
            print('password mismatch')
        return redirect('/')
    else:   
        return render(requests,'register.html')
    
def logout(requests):
    auth.logout(requests)
    return redirect("/")