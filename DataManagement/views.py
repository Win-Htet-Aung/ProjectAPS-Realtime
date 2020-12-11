from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from django.http import JsonResponse
from DataManagement.models import *
from RealtimeAPS.models import *
from json import dumps

# Create your views here.
@login_required
def index(request):
    data = {'sensors':{}}
    if request.user.is_superuser:
        data['projects'] = Project.objects.all()
    else:
        data['projects'] = [i.project for i in UserProject.objects.filter(user = request.user)]
    for p in data['projects']:
        temp = [s.serial for s in p.sensors.all()]
        data['sensors'][p.name] = temp
    data['sensors'] = dumps(data['sensors'])
    return render(request, 'DataManagement/index.html', data)
