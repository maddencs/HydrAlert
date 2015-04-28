from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import Reservoir, PlotZone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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

    return render(request, 'Hydro/register.html', {})


def login_view(request):
    message = ""

    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('plot_list')
            else:
                message = "Inactive User"
        else:
            message = "Invalid Login"

    return render(request, 'Hydro/login.html', {'message': message})


def plot_list(request):
    current_user = request.user.id
    in_plot_list = []
    for plot in PlotZone.objects.all():
        if plot.user.id == current_user:
            in_plot_list.append(plot)
        else:
            pass
    context = {'plot_list': in_plot_list}
    return render(request, 'Hydro/index.html', context)


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
    return render(request, 'Hydro/ResDetails.html', context)