from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>自动化平台</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; text-align: center; background: #f5f5f5; }
            h1 { color: #333; }
            .menu { margin-top: 30px; display: flex; justify-content: center; flex-wrap: wrap; gap: 15px; }
            .menu a { display: inline-block; padding: 12px 25px; background: #007acc; color: white; 
                      text-decoration: none; border-radius: 5px; font-size: 16px; transition: background 0.3s; }
            .menu a:hover { background: #005a9e; }
        </style>
    </head>
    <body>
        <h1>欢迎使用自动化平台</h1>
        <div class="menu">
            <a href="/monitor/">📊 监控系统</a>
            <a href="/auto/">⚙️ 自动化平台</a>
            <a href="/blog/">📝 博客</a>
            <a href="/admin/">🔧 后台管理</a>
            <a href="/auto/python/">🐍 Python 执行器</a>
            <a href="/auto/switches/">🔄 交换机管理</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('monitor/', include('monitor.urls')),
    path('', home),
    path('auto/', include('automation.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
