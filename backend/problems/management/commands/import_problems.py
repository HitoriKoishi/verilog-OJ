import os
import json
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from problems.models import Problem, TestCase

class Command(BaseCommand):
    help = '从JSON文件批量导入题目'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='JSON题目文件路径')
        parser.add_argument('testcase_dir', type=str, help='测试用例文件夹路径')

    def handle(self, *args, **options):
        json_file = options['json_file']
        testcase_dir = options['testcase_dir']
        
        # 读取JSON文件
        with open(json_file, 'r', encoding='utf-8') as f:
            problems_data = json.load(f)
        
        # 导入题目
        for problem_data in problems_data:
            # 创建题目
            problem = Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                input_description=problem_data.get('input_description', ''),
                output_description=problem_data.get('output_description', ''),
                difficulty=problem_data.get('difficulty', 'medium'),
                time_limit=problem_data.get('time_limit', 1),
                memory_limit=problem_data.get('memory_limit', 256),
                is_public=problem_data.get('is_public', True)
            )
            
            # 处理测试用例
            for tc_data in problem_data['test_cases']:
                # 读取testbench文件
                tc_file_path = os.path.join(testcase_dir, tc_data['testbench_filename'])
                with open(tc_file_path, 'r') as tc_file:
                    testbench_content = tc_file.read()
                
                # 创建测试用例
                test_case = TestCase(
                    problem=problem,
                    expected_output=tc_data['expected_output']
                )
                # 保存testbench文件
                test_case.testbench_file.save(
                    tc_data['testbench_filename'],
                    ContentFile(testbench_content.encode('utf-8'))
                )
                test_case.save()
            
            self.stdout.write(self.style.SUCCESS(f'成功导入题目: {problem.title}'))
