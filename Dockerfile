FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /app
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
COPY . .

RUN uv sync 

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]