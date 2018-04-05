from django import forms
from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.utils import timezone
#form django import forms
# Create your models here.

regex=r'[0-9]'


class Employee(models.Model):
    Employee_Id = models.CharField(max_length=10,unique=True)
    Employee_name = models.CharField(max_length=50)
    Employee_phone = models.CharField(max_length=10, validators=[MinLengthValidator(10), RegexValidator(regex)],
                                      help_text="Phone Number should be 10 digits")
    Employee_email = models.EmailField(max_length=200)
    Employee_Address= models.CharField(max_length=200)


    def __str__(self):
      return str(self.Employee_name)


class Mentor(models.Model):
    Mentor_Id = models.CharField(max_length=10,unique=True)
    Mentor_name = models.CharField(max_length=49,null=True)
    Mentor_phone = models.CharField(max_length=10, validators=[MinLengthValidator(10), RegexValidator(regex)],
                                    help_text="Phone Number should be 10 digits")
    Mentor_email = models.EmailField(max_length=49, null=True)
    Mentor_Address=models.CharField(max_length=200)
    Mentor_Gender=models.CharField(max_length=10, null = True ,help_text="Enter F or M")
    begining_date = models.DateField(default=timezone.now)
    ending_date = models.DateField(blank=True, null=True)

    def created(self):
        self.begining_date = timezone.now()
        self.save()

    def enddate(self):
        self.ending_date = timezone.now()
        self.save()

    def __str__(self):
       return str(self.Mentor_name)

class Student(models.Model):
     Student_id= models.CharField(max_length=15,unique=True)
     Student_name=models.CharField(max_length=49,null=True)
     Student_curr_grade = models.CharField(max_length=10, null=True)
     Student_prev_grade = models.CharField(max_length=10, null=True)
     Student_Class = models.CharField(max_length=10)
     Parents_email = models.EmailField(max_length=200, null=True)
     Parents_phone = models.CharField(validators=[MinLengthValidator(10), RegexValidator(regex)], max_length=10)
     School= models.CharField(max_length=49)
     Men_name =models.ForeignKey(Mentor,related_name='Menemail')
     Emp_name= models.ForeignKey(Employee, related_name='Empemail')
     Comments=models.CharField(max_length=200, null=True)
     start_date = models.DateTimeField(default=timezone.now)
     last_date = models.DateField(blank=True, null=True)


     def create(self):
         self.start_date = timezone.now()
         self.save()

     def lastdate(self):
         self.last_date = timezone.now()
         self.save()

     def __str__(self):
      return str(self.Men_name)

     def __str__(self):
       return str(self.Emp_name)

     def __str__(self):
       return str(self.Student_name)

class Appointment(models.Model):
    Sname = models.ForeignKey(Student, related_name='Appointment')
    Mname = models.ForeignKey(Mentor, related_name='Appointment')
    Sid = models.ForeignKey(Student, related_name='Appointment2')


    def __str__(self):
        return str(self.sname)


class ClassName(models.Model):
    class_name = models.CharField(max_length=20)
    class_date=models.DateField(blank=True, null=True)
    Mentor= models.ForeignKey(Mentor, related_name='class_mentor')
    #student = models.CharField(max_length=20, null=True)
    student= models.ManyToManyField(Student, related_name='class_student')
    attendance = models.BooleanField(default=True)
    #attendance =models.ChoiceField(widget=forms.RadioSelect)

    def __str__(self):
        return str(self.class_name)

class Attendance(models.Model):
    stu_name = models.ForeignKey(Student,related_name='studentname')
    attend = models.BooleanField(default=False)
    attend_date = models.DateTimeField(default=timezone.now)
    remarks= models.CharField(max_length=250,default='attendance remarks')

    def __str__(self):
        return str(self.stu_name)

    def create(self):
        self.attend_date = timezone.now()
        self.save()



# twilio

class SendSMS(models.Model):
    to_number = models.CharField(max_length=30)
    from_number = models.CharField(max_length=30)
    sms_sid = models.CharField(max_length=34, default="", blank=True)
    account_sid = models.CharField(max_length=34, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default="", blank=True)
    body= models.CharField(max_length=200, default="", blank = True)