from factory.django import DjangoModelFactory
from .models import User
from factory import Sequence, LazyAttribute

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: f'test{n}')
    email = LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = LazyAttribute(lambda obj: f'{obj.username}@example.com')