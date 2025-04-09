from django.contrib import admin
from .models import Problem, TestCase

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'difficulty', 'created_at', 'is_public')
    list_filter = ('difficulty', 'is_public')
    search_fields = ('title', 'description')
    inlines = [TestCaseInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'difficulty', 'is_public')
        }),
        ('题目内容', {
            'fields': ('description', 'input_description', 'output_description')
        }),
        ('限制', {
            'fields': ('time_limit', 'memory_limit')
        }),
    )
