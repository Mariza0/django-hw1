from random import randrange
import pytest as pytest
from model_bakery import baker
from rest_framework import response
from rest_framework.test import APIClient
from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


def test_api(client):
    response = client.get('/api/v1/')
    assert response.status_code == 200


@pytest.fixture
def factory_courses():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def factory_student():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.mark.django_db
def test_courses(client, factory_courses):
    """проверка получения 1-го курса"""
    courses = factory_courses()
    response = client.get(path='/api/v1/courses/',)
    data = response.json()
    assert data[0]['name'] == courses.name
    assert response.status_code == 200


@pytest.mark.django_db
def test_courses_list(client, factory_courses):
    """проверка получения списка курсов (list-логика)"""
    courses = factory_courses(_quantity=20)
    response = client.get(path='/api/v1/courses/',)
    data = response.json()
    for i, n in enumerate(data):
        assert n['name'] == courses[i].name
    assert len(courses) == len(data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_courses_url(client, factory_courses):
    """проверка фильтрации списка курсов по id, name"""
    courses = factory_courses(_quantity=20)
    c_id = randrange(20)
    path = '/api/v1/courses/?id=' + str(c_id) + '/'
    response_id = client.get(f'/api/v1/courses/{courses[c_id].id}/')
    response_name = client.get(f'/api/v1/courses/?name={courses[c_id].name}')
    data_id = response_id.json()
    data_name = response_name.json()
    assert response_id.status_code == 200
    assert response_name.status_code == 200
    assert courses[c_id].name == data_id['name']
    assert courses[c_id].name == data_name[0]['name']


@pytest.mark.django_db
def test_create_course(client):
    """тест успешного создания курса"""
    count = Course.objects.count()
    response1 = client.post('/api/v1/courses/', data={'name': 'name1'})
    response2 = client.get(f'/api/v1/courses/?name={"name1"}')
    response3 = client.get(f'/api/v1/courses/{response1.json()["id"]}/')
    assert response1.status_code == 201
    assert Course.objects.count() == count + 1
    assert response2.status_code == 200
    assert response3.json()['name'] == 'name1'


@pytest.mark.django_db
def test_courses_update(client, factory_courses):
    """тест успешного обновления курса"""
    courses = factory_courses(_quantity=2)
    response1 = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'name_new'})
    response2 = client.delete(f'/api/v1/courses/{courses[1].id}/')
    response3 = client.get(f'/api/v1/courses/{courses[1].id}/')
    assert response1.status_code == 200
    assert response2.status_code == 204
    assert response3.status_code == 404
