from django.shortcuts import render
from books.models import get_book_list, get_book, list_slug
from django.core.paginator import Paginator



def books_view(request):
    template = 'books/books_list.html'
    books = get_book_list()
    page_number = request.GET.get('page', '')
    print('page_number', page_number)

    if page_number == '':
        context = {'books': books}
    else:
        paging = list_slug()
        print(paging)
        paginator = Paginator(paging, 1)
        page = paginator.get_page(page_number)
        context = {'books': page}
    return render(request, template, context)

def book_view(request, slug):
    template = 'books/books_list.html'
    book = get_book(slug)
    context = {'books': book}
    return render(request, template, context)

# формирование словаря со значениями  slug
list_s = list_slug()
slug_list = sorted(list_s) #['2016-12-06', '2018-02-27', '2019-12-05', '2020-04-29', '2020-04-30']
n = 0
dict_slug = {}
while n < len(slug_list):
    dict_slug[n] = slug_list[n]
    n += 1


def pagi(request, slug):
    template = 'books/pagi.html'
    book = get_book(slug)[0]
    # получаем значение ключа по slug
    val_list = list(dict_slug.values())
    key = val_list.index(slug)
    print('key', val_list.index(slug)) # key 4

    # формируем след стр
    if key < len(slug_list)-1:
        next_slug = dict_slug[key + 1]
    else:
        next_slug = slug
    print('next', next)
    # формируем предыдущ стр
    if key >= 1:
        previous_slug = dict_slug[key - 1]
    else:
        previous_slug = slug


    context = {
        'book': book,
        'next_slug': next_slug,
        'previous_slug': previous_slug,
            }
    print(context)
    return render(request, template, context)
