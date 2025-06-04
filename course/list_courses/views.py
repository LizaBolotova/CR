from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.db import models
from django.db.models import Avg, Min, Max, Sum

from .models import Course
from .forms import CourseForm


#Все курсы
def all_courses(request):
    show = Course.objects.all()
    search_input = request.GET.get('search', '').strip()
    m = ''
    if search_input:
        m = Course.objects.filter(
            models.Q(name__iregex=search_input) |
            models.Q(category__iregex=search_input))
        #m = Course.objects.filter(name__icontains=search_input) | Course.objects.filter(category__icontains=search_input)
    context = {'show': show, 'm': m}
    return render(request, 'show_all.html', context)

#Один курс инфо
def one_course(request,course_id:int):
    cours = Course.objects.get(id=course_id)
    context = {'cours': cours}
    return render(request, 'show_one.html', context)

# Форма
def form(request):
    if request.method == 'POST':
        forma = CourseForm(request.POST, request.FILES)
        if forma.is_valid():
            forma.save()
    else:
        forma = CourseForm()
    return render(request, 'form.html', context={'form': forma})

# Табличка
def statistics(request):
    courses = Course.objects.all()
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'name')

    stats = {
        # Для длительности
        'avg_length': courses.aggregate(Avg('length'))['length__avg'],
        'min_length': courses.aggregate(Min('length'))['length__min'],
        'max_length': courses.aggregate(Max('length'))['length__max'],

        # Для стоимости
        'avg_cost': courses.aggregate(Avg('cost'))['cost__avg'],
        'min_cost': courses.aggregate(Min('cost'))['cost__min'],
        'max_cost': courses.aggregate(Max('cost'))['cost__max'],
        'total_cost': courses.aggregate(Sum('cost'))['cost__sum'],

        # Для студентов
        'avg_students': courses.aggregate(Avg('stud_amount'))['stud_amount__avg'],
        'min_students': courses.aggregate(Min('stud_amount'))['stud_amount__min'],
        'max_students': courses.aggregate(Max('stud_amount'))['stud_amount__max'],
        'total_students': courses.aggregate(Sum('stud_amount'))['stud_amount__sum'],

        # Для оценок
        'avg_grade_global': courses.aggregate(Avg('avg_grade'))['avg_grade__avg'],
        'min_grade': courses.aggregate(Min('avg_grade'))['avg_grade__min'],
        'max_grade': courses.aggregate(Max('avg_grade'))['avg_grade__max'],

        'courses': courses
    }

    if search:
        courses = Course.objects.filter(
            models.Q(name__iregex=search) |
            models.Q(category__iregex=search))

    if category:
        courses = courses.filter(category=category)

    courses = courses.order_by(sort)

    context = {
        'stats': stats,
        'courses': courses,
        'search_query': search,
        'current_category': category,
        'categories': Course.objects.values_list('category', flat=True).distinct(),
        'sort_fields': [
            ('name', 'По названию'),
            ('length', 'По длительности'),
            ('cost', 'По стоимости'),
            ('stud_amount', 'По количеству студентов'),
        ]
    }


    return render(request, 'statistics.html', context)


