from django.shortcuts import render, redirect
from django.contrib.auth.decorators import *
from django.http import JsonResponse, FileResponse, HttpResponse
from DataManagement.models import *
from RealtimeAPS.models import *
from json import dumps, loads
from google.cloud import pubsub
import csv
import datetime
import random
import os
import requests
import websocket
import time

pdir = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = pdir + "\\MyIoT-61c1e4f98fcf.json"
subscriber = pubsub.SubscriberClient()

# Create your views here.
@login_required
def index(request):
    if request.method == 'POST':
        form = request.POST
        action = form.get('action')
        if action == 'Archive':
            serial = form.get('sensor_number')
            sensor = Sensor.objects.get(serial=serial)
            log_to_archive = []
            if sensor.type == 'TVL':
                log_to_archive = Log.objects.filter(sensor=sensor)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{serial}.csv"'
            writer = csv.writer(response)
            writer.writerow(["serial no:", serial])
            for i in log_to_archive:
                writer.writerow([str(i.loggedtime), float(i.tran), float(i.vert), float(i.long)])
            return response
        elif action == 'Delete':
            pass
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

def data_get(request, proj, serial):
    if request.user.is_superuser:
        data = {'attrs':[], 'logs':[]}
        sensor = Sensor.objects.get(serial=serial)
        if sensor.type == 'TVL':
            attrs = ['Tran', 'Vert', 'Long']
            logs = []
            for i in sensor.logs.all():
                l = {}
                l['logged_time'] = i.loggedtime
                l['tran'] = i.tran
                l['vert'] = i.vert
                l['long'] = i.long
                logs.append(l)
            data['attrs'] = attrs
            data['logs'] = logs
        elif sensor.type == 'TP':
            attrs = ['Temp']
            logs = []
            for i in sensor.tplogs.all():
                l = {}
                l['logged_time'] = i.loggedtime
                l['temp'] = i.temp
                logs.append(l)
            data['attrs'] = attrs
            data['logs'] = logs
        return JsonResponse(data)
    return redirect('/')

def data_upload(request):
    if request.method == 'POST':
        form = request.POST
        proj = form.get('project_name')
        serial = form.get('sensor_number')
        stype = Sensor.objects.get(serial=serial).type
        datafile = request.FILES.get('data_file')
        process_data(proj, serial, stype, datafile)
    return redirect('/')

def process_data(proj, snum, stype, file):   #data processing
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    sensor = Sensor.objects.get(serial=snum)
    if (stype == "TVL"): #need to change later
        log_data = file.readlines()[::-1]
        logs = []
        for l in log_data:
            log = l.decode('utf-8')
            if not log[0].isdigit():
                date = log.split()
                yy = int(date[-1])
                mm = month.index(date[0]) + 1
                dd = int(date[1][:-1])
                break
            else:
                log = log.split()
                time = log[0]
                td = float(log[1])
                vd = float(log[3])
                ld = float(log[5])
                logs.append([time,td,vd,ld])
        for l in logs:
            Log(sensor=sensor, loggedtime=f"{yy}-{mm}-{dd} {l[0]}", tran=l[1], vert=l[2], long=l[3]).save()
    elif (stype == "EL"):
        log_data = file.readlines()
        for i in log_data[10:]:
            log = i.decode('utf-8').strip()
            time, temp, aaxis, baxis = log.split(',')[:4]
            date, time = time.split()
            mm, dd, yy = map(int, date.split('/'))
            TiltLog(sensor=sensor, loggedtime=f"{yy}-{mm}-{dd} {time}:00", temp = float(temp), aaxis=float(aaxis), baxis=float(baxis)).save()
    elif (stype == "TP"):
        for i in range(20):
            now = datetime.datetime.now()
            mm, dd, yy = now.month, now.day, now.year
            hh, mm = now.hour, now.minute
            time = f"{hh}:{mm}"
            temp = random.randint(4000, 9999) / 1000
            TPLog(sensor=sensor, loggedtime=now, temp=temp).save()
        print('Ok')

@login_required
def chart(request, serial):
    data = {'chartinfo': {}}
    sensor = Sensor.objects.get(serial=serial)
    data['chartinfo']['serial'] = sensor.serial
    data['chartinfo']['sensor_type'] = sensor.type
    if sensor.type == 'TVL':
        datasets = {}
        data['chartinfo']['labels'] = [t['loggedtime'].strftime("%H:%M") for t in Log.objects.values('loggedtime').order_by('loggedtime')]
        for i in ['tran', 'vert', 'long']:
            temp = [float(j[i]) for j in Log.objects.values(i).order_by('loggedtime')]
            datasets[i] = temp
        data['chartinfo']['datasets'] = datasets
        data['chartinfo'] = dumps(data['chartinfo'])
    elif sensor.type == 'TP':
        datasets = {}
        data['chartinfo']['labels'] = []
        for i, t in enumerate(TPLog.objects.values('loggedtime').order_by('-loggedtime')):
            data['chartinfo']['labels'].insert(0, t['loggedtime'].strftime("%H:%M"))
            if i == 19:
                break
        datasets['temp'] = []
        for i, j in enumerate(TPLog.objects.values('temp').order_by('-loggedtime')):
            datasets['temp'].insert(0, float(j['temp']))
            if i == 19:
                break
        data['chartinfo']['datasets'] = datasets
        data['chartinfo'] = dumps(data['chartinfo'])

    data['sensor'] = sensor
    return render(request, 'DataManagement/chart.html', data)
