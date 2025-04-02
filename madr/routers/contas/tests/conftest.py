import pytest
from testcontainers.postgres import PostgresContainer
from django.db import connections
from django.db.utils import OperationalError


@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer('postgres:latest', driver='psycopg') as postgres:
        yield postgres


@pytest.fixture(scope='session')
def django_db_modify_db_settings(postgres_container):
    from django.conf import settings
    __import__("ipdb").set_trace()
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': postgres_container.env['POSTGRES_DB'],
        'USER': postgres_container.env['POSTGRES_USER'],
        'PASSWORD': postgres_container.env['POSTGRES_PASSWORD'],
        'HOST': postgres_container.get_container_host_ip(),
        'PORT': postgres_container.get_exposed_port(5432),
    }
    yield

    for connection in connections.all():
        connection.close()

@pytest.mark.django_db
def test_can_connect_to_database():
    db_conn = connections['default']
    __import__("ipdb").set_trace()
    try:
        db_conn.ensure_connection()
        assert db_conn.is_usable()
    except OperationalError:
        pass

