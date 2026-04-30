from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import io
import base64
import traceback

# 用于存储执行状态
execution_context = {}

@csrf_exempt
def python_console(request):
    return render(request, 'automation/python_console.html')

@csrf_exempt
def execute_python(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        code = data.get('code', '')
        input_value = data.get('input_value', None)
        session_id = data.get('session_id', 'default')
        
        # 获取或创建执行上下文
        if session_id not in execution_context:
            execution_context[session_id] = {
                'stdin_buffer': [],
                'namespace': {}
            }
        
        ctx = execution_context[session_id]
        
        # 如果有输入，存入缓冲区
        if input_value is not None:
            ctx['stdin_buffer'].append(input_value)
        
        # 自定义输入函数
        def custom_input(prompt=''):
            # 从缓冲区取输入，如果没有则等待
            if ctx['stdin_buffer']:
                return ctx['stdin_buffer'].pop(0)
            else:
                # 抛出特殊异常通知前端需要输入
                raise Exception(f"__INPUT_REQUIRED__:{prompt}")
        
        # 捕获输出
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        result = {'output': '', 'error': '', 'image': '', 'success': True}
        
        # 准备执行环境
        namespace = ctx['namespace']
        namespace['custom_input'] = custom_input
        namespace['input'] = custom_input  # 覆盖 input
        
        # 添加 matplotlib 支持
        matplotlib_code = '''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io as _io
import base64 as _base64
'''
        
        full_code = matplotlib_code + '\n' + code
        
        # 处理 plt.show()
        if 'plt.show()' in code:
            full_code = full_code.replace('plt.show()', '''
buf = _io.BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight')
buf.seek(0)
result_image = _base64.b64encode(buf.getvalue()).decode()
buf.close()
plt.close()
''')
            result['has_image'] = True
        
        try:
            exec(full_code, namespace)
            result['output'] = captured_output.getvalue()
            if 'result_image' in namespace:
                result['image'] = namespace['result_image']
                
        except Exception as e:
            error_msg = str(e)
            if error_msg.startswith('__INPUT_REQUIRED__:'):
                prompt = error_msg.split(':', 1)[1]
                result['needs_input'] = True
                result['prompt'] = prompt
                result['success'] = True
            else:
                result['error'] = traceback.format_exc()
                result['success'] = False
        finally:
            sys.stdout = old_stdout
            # 保存命名空间供下次使用（保留变量）
            ctx['namespace'] = namespace
        
        return JsonResponse(result)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
