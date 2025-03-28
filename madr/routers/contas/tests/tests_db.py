from madr.routers.contas.factories import UserFactory
import pytest

@pytest.mark.django_db(serialized_rollback=True)
def test_str_method():
    username = 'xpto'
    user = UserFactory(username=username)

    assert str(user) == username

@pytest.mark.django_db(serialized_rollback=True)
@pytest.mark.parametrize(
    ('username', 'username_sanitizado'),
    [
        ('Machado De Assis', 'machado de assis'),
        ('Manuel        Bandeira', 'manuel bandeira'),
        ('Edgar Alan Poe         ', 'edgar alan poe'),
        ('Androides Sonham Com Ovelhas Elétricas?', 'androides sonham com ovelhas elétricas'),
        ('  breve  história  do tempo ', 'breve história do tempo'),
        ('O mundo assombrado pelos demônios', 'o mundo assombrado pelos demônios'),
    ]
)
def test_sanitizar_username(username: str, username_sanitizado: str):
    user = UserFactory(username=username)
    user.sanitizar_username()
    assert user.username == username_sanitizado

@pytest.mark.django_db(serialized_rollback=True)
def test_save_method():
    username = 'Manuel        Bandeira'
    user = UserFactory.build(username=username)

    user.save()

    assert user.username == 'manuel bandeira'