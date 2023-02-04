from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'group'
    students = Student.objects.prefetch_related('teachers').order_by(ordering)
    context = { 'students': students}
    return render(request, template, context)

def teachers_list(request):
    template = 'school/teachers_list.html'
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    ordering = 'name'
    teachers = Teacher.objects.prefetch_related('students').order_by(ordering)
    context = { 'teachers': teachers}
    return render(request, template, context)