from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'owner', 'created_at', 'due_date']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
    fieldsets = [
        ('Informations de base', {
            'fields': ['title', 'description', 'owner']
        }),
        ('Statut et priorité', {
            'fields': ['status', 'priority', 'due_date']
        }),
        ('Informations de suivi', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
