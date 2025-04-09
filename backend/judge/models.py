from django.db import models
from django.conf import settings
from problems.models import Problem

class Submission(models.Model):
    STATUS_CHOICES = (
        ('PENDING', '等待评测'),
        ('RUNNING', '评测中'),
        ('ACCEPTED', '通过'),
        ('WRONG_ANSWER', '错误答案'),
        ('COMPILE_ERROR', '编译错误'),
        ('RUNTIME_ERROR', '运行时错误'),
        ('TIME_LIMIT_EXCEEDED', '时间超限'),
        ('MEMORY_LIMIT_EXCEEDED', '内存超限'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20, default='verilog')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    execution_time = models.FloatField(null=True, blank=True)  # 执行时间(毫秒)
    memory_used = models.IntegerField(null=True, blank=True)   # 使用内存(KB)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Submission {self.id} by {self.user.username} for problem {self.problem.title}"
