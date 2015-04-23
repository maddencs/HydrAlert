from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Reservoir, PlotZone, ReservoirForm, PlotForm


class IndexView(generic.ListView):
    template_name = 'Hydro/index.html'
    context_object_name = 'plot_list'

    def get_queryset(self):
        return PlotZone.objects.order_by('id')


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
        else:
            print form.errors
    else:
        form = PlotForm()

    context = {'form': form, 'plot_id': plot_id, 'comments': comments, 'light_start': light_start, 'light_stop': light_stop, 'goal_temp': goal_temp, 'goal_humid': goal_humid,}
    return render(request, 'Hydro/modify_plot.html', context)