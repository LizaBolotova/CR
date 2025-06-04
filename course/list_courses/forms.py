from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        labels = {
            'name': 'Название курса',
            'description': 'Описание',
            'category': 'Направление',
            'length': 'Длительность (недели)',
            'format': 'Формат обучения',
            'cost': 'Стоимость (в рублях)',
            'sertificate': 'Наличие сертификата',
            'stud_amount': 'Количество студентов',
            'avg_grade': 'Средний балл',
            'photo': 'Фото курса',
        }
        help_texts = {
            'avg_grade': 'Введите средний балл от 0 до 10',
            'photo': 'Загрузите изображение в формате JPG/PNG',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'certificate': forms.CheckboxInput(),
        }
