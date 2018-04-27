from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from django.utils import timezone
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q
from .models import Student,Mentor,Employee,SendSMS
from .forms import StudentForm,UserForm,EmployeeForm,ClassNameForm
# twillio imports start
from django.urls import reverse_lazy
from django.conf import settings
from decimal import Decimal
from datetime import datetime
from django.views.generic import CreateView
from home.utils import send_twilio_message
import geocoder
import logging

from googlevoice import Voice
#from googlevoice.util import input
import sys
#from sendsms import api
import fileinput
#from sendsms import message
def searchemp(request):
    name_query = request.GET.get("name")
    curr_grade_query = request.GET.get("currgrade")
    prev_grade_query = request.GET.get("prevgrade")

    students = None
    #if (len(name_query) > 0) or (len(curr_grade_query) > 0) or (len(prev_grade_query) > 0):
    #    students = Student.objects.filter(
    #        Q(Student_name__icontains=name_query, Student_curr_grade__icontains=curr_grade_query,Student_prev_grade__icontains=prev_grade_query)).distinct()
    if len(name_query) > 0:
        students = Student.objects.filter(Q(Student_name__icontains=name_query)).distinct()
    #elif len(curr_grade_query) > 0:
    #    students = Student.objects.filter(Q(Student_curr_grade__icontains=curr_grade_query)).distinct()
    #elif len(prev_grade_query) > 0:
    #    students = Student.objects.filter(Q(Student_prev_grade__icontains=prev_grade_query)).distinct()
    else:
        pass
    return render(request, 'home/emphome.html', {'students': students})


def searchment(request):
    name_query = request.GET.get("name")
    curr_grade_query = request.GET.get("currgrade")
    prev_grade_query = request.GET.get("prevgrade")

    students = None
    #if (len(name_query) > 0) or (len(curr_grade_query) > 0) or (len(prev_grade_query) > 0):
    #    students = Student.objects.filter(
    #        Q(Student_name__icontains=name_query, Student_curr_grade__icontains=curr_grade_query,
    #          Student_prev_grade__icontains=prev_grade_query)).distinct()
    if len(name_query) > 0:
        students = Student.objects.filter(Q(Student_name__icontains=name_query)).distinct()
    #elif len(curr_grade_query) > 0:
    #    students = Student.objects.filter(Q(Student_curr_grade__icontains=curr_grade_query)).distinct()
    #elif len(prev_grade_query) > 0:
    #    students = Student.objects.filter(Q(Student_prev_grade__icontains=prev_grade_query)).distinct()
    else:
        pass
    return render(request, 'home/mentorhome.html', {'students': students})


def home(request):
    return render(request, 'home/base.html',
                  {'home': home})

def about(request):
    return render(request, 'home/about.html',
                  {'about': about})


def mentor(request):
    return render(request, 'home/mentor.html',
                  {'mentor': mentor})

def index(request):
    return render(request, 'home/index.html',
                  {'index': index})

def empindex(request):
    return render(request, 'home/empindex.html',
                  {'empindex': empindex})

def emphome(request):
    students = Student.objects.filter(Emp_name__Employee_name=request.user.username).order_by('Student_name')
    return render(request, 'home/emphome.html',
                  {'students': students})

def mentorhome(request):
    students = Student.objects.filter(Men_name__Mentor_name=request.user.username).order_by('Student_name')
    return render(request, 'home/mentorhome.html',
                  {'students':students})


#def studentsreports(request):
#    return render(request, 'home/studentsreports.html',
#                  {'studentsreports': studentsreports})

def createappointments(request):
    return render(request, 'home/createappointments.html',
                  {'createappointments': createappointments})

def mentortask(request):
    return render(request, 'home/mentortask.html',
                  {'mentortask': mentortask})

def empmarkattendance(request):
    return render(request, 'home/empmarkattendance.html',
                  {'empmarkattendance': empmarkattendance})

#def empstudentsreports(request):
#    return render(request, 'home/empstudentsreports.html',
#                  {'empstudentsreports': empstudentsreports})

def empcreateappointments(request):
    return render(request, 'home/empcreateappointments.html',
                  {'empcreateappointments': empcreateappointments})

def emptask(request):
    return render(request, 'home/emptask.html',
                  {'emptask': emptask})

def mentstudlist(request):
    #users = request.user.username()
    students = Student.objects.filter(start_date__lte=timezone.now()).order_by('Student_name')
    return render(request, 'home/mentstudlist.html',
                  {'students': students})



def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'home/base.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return emphome(request)
            else:
                login(request, user)
                return mentorhome(request)
        else:
            return render(request, 'home/login.html', {'error_message': 'Invalid login'})
    return render(request, 'home/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home/login.html')
    context = {
        "form": form,
    }
    return render(request, 'home/register.html', context)

def password_reset(request):
    return render(request, 'home/password_reset.html',
    {'home': password_reset})


def password_reset_confirm(request):
    return render(request, 'home/password_reset_confirm.html',
    {'home': password_reset_confirm})

def password_reset_email(request):
    return render(request, 'home/password_reset_email.html',
    {'home': password_reset_email})

def password_reset_complete(request):
    return render(request, 'home/password_reset_complete.html',
    {'home': password_reset_complete})

def Student_list(request):
    students = Student.objects.filter(start_date__lte=timezone.now()).order_by('Student_name')
    return render(request, 'home/studentlist.html',
    {'students': students})

def Student_Report(request):
    students = Student.objects.filter(start_date__lte=timezone.now()).order_by('Student_name')
    return render(request, 'home/studentsreports.html',
    {'students': students})

def Emp_Student_Report(request):
    students = Student.objects.filter(start_date__lte=timezone.now()).order_by('Student_name')
    return render(request, 'home/empstudentsreports.html',
    {'students': students})

def Student_Report_Edit(request,pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            student.updated_date = timezone.now()
            student.save()
            students = Student.objects.filter(start_date__lte=timezone.now()).order_by('Student_name')
            return render(request, 'home/studentsreports.html',
            {'students': students})
    else:
        form = StudentForm(instance=student)
        return render(request, 'home/studreportedit.html', {'form': form})


def Emp_Student_Report_Edit(request,pk):
    student = get_object_or_404(Student,pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            student.updated_date = timezone.now()
            student.save()
            students = Student.objects.filter(start_date__lte=timezone.now()).order_by('Student_name')
            return render(request, 'home/empstudentsreports.html',
            {'students': students})
    else:
        form = StudentForm(instance=student)
        return render(request, 'home/empstudreportedit.html', {'form': form})


def studentedit(request,pk):
   student = get_object_or_404(Student,pk=pk)
   if request.method == "POST":
       form = StudentForm(request.POST, instance=student)
       if form.is_valid():
           student = form.save()
           student.updated_date = timezone.now()
           student.save()
           students = Student.objects.filter(start_date__lte=timezone.now())
           return render(request, 'home/studentlist.html', {'students': students})
   else:
       # print("else")
       form = StudentForm(instance=student)
   return render(request, 'home/studentedit.html', {'form': form})

def studentadd(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.start_date = timezone.now()
            student.save()
            students = Student.objects.filter(start_date__lte=timezone.now())
            return render(request, 'home/studentlist.html',
                          {'students': students})
    else:
        form = StudentForm()
        # print("Else")
    return render(request, 'home/studentadd.html', {'form': form})

def mentor_list(request):
    mentors = Mentor.objects.filter(begining_date__lte=timezone.now()).order_by('Mentor_name')
    return render(request, 'home/mentorlist.html',
                 {'mentors': mentors})


def mentor_edit(request, pk):
   mentor = get_object_or_404(Mentor, pk=pk)
   if request.method == "POST":
       form = MentorForm(request.POST, instance=mentor)
       if form.is_valid():
           mentor = form.save()
           mentor.updated_date = timezone.now()
           mentor.save()
           mentors = Mentor.objects.filter(begining_date__lte=timezone.now())
           return render(request, 'home/mentorlist.html', {'mentors': mentors})
   else:
       form = MentorForm(instance=mentor)
   return render(request, 'home/mentoredit.html', {'form': form})

def mentor_new(request):
    if request.method == "POST":
        form = MentorForm(request.POST)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.start_date = timezone.now()
            mentor.save()
            mentors = Mentor.objects.filter(begining_date__lte=timezone.now())
            return render(request, 'home/mentorlist.html',
                          {'mentors': mentors})
    else:
        form = MentorForm()
        # print("Else")
    return render(request, 'home/mentornew.html', {'form': form})

def mrkatt_new(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            mrkatt = form.save(commit=False)
            mrkatt.start_date = timezone.now()
            mrkatt.save()
            students = Student.objects.all()
            return render(request, 'home/markattendance.html',
                          {'students': students})
    else:
        form = AttendanceForm()
        # print("Else")
    return render(request, 'home/markattendanceedit.html', {'form': form})


def markattendance(request):
    students = Student.objects.all().order_by('Student_name')
    return render(request, 'home/markattendance.html',
                  {'students': students})

def studentsarchive(request):
    student = get_object_or_404(Student)
    if request.method =="POST":
       form = StudentForm(request.POST, instance = student)
       print("one")
       if form.is_valid():
           print("2")
           student= form.save()
           print("3")
           Stud_id = form.cleaned_data['Student ID']
           print("4")
           student_arch= Student.object.filter(Student_id = Stud_id).order_by('Student_name')
           print("5")
           student_arch.delete()
           students = StudentForm(instance=student)
           return render(request, 'home/studentlist.html', {'students': students})

    else:
           print("else")
     #  form = StudentForm(instance=student)
      # return render(request, 'home/studentsarchive.html', {'form': form})


def map(request):
    students=Student.objects.all()
    mapvalue=False
    if request.method=='POST':
        mapvalue=True
        print(request.POST)
        schoolID=request.POST.get('element.school')
        print(schoolID)
        g = geocoder.ip('me')
        # print(str(g.latlng).strip("[]"))
        lats=str(g.latlng).strip("[]").replace(" ","")
        src="https://www.google.com/maps/embed/v1/directions?origin="+lats+"&destination=place_id:"+schoolID+"&key=AIzaSyBcCqgDCGOBUkwpaj7Pdc0osAS9wUQKyXs"
        return render(request,'home/map.html',{'students':students,'mapvalue':mapvalue,"schoolID":schoolID,"src":src})
    return render(request, 'home/map.html', {'students': students,'mapvalue':mapvalue})

def archive(request):
    students = Student.objects.filter(start_date__lte=timezone.now())
    return render(request, 'home/archive.html',
                  {'students': students})


def location(request):
    return render(request, 'home/marker.html',
    {'home': location})


def give(request):
    return render(request, 'home/give.html',
    {'home':give})

def thankyou(request) :
        return render(request, 'home/thankyou.html',
                      {'home': thankyou} )

def sendSMS(request):
    success=False
    studentList=Student.objects.all()
    if request.method=='POST':
        success=True
        number = request.POST.get('to_number')
        print('njjj')
        api.send_sms(body='I can haz txt', from_phone='+14024520413', to=['+14029153381'])
        from sendsms.message import SmsMessage
        message = SmsMessage(body='lolcats make me hungry', from_phone='+14024520413', to=['+41791234567'])
        message.send()
        body = request.POST.get('body')
        api.send_sms(body='I can haz txt', from_phone='+14024520413', to=['+14029153381'])
        # call twilio
        #

        #
        # voice = Voice()
        # voice.login(user, password)
        # number='4029153381'
        # message='test1234'
        # print (number)
        # number = input('Number to send message to: ') # use these for command method
        # message = input('Message text: ')

        # voice.send_sms(number, message)
        sent = send_twilio_message(number, body)
        # form = SendSMS()
        # save form
        # send_sms = form.save()
        # send_sms.from_number = settings.TWILIO_PHONE_NUMBER
        # send_sms.sms_sid = sent.sid
        # send_sms.account_sid = sent.account_sid
        # send_sms.status = sent.status
        # send_sms.sent_at = datetime.now()
        # if sent.price:
        #     send_sms.price = Decimal(force_text(sent.price))
        #     send_sms.price_unit = sent.price_unit
        # send_sms.save()
        return render (request,'home/sendsms_form.html',{'success':success,'studentList':studentList})
    return render(request,'home/sendsms_form.html',{'success':success,'studentList':studentList})

class SendSmsCreateView(CreateView):
    model = SendSMS
    form_class = SendSMSForm
    template_name = 'home/sendsms_form.html'
    success_url = reverse_lazy('send_sms')
    print('test')
    # studentList = Student.objects.all()
    def form_valid(self, form):
        number = form.cleaned_data['to_number']
        logging.debug("Oh hai!")
        body = form.cleaned_data['body']
        # call twilio
        sent = send_twilio_message(number, body)
        form=SendSMS()
        # save form
        send_sms = form.save(commit=False)
        send_sms.from_number = settings.TWILIO_PHONE_NUMBER
        send_sms.sms_sid = sent.sid
        send_sms.account_sid = sent.account_sid
        send_sms.status = sent.status
        send_sms.sent_at = datetime.now()
        if sent.price:
            send_sms.price = Decimal(force_text(sent.price))
            send_sms.price_unit = sent.price_unit
        send_sms.save()
        print (form)
        # return super(SendSmsCreateView, self).form_valid(form)
        # return render(request, 'home/thankyou.html',
        #               {'home': thankyou})

    def get_context_data(self, **kwargs):
        context = super(SendSmsCreateView, self).get_context_data(**kwargs)
        # here's the difference:
        context['studentList'] = Student.objects.all()
        return context

