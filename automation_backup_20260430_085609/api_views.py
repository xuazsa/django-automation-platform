from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Switch
from .services.switch_service import SwitchService

@api_view(['POST'])
def switch_backup(request):
    import json
    try:
        data = json.loads(request.body)
        switch = Switch.objects.get(pk=data.get('switch_id'))
    except:
        return Response({'success': False, 'error': '参数错误'})
    
    success, msg = SwitchService.backup_config(switch)
    return Response({'success': success, 'error': '' if success else msg})
