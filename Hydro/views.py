from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Reservoir, PlotZone, ReservoirForm


class IndexView(generic.ListView):
    template_name = 'Hydro/index.html'
    context_object_name = 'plot_list'

    def get_queryset(self):
        return PlotZone.objects.order_by('id')


def details(request, reservoir_id):
    r = get_object_or_404(Reservoir, pk=reservoir_id)
    current_ppm = r.current_ppm
    current_ph = r.current_ph
    res = PlotZone.objects.get(pk=reservoir_id)
    current_temp = res.current_temp
    current_humid = res.current_humid
    res_id = res.id
    context = {'res_id': res_id, 'current_ppm': current_ppm, 'current_ph': current_ph, 'current_temp': current_temp,
               'current_humid': current_humid, }
    return render(request, 'Hydro/ResDetails.html', context)


def modify_res(request, reservoir_id):
    try:
        r = Reservoir.objects.get(pk=reservoir_id)
        r.save()
    except Reservoir.DoesNotExist:
        r = None

    upper_ph = r.goal_ph_high
    lower_ph = r.goal_ph_low
    res_id = r.id
    if request.method == 'POST':
        form = ReservoirForm(request.POST)
        form.save()
        if form.is_valid():
            form.save(commit=True)

        else:
            print form.errors

    else:
        form = ReservoirForm()

    context = {'form': form, 'upper_ph': upper_ph, 'lower_ph': lower_ph, 'res_id': res_id}
    return render(request, 'Hydro/modify_res.html', context)