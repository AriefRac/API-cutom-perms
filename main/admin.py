from django.contrib import admin
from .models import Modul, Category, Post

# Register your models here.
@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    readonly_fields = (
        'published',
        'created_at',
        'updated_at',
        'slug',
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at',
        'date',
        )

admin.site.register(Category)