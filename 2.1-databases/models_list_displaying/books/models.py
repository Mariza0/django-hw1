# coding=utf-8

from django.db import models
import re


class Book(models.Model):
    name = models.CharField(u'Название', max_length=64)
    author = models.CharField(u'Автор', max_length=64)
    pub_date = models.DateField(u'Дата публикации')
    # slug = models.SlugField(max_length=70)

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.slug = str(self.pub_date)

    def __str__(self):
        return f"'name': {self.name}, 'author': {self.author}, 'slug': {self.slug}, 'pub_date':{str(self.pub_date)}"

def get_book_list():
    book_list = Book.objects.all()
    return book_list

def get_book(slug):
    book = Book.objects.filter(pub_date=slug)
    return book

def list_slug():
    list_s = [str(element.pub_date) for element in Book.objects.all()]
    return list_s