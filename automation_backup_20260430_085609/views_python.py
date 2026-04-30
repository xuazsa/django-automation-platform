from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sys
from io import StringIO, BytesIO
import traceback
import json
import base64

@csrf_exempt
def execute_python(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '')
        
        # 捕获输出
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        result = {
            'output': '',
            'error': '',
            'image': '',
            'success': True
        }
        
        # 添加 matplotlib 支持
        matplotlib_code = '''
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
'''
        
        full_code = matplotlib_code + '\n' + code + '\nplt.savefig("temp_plot.png", bbox_inches="tight")\nplt.close()'
        
        try:
            exec(full_code)
            result['output'] = captured_output.getvalue()
            
            # 检查是否有生成的图片
            import os
            if os.path.exists('temp_plot.png'):
                with open('temp_plot.png', 'rb') as f:
                    result['image'] = base64.b64encode(f.read()).decode()
                os.remove('temp_plot.png')
                
        except Exception as e:
            result['error'] = traceback.format_exc()
            result['success'] = False
        finally:
            sys.stdout = old_stdout
        
        return JsonResponse(result)
    
    return render(request, 'automation/python_console.html')
