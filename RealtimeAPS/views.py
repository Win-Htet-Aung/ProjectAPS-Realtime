from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import *
from RealtimeAPS.models import *
from DataManagement.models import *
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
    return render(request, 'RealtimeAPS/index.html', data)

def login(request):
    if request.method == 'POST':
        form = request.POST
        username = form.get('username')
        password = form.get('password')
        user = auth.authenticate(request, username = username, password = password)
        if user:
            auth.login(request, user)
            return redirect('/')
    return render(request, 'RealtimeAPS/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def users(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = request.POST
            action = form.get('action')
            if action == 'Add':
                return redirect('/users/add/')
            elif action == 'Remove':
                for x in [int(i) for i in form if i.isdigit()]:
                    User.objects.get(id = x).delete()
        data = {}
        data['users'] = User.objects.filter(is_superuser=False)
        return render(request, 'RealtimeAPS/users.html', data)
    return redirect('/')

def user_detail(request, pk):
    if request.user.is_superuser or request.user.id == pk:
        if request.method == 'POST':
            form = request.POST
            action = form.get('action')
            if action == 'Save':
                username = form.get('username')
                email = form.get('email')
                companyname = form.get('company_name')
                phone = form.get('phone')
                u = User.objects.filter(id = pk)
                info = u[0].info
                u.update(username = username, email = email)
                info.companyname = companyname
                info.phone = phone
                info.save()
        data = {}
        data['user'] = User.objects.get(id = pk)
        return render(request, 'RealtimeAPS/user_detail.html', data)
    return redirect('/')

def user_add(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = request.POST
            username = form.get('username')
            email = form.get('email')
            password = form.get('password')
            user = User.objects.create_user(username = username, password = password, email = email, is_staff = False, is_superuser = False)
            user_info = UserInfo(user=user, companyname='', phone='')
            user_info.save()
            return redirect('/users/')
        return render(request, 'RealtimeAPS/user_add.html')
    return redirect('/')

def projects(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = request.POST
            action = form.get('action')
            if action == 'Add':
                return redirect('/projects/add/')
            elif action == 'Remove':
                for x in [int(i) for i in form if i.isdigit()]:
                    Project.objects.get(id = x).delete()
        data = {}
        data['projects'] = Project.objects.all()
        return render(request, 'RealtimeAPS/projects.html', data)
    return redirect('/')

@login_required
def project_detail(request, pk):
    if request.user.is_superuser or (request.user in [i.user for i in UserProject.objects.filter(project_id=pk)]):
        if request.method == 'POST':
            form = request.POST
            action = form.get('action')
            if action == 'Save':
                proj_name = form.get('project_name')
                proj = Project.objects.get(id = pk)
                proj.name = proj_name
                proj.save()
            elif action == 'Cancel':
                return redirect('/projects/')
        data = {}
        data['project'] = Project.objects.get(id = pk)
        return render(request, 'RealtimeAPS/project_detail.html', data)
    return redirect('/')

def project_add(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = request.POST
            proj_name = form.get('project_name')
            proj = Project(name=proj_name)
            proj.save()
            return redirect(f'/projects/{proj.id}/')
        return render(request, 'RealtimeAPS/project_add.html')
    return redirect('/')

def project_user_add(request, pk):
    if request.user.is_superuser:
        proj = Project.objects.get(id = pk)
        if request.method == 'POST':
            form = request.POST
            action = form.get('action')
            if action == 'Remove':
                for x in [int(i) for i in form if i.isdigit()]:
                    user = User.objects.get(id = x)
                    UserProject.objects.get(user=user, project=proj).delete()
            else:
                username = form.get('username')
                user = User.objects.get(username=username)
                UserProject(user=user, project=proj).save()
            return redirect(f'/projects/{pk}/')
        data = {}
        users = User.objects.filter(is_superuser=False)
        users_assigned = [i.user.username for i in UserProject.objects.filter(project=proj)]
        data['users'] = users.exclude(username__in=users_assigned)
        data['project'] = proj
        return render(request, 'RealtimeAPS/project_user_add.html', data)
    return redirect('/')

def project_sensor_add(request, pk):
    if request.user.is_superuser:
        proj = Project.objects.get(id = pk)
        if request.method == 'POST':
            form = request.POST
            action = form.get('action')
            if action == 'Remove':
                for x in [int(i) for i in form if i.isdigit()]:
                    user = User.objects.get(id = x)
                    UserProject.objects.get(user=user, project=proj).delete()
            else:
                serial = form.get('serial')
                s_type = form.get('sensor_type')
                sensor = Sensor(serial = serial, type = s_type, project = proj)
                sensor.save()
            return redirect(f'/projects/{pk}/')
        data = {}
        data['project'] = proj
        return render(request, 'RealtimeAPS/project_sensor_add.html', data)
    return redirect('/')
