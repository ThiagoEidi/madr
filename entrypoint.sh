#!/bin/sh

# Executa as migrações do banco de dados
python manage.py migrate

# Inicia a aplicação
python manage.py runserver 0.0.0.0:8000