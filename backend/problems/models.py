from django.db import models

class Problem(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', '简单'),
        ('medium', '中等'),
        ('hard', '困难'),
    )
    
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述')
    input_description = models.TextField('输入说明', blank=True)
    output_description = models.TextField('输出说明', blank=True)
    difficulty = models.CharField('难度', max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    time_limit = models.FloatField('时间限制(秒)', default=1)
    memory_limit = models.IntegerField('内存限制(MB)', default=256)
    is_public = models.BooleanField('是否公开', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    # 统计信息
    submission_count = models.IntegerField('提交次数', default=0)
    accepted_count = models.IntegerField('通过次数', default=0)
    
    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['id']
    
    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name='所属题目')
    testbench_file = models.FileField('测试文件', upload_to='testcases/')
    expected_output = models.TextField('期望输出')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例'
    
    def __str__(self):
        return f"测试用例 {self.id} - {self.problem.title}"
