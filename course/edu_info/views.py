from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Page
# Create your views here.
def portal(request):
    return render(request, 'portal.html')



def home(request):
    page = Page.objects.get(name='Я')
    nav_pages = Page.objects.filter(show_in_nav=True)
    return render(request, 'Я.html', {'page': page, 'nav_pages': nav_pages})

def show_page(request, page_name):
    page = Page.objects.get(name=page_name)
    nav_pages = Page.objects.filter(show_in_nav=True)
    # Если страница не сокурсники, то передаем данные без изменений (нужно отобрать сокурсников для дальнейшей сортировки)
    if page_name != 'Сокурсники':
        return render(request, f'{page_name}.html', {'page': page, 'nav_pages': nav_pages})
    # Если == Сокурсники
    classmates = page.data.get('classmates', [])
    # Фильтрация
    group_filter = request.GET.get('group', 'all')
    age_filter = request.GET.get('age', 'all')
    grade_filter = request.GET.get('grade', 'all')

    if group_filter != 'all':
        classmates = [c for c in classmates if c['academic_group'] == group_filter]

    if age_filter == '22+':
        classmates = [c for c in classmates if c['age'] >= 22]
    elif age_filter == '21-':
        classmates = [c for c in classmates if c['age'] < 22]

    if grade_filter == '7+':
        classmates = [c for c in classmates if c['avg_grade'] >= 7]
    elif grade_filter == '8+':
        classmates = [c for c in classmates if c['avg_grade'] >= 8]
    elif grade_filter == '9+':
        classmates = [c for c in classmates if c['avg_grade'] >= 9]

    # Сортировка
    sort_option = request.GET.get('sort', 'full_name')
    sort_options = {
        'full_name': 'full_name',
        '-full_name': 'full_name',
        'group': 'academic_group',
        '-group': 'academic_group',
        'age': 'age',
        '-age': 'age',
        'grade': 'avg_grade',
        '-grade': 'avg_grade'}
    if sort_option in sort_options:
        sort_field = sort_options[sort_option]
        reverse_sort = sort_option.startswith('-')

        if sort_option == 'group':
            classmates = sorted(
                classmates,
                key=lambda x: int(x['academic_group'][3:]))

        elif sort_option == '-group':
            classmates = sorted(
                classmates,
                key=lambda x: int(x['academic_group'][3:]),
                reverse=True)

        else:
            classmates = sorted(
                classmates,
                key=lambda x: x.get(sort_field, ''),
                reverse=reverse_sort)

        context = {
            'page': page,
            'nav_pages': nav_pages,
            'classmates': classmates,
            'current_sort': sort_option,
            'current_group_filter': group_filter,
            'current_age_filter': age_filter,
            'current_grade_filter': grade_filter,
            'all_groups': sorted(list(set(c['academic_group'] for c in page.data.get('classmates', []))))
        }

    return render(request, 'Сокурсники.html', context)