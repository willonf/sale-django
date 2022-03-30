from django.contrib import admin
from basic import models


# Register your models here.
@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'modified_at']
    list_display_links = ['id', 'name', 'active', 'created_at', 'modified_at']
    search_fields = ['id', 'name']
    list_filter = ['active', 'name']
