from django.shortcuts import render, get_object_or_404
from .models import Reservoir, PlotZone
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'Hydro/index.html'
    context_object_name = 'plot_list'

    def get_queryset(self):
        return PlotZone.objects.order_by('id')


def details(request, reservoir_id):
    c = get_object_or_404(Reservoir, pk=reservoir_id)
    current_ppm = c.current_ppm
    current_ph = c.current_ph
    res = PlotZone.objects.get(pk=reservoir_id)
    current_temp = res.current_temp
    current_humid = res.current_humid
    res_id = res.id
    context = {'res_id': res_id, 'current_ppm': current_ppm, 'current_ph': current_ph, 'current_temp': current_temp,
               'current_humid': current_humid, }
    return render(request, 'Hydro/ResDetails.html', context)