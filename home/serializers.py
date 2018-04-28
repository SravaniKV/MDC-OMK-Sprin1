from rest_framework import serializers
from .models import Student


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
            model = Student
            fields = ('Student_id', 'Student_name', 'Student_Class', 'Student_curr_grade', 'Student_prev_grade', 'Parents_email',
    'Parents_phone', 'School','School_ID', 'Men_name', 'Emp_name','Comments', 'start_date', 'last_date')