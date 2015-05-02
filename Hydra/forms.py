from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from datetimewidget.widgets import TimeWidget, DateWidget
from Hydra.models import Reservoir, PlotZone


def modify_res(request, reservoir_id):
    try:
        r = get_object_or_404(Reservoir, pk=reservoir_id)
        r.save()
    except Reservoir.DoesNotExist:
        r = None

    prepop_data = {'goal_ph_high': r.goal_ph_high, 'goal_ph_low': r.goal_ph_low, 'res_id': r.id,
                   'comments': r.reservoir_comments, 'res_change_date': r.res_change_date}
    if request.method == 'POST':
        form = ReservoirForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            return redirect('plot_list')
        else:
            print form.errors
    else:
        form = ReservoirForm(instance=r, initial=prepop_data)

    context = {'form': form, 'goal_ph_high': r.goal_ph_high, 'goal_ph_low': r.goal_ph_low, 'res_id': r.id,
               'comments': r.reservoir_comments, 'res_change_date': r.res_change_date}
    return render(request, 'Hydra/modify_res.html', context)


def modify_plot(request, plot_id):
    try:
        p = get_object_or_404(PlotZone, pk=plot_id)
    except PlotZone.DoesNotExist:
        p = None

    plot_comments = p.plot_comments
    light_start = p.light_start
    light_stop = p.light_stop
    goal_temp = p.goal_temp
    goal_humid = p.goal_humid
    plot_id = p.id
    prepop_data = {'plot_id': plot_id, 'comments': plot_comments, 'light_start': light_start,
                   'light_stop': light_stop, 'goal_temp': goal_temp, 'goal_humid': goal_humid, }
    if request.method == 'POST':
        form = PlotForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('plot_list')

        else:
            print form.errors
    else:
        form = PlotForm(instance=p, initial=prepop_data)

    context = {'form': form, 'plot_id': plot_id, 'plot_comments': plot_comments, 'light_start': light_start,
               'light_stop': light_stop, 'goal_temp': goal_temp, 'goal_humid': goal_humid, }
    return render(request, 'Hydra/modify_plot.html', context)


class PlotForm(forms.ModelForm):
    class Meta:
        model = PlotZone
        # fields = ('light_start', 'light_stop', 'goal_temp')
        exclude = ('current_temp', 'lights_on', 'current_humid', 'user', 'humid_alert_sent', 'temp_alert_sent',
                   'light_alert_sent', )
        TimeOptions = {
            'format': 'HH:ii',
            'autoclose': True,
            'showMeridian': True,
            'clearBtn': True,
        }
        widgets = {
            'light_start': TimeWidget(usel10n=True, bootstrap_version=3),
            'light_stop': TimeWidget(usel10n=True, bootstrap_version=3),
        }


class AddPlotForm(forms.ModelForm):
    class Meta:
        model = PlotZone
        exclude = ('current_temp', 'lights_on', 'current_humid', 'name', 'humid_alert_sent', 'temp_alert_sent',
                   'light_alert_sent', 'user', )
        TimeOptions = {
            'format': 'HH:ii',
            'autoclose': True,
            'showMeridian': True,
            'clearBtn': True,
        }
        widgets = {
            'light_start': TimeWidget(usel10n=True, bootstrap_version=3),
            'light_stop': TimeWidget(usel10n=True, bootstrap_version=3),
        }


class ReservoirForm(forms.ModelForm):
    class Meta:
        model = Reservoir
        exclude = ('plot', 'current_ph', 'current_ppm', 'ph_alert_sent', 'ppm_alert_sent', 'res_change_alert',)

        DateOptions = {
            'format': 'yyyy/mm/dd',
            'autoclose': True,
            'clearBtn': True,
            'todayHighlight': True,
        }

        widgets = {
            'date': DateWidget(usel10n=True, bootstrap_version=3),
        }