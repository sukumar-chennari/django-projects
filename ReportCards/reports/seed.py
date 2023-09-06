from faker import Faker
import random
fake = Faker()

from .models import *
from django.db.models import Sum

def seed_db(n=10):
    try:
# sourcery skip: remove-zero-from-range
        for _ in range(0,n):
            student_name=fake.name()
            student_address=fake.address()
            student_email=fake.email()
            student_age=random.randint(20,30)

            department_obj=Department.objects.all()
            random_index=random.randint(0,len(department_obj)-1)
            department=department_obj[random_index]

            student_id=f'STU-0{random.randint(100,999)}'

            student_id_obj=StudentID.objects.create(student_id = student_id)
            student_obj=Student.objects.create(
                        student_name=student_name,
                        student_address=student_address,
                        student_email=student_email,
                        student_age=student_age,
                        department=department,
                        student_id=student_id_obj
                        )
    except Exception as e:
        print(e)

def create_subject_marks():
    try:
        student_obj=Student.objects.all()
        for student in student_obj:
            subjects=Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0,100)
                )
    except Exception as e:
        print(e)

def generate_report_card():
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','-student_age')
    current_rank=-1
    i=1
    
    for rank in ranks:
        ReportCard.objects.create(
            student=rank,
            student_rank=i
        )
        i = i + 1