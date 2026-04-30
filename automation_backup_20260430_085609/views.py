from django.shortcuts import render
from .models import Switch

def switch_list(request):
    switches = Switch.objects.all()
    return render(request, 'automation/switch_list.html', {'switches': switches})
