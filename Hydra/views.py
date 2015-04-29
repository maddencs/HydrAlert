from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Reservoir, PlotZone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
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
            print user.errors

        login(request, user)
        print ("login")
        redirect("about")

    return render(request, 'Hydra/register.html', {})


def login_view(request):
    message = ""
    # if request.user.is_authenticated:
    #     return redirect('plot_list')
    # else:
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('plot_list')
            else:
                message = "Inactive User"
        else:
            message = "Invalid Login"

    return render(request, 'Hydra/login.html', {'message': message})


def plot_list(request):
    current_user = request.user.id
    in_plot_list = []
    for plot in PlotZone.objects.all():
        if plot.user.id == current_user:
            in_plot_list.append(plot)
        else:
            pass
    context = {'plot_list': in_plot_list}
    return render(request, 'Hydra/index.html', context)


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
    plot_list = PlotZone.objects.filter(user=request.user)

    for plot in plot_list:
        grab_plot_list.append({'id': plot.id, 'comments': plot.plot_comments, 'light_start': str(plot.light_start),
                               'light_stop': str(plot.light_stop), 'current_temp': plot.current_temp,
                               'current_humid': plot.current_humid, 'goal_temp': plot.goal_temp,
                               'goal_humid': plot.goal_humid, 'light_status': plot.light_status})
        for res in plot.reservoir_set.all():
            grab_res_list.append({'id': res.id, 'plot': res.plot_id, 'current_ph': res.current_ph, 'current_ppm': res.current_ppm,
                                  'goal_ph_low': res.goal_ph_low, 'goal_ph_high': res.goal_ph_high, })

    return HttpResponse(json.dumps({'plot_list': grab_plot_list, 'res_list': grab_res_list}, indent=4),
                        content_type='application/json')


def new_plotlist(request):
    return render(request, 'Hydra/plot_page.html',{})