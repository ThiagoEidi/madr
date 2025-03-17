from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn')  # Exibe essas colunas na listagem
    search_fields = ('title', 'author', 'isbn')  # Permite busca por título, autor e ISBN
    list_filter = ('published_date',)  # Adiciona filtro por data de publicação
    ordering = ('-published_date',)  # Ordena os livros do mais recente para o mais antigo
