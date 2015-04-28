from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Reservoir, PlotZone, ReservoirForm, PlotForm, AddPlotForm, AddReservoirForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def register(request):
    if request.POST:
        user = User.objects.create_user(username=request.POST["username"], password=request.POST["password"])
        user.save()

        user = authenticate(username=request.POST["username"], password=request.POST["password"])
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
                #redirect to a success page
                return redirect('plot_list')
            else:
                message = "Inactive User"
        else:
            #return invalid login message
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


def modify_res(request, reservoir_id):
    try:
        r = get_object_or_404(Reservoir, pk=reservoir_id)
        r.save()
    except Reservoir.DoesNotExist:
        r = None

    comments = r.reservoir_comments
    upper_ph = r.goal_ph_high
    lower_ph = r.goal_ph_low
    res_id = r.id
    if request.method == 'POST':
        form = ReservoirForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            redirect('modify_res')
        else:
            print form.errors
    else:
        form = ReservoirForm()

    context = {'form': form, 'upper_ph': upper_ph, 'lower_ph': lower_ph, 'res_id': res_id,'comments': comments}
    return render(request, 'Hydro/modify_res.html', context)


def modify_plot(request, plot_id):
    try:
        p = get_object_or_404(PlotZone, pk=plot_id)
        p.save()
    except PlotZone.DoesNotExist:
        p = None

    comments = p.plot_comments
    light_start = p.light_start
    light_stop = p.light_stop
    goal_temp = p.goal_temp
    goal_humid = p.goal_humid
    plot_id = p.id
    if request.method == 'POST':
        form = PlotForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('index')

        else:
            print form.errors
    else:
        form = PlotForm()

    context = {'form': form, 'plot_id': plot_id, 'comments': comments, 'light_start': light_start, 'light_stop': light_stop, 'goal_temp': goal_temp, 'goal_humid': goal_humid,}
    return render(request, 'Hydro/modify_plot.html', context)


def add_plot_page(request):
    p = PlotZone(user=request.user)
    if request.method == 'POST':
        form = AddPlotForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('plot_list')
        else:
            print form.errors
    else:
        form = AddPlotForm()

    context = {'form': form,}
    return render(request, 'Hydro/add_plot.html', context)


def add_res_page(request, plot_id):
    plot = get_object_or_404(PlotZone, pk=plot_id)

    r = Reservoir(plot=plot)
    if request.method == 'POST':
        form = AddReservoirForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print form.errors
    else:
        form = AddReservoirForm()

    context = {"form": form, "plot_id": plot.id}
    return render(request, 'Hydro/add_res.html', context)