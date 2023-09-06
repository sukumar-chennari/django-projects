from django.db import models

# Create your models here.
class StudentID(models.Model):
    student_id=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id

class Department(models.Model):
    department=models.CharField(max_length=100)

    class Meta:
        ordering=['department']
    def __str__(self) -> str:
        return self.department

class Student(models.Model):
    student_name=models.CharField(max_length=100)
    student_email=models.EmailField(unique=True)
    student_age=models.IntegerField(default=18)
    student_address=models.CharField(max_length=100)

    student_id=models.OneToOneField(StudentID,related_name='studentid',on_delete=models.CASCADE)
    department=models.ForeignKey(Department,related_name='depart',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.student_name
    
    class Meta:
        ordering=['student_name']
        verbose_name='student'

class Subject(models.Model):
    subject_name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject_name
    
class SubjectMarks(models.Model):
    student=models.ForeignKey(Student,related_name='studentmarks',on_delete=models.CASCADE,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks=models.IntegerField()

    class Meta:
        unique_together=['student','subject']

    def __str__(self) -> str:
        return self.marks

class ReportCard(models.Model):
    student=models.ForeignKey(Student,related_name='studentreportmarks',on_delete=models.CASCADE,null=True)
    date_of_report_card=models.DateField(auto_now_add=True)
    student_rank=models.IntegerField()

    class Meta:
        ordering=['student_rank','date_of_report_card']
    

