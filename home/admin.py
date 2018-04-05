from django.contrib import admin
from .models import Employee, Mentor, Student, ClassName, Attendance




class EmployeeList(admin.ModelAdmin):
    list_display = ('Employee_name', 'Employee_phone', 'Employee_Address', 'Employee_Id')
    search_fields = ('Employee_name', 'Employee_phone','Employee_Id')


class MentorList(admin.ModelAdmin):
    list_display = ('Mentor_name', 'Mentor_phone', 'Mentor_Id','Mentor_Address','Mentor_Gender','begining_date','ending_date','Mentor_email')
    search_fields = ('Mentor_name', 'Mentor_phone','Mentor_Id','begining_date','ending_date','Mentor_email')

class StudentList(admin.ModelAdmin):
    list_display = ('Student_id', 'Student_name', 'Student_Class', 'Student_curr_grade', 'Student_prev_grade', 'Parents_email',
    'Parents_phone', 'School', 'Men_name', 'Emp_name','Comments', 'start_date', 'last_date')
    search_fields = ('Student_name', 'Student_id', 'School', 'Parents_phone', 'start_date', 'last_date', 'Student_Class')

class ClassNameList(admin.ModelAdmin):
    list_display = ('class_name', 'class_date','Mentor')
    search_fields =  ('class_name', 'class_date','Mentor',)

class  AttendanceList(admin.ModelAdmin):
    list_display = ('stu_name','attend','attend_date','remarks',)


admin.site.register(Employee,EmployeeList )
admin.site.register(Mentor,MentorList)
admin.site.register(Student, StudentList)
admin.site.register(ClassName, ClassNameList)
admin.site.register(Attendance, AttendanceList)