from django.core.exceptions import ValidationError
from django.db import models
from django.forms import BaseInlineFormSet

class Tags(models.Model):
    name = models.CharField(max_length=70, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    tag = models.ManyToManyField(Tags, through='Relationship',)
    #ordering = ['-published_at']

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


# class RelationshipInlineFormset(BaseInlineFormSet):
#     def clean(self):
#         print('form.cleaned_data', self.forms.cleaned_data)
#         for form in self.forms:
#             print('form.cleaned_data', form.cleaned_data['name'])
#
#             #try:
#             # В form.cleaned_data будет словарь с данными
#             # каждой отдельной формы, которые вы можете проверить
#             print('form.cleaned_data', form.cleaned_data['is_main'])
#             # вызовом исключения ValidationError можно указать админке о наличие ошибки
#             # таким образом объект не будет сохранен,
#             # а пользователю выведется соответствующее сообщение об ошибке
#             #except:
#                 #raise ValidationError('Основным может быть только один раздел')
#         return super().clean()


class Relationship(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name='scopes', verbose_name='Раздел')
    is_main = models.BooleanField(null=False, verbose_name='Основной')
    # formset = RelationshipInlineFormset


    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'