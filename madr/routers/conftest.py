import pytest
from testcontainers.postgres import PostgresContainer
from django.db import connections

@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer('postgres:latest', driver='psycopg2') as postgres:
        yield postgres


@pytest.fixture(scope='session')
def django_db_modify_db_settings(postgres_container):
    from django.conf import settings
    
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': postgres_container.env['POSTGRES_DB'],
        'USER': postgres_container.env['POSTGRES_USER'],
        'PASSWORD': postgres_container.env['POSTGRES_PASSWORD'],
        'HOST': postgres_container.get_container_host_ip(),
        'PORT': postgres_container.get_exposed_port(5432),
    }
    
    connections.settings = connections.configure_settings(settings.DATABASES)
    connections["default"] = connections.create_connection("default")
    

