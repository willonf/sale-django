from django.contrib import admin
from basic import models


# Register your models here.

# TODO: Página que será montada no Django Admin
@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'modified_at']
    list_display_links = ['id', 'name', 'active', 'created_at', 'modified_at']
    search_fields = ['id', 'name']
    list_filter = ['active', 'name']
    # Outros campos podem ser adicionados