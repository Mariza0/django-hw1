from django.db import models
import re


class Phone(models.Model):
    name = models.CharField(max_length=70)
    price = models.FloatField()
    image = models.ImageField()
    release_date = models.CharField(max_length=15)
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=70)

    def __init__(self, *args, **kwargs):
        super(Phone, self).__init__(*args, **kwargs)
        self.slug = re.sub(r'[^\w\s]+|[\d]+', r'', self.name).strip().replace(' ', '-')

    def __str__(self):
        return {self.name},{self.price},{self.lte_exists}


def list_phones(sort):
    if sort == 'name':
        list_phone = Phone.objects.order_by('name')
    elif sort == 'min_price':
        list_phone = Phone.objects.order_by('price')
    elif sort == 'max_price':
        list_phone = Phone.objects.order_by('-price')
    else:
        list_phone = Phone.objects.all()
    return list_phone


def product(slug):
    phone_model = Phone.objects.get(slug=slug)
    return phone_model
