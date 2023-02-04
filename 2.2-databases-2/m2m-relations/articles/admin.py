from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tags, Relationship

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            print('form.cleaned_data', form.cleaned_data)
            if form.cleaned_data.get('is_main') == True:
                count += 1
            if count > 1:
                raise ValidationError('Основным может быть только один раздел')
        return super().clean()

class RelationshipInline(admin.TabularInline):
    model = Relationship
    list_display = ['tag', 'is_main']
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [RelationshipInline]


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',]
