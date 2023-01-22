from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}
def get_info(request):
    return render(request, 'main.html')

def get_recipe(request):
    path = request.META.get('PATH_INFO').strip('/') #omlet
    print(path)
    servings_param = request.GET.get('servings')
    print('servings_param', servings_param)
    context = {
        'recipe': DATA.get(path)
    }
    if servings_param is not None:
        context = {'recipe': {key: value * abs(int(servings_param))
                              for key, value in context.get('recipe').items()}}
    print(context)
    return render(request, 'calculator/index.html', context)

def page_not_found_view(request, exception):
    return render(request, '404.html', {})#status=404)
# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/salad.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
