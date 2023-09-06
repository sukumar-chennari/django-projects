from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator

# Create your views here.


from .models import *
from django.db.models import Q,Sum

def get_student(request):
    queryset=Student.objects.all()

    if request.GET.get('search'):
        Search=request.GET.get('search')
        queryset=queryset.filter(
            Q(student_name__icontains=Search)|
            Q(department__department__icontains=Search)|
            Q(student_id__student_id__icontains=Search)
        )
    paginator = Paginator(queryset, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    return render(request,'reports/students.html',context={'students':page_obj})

from .seed import *
def see_marks(request,student_id):
    #generate_report_card()
    queryset=SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    students=Student.objects.filter(student_id__student_id=student_id)
    total_marks=queryset.aggregate(total_marks=Sum('marks'))
    return render(request,'reports/see_marks.html',context={'queryset':queryset,'students':students,'total_marks':total_marks})
