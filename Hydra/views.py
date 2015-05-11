from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Reservoir, PlotZone, Sensors
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json


def register(request):
    if request.POST:
        user = User.objects.create_user(username=request.POST["Username"], password=request.POST["Password"])
        user.save()
        if user.is_active:
            user = authenticate(username=request.POST["Username"], password=request.POST["Password"])
            login(request, user)
            return redirect('plot_list')
        else:
            print(user.errors)

        login(request, user)

    return render(request, 'Hydra/register.html', {})


def login_view(request):
    message = ""
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('plot_list')
            else:
                message = "Inactive User"
        else:
            message = "Invalid Login"

    return render(request, 'Hydra/login.html', {'message': message})


def logout_view(request):
    if request.POST:
        return logout(request)


@login_required(login_url='/Hydra/login/')
def details(request, reservoir_id):
    r = get_object_or_404(Reservoir, pk=reservoir_id)
    current_ppm = r.current_ppm
    current_ph = r.current_ph
    plot = PlotZone.objects.get(pk=reservoir_id)
    current_temp = plot.current_temp
    current_humid = plot.current_humid
    res_id = plot.id
    context = {'res_id': res_id, 'current_ppm': current_ppm, 'current_ph': current_ph, 'current_temp': current_temp,
               'current_humid': current_humid, }
    return render(request, 'Hydra/ResDetails.html', context)


def data_grab(request):
    grab_plot_list = []
    grab_res_list = []
    _plot_list = PlotZone.objects.filter(user=request.user)

    for plot in _plot_list:
        grab_plot_list.append({'id': plot.id, 'comments': plot.plot_comments, 'light_start': str(plot.light_start),
                               'light_stop': str(plot.light_stop), 'current_temp': plot.current_temp,
                               'current_humid': plot.current_humid, 'goal_temp': plot.goal_temp,
                               'goal_humid': plot.goal_humid, 'light_status': plot.light_status,
                               'alert_status': plot.alert_status, })
        for res in plot.reservoir_set.all():
            grab_res_list.append({'id': res.id, 'plot': res.plot_id, 'current_ph': res.current_ph,
                                  'current_ppm': res.current_ppm, 'goal_ph_low': res.goal_ph_low,
                                  'goal_ph_high': res.goal_ph_high, 'alert_status': res.alert_status, })

    return HttpResponse(json.dumps({'plot_list': grab_plot_list, 'res_list': grab_res_list}, indent=4),
                        content_type='application/json')


@login_required(login_url='/Hydra/login/')
def plot_list(request, **kwargs):
    context = {'message': ""}
    message = kwargs.pop('message', "")
    main_plot_list = PlotZone.objects.all()
    context['dropdown_plot_list'] = main_plot_list
    context['message'] = message
    return render(request, 'Hydra/plot_page.html', context)


@login_required(login_url='/Hydra/login/')
def add_plot(request):
    if request.method == 'POST':
        p = PlotZone()
        p.save()
        p.user.add(request.user)
        p.light_start = request.POST['light_start']
        p.light_stop = request.POST['light_stop']
        p.goal_temp = request.POST['goal_temp']
        p.goal_humid = request.POST['goal_humid']
        p.save()
        return HttpResponse()


@login_required(login_url='/Hydra/login/')
def add_res(request):
    if request.method == 'POST':
        r = Reservoir()
        r.plot = PlotZone.objects.get(pk=request.POST['plot'])
        r.goal_ph_high = request.POST['goal_ph_high']
        r.goal_ph_low = request.POST['goal_ph_low']
        r.goal_ppm = request.POST['goal_ppm']
        # r.ppm_tolerance = request.POST['ppmTolerance']
        r.save()
        # return HttpResponse()


def create_email(request, **kwargs):
    email_plot_list = kwargs.pop('plot_list', [])
    res_list = kwargs.pop('res_list', [])
    context = {'plot_list': email_plot_list, 'res_list': res_list, }
    return render(request, 'Hydra/alert_email.html', context)

@login_required(login_url='/Hydra/login/')
def delete_plot(request, plot_id):
    p = PlotZone.objects.filter(id=plot_id)
    res_lst = Reservoir.objects.filter(plot=p)
    p.delete()
    for res in res_lst:
        res.delete()
    return redirect('plot_list')

@login_required(login_url='/Hydra/login/')
def delete_res(request, res_id):
    r = Reservoir.objects.get(id=res_id)
    r.delete()
    return redirect('plot_list')

@login_required(login_url='/Hydra/login/')
def add_sensor(request, res_id):
    if request.method == 'POST':
        pin = request.POST['pin']
        s_type = request.POST.get('type')
        res = Reservoir.objects.get(pk=res_id)
        sensor = Sensors(type=s_type, res=res, sensor_pin=pin)
        sensor.save()

        return redirect('plot_list')
    return render(request, 'Hydra/add_sensor.html', {'res_id': res_id})

@login_required(login_url='/Hydra/login/')
def change_info(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST['email']
        user.name = request.POST['name']
        user.save()
        return HttpResponse()