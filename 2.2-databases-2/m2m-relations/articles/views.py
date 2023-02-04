from django.shortcuts import render

from articles.models import Article, Relationship


def articles_list(request):
    template = 'articles/news.html'
    context = {}
    ordering = '-published_at'
    object_list = Article.objects.order_by(ordering)
    # используйте этот параметр для упорядочивания результатов
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
    context = {'object_list': object_list}

    return render(request, template, context)
