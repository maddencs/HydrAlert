import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HydrAlert.settings')

import django

django.setup()

from django.contrib.auth.models import User
from Hydra.models import AlertEmail, PlotZone, Reservoir
from datetime import datetime
from hydralib import within_range, light_check, compile_alerts


def check_stats():
    time_now = datetime.now().time()
    for user in User.objects.all():
        alert_plts = []
        alert_res_lst = []
        for plot in PlotZone.objects.filter(user=user):
            reservoirs = Reservoir.objects.filter(plot=plot)
            plot.check_alerts()
            for reservoir in reservoirs:
                ph = reservoir.current_ph
                temp = plot.current_temp
                goal_ph_low = reservoir.goal_ph_low
                goal_ph_high = reservoir.goal_ph_high
                goal_temp = plot.goal_temp
                if (ph <= goal_ph_low) and not reservoir.ph_alert:
                    # email, created = AlertEmail.objects.get_or_create(user=plot.user, toaddrs=plot.user.email, plot_zone=plot,
                    #                                                   res=reservoir, time_failed=str(timezone.now()),
                    #                                                   msg="pH too low in Reservoir %s.")
                    # send_email(email)
                    reservoir.ph_alert = True
                    alert_res_lst.append(reservoir)
                elif ph >= goal_ph_high:
                        if not reservoir.ph_alert:
                            # email, created = AlertEmail.objects.get_or_create(user=plot.user,toaddrs=plot.user.email, plot_zone=plot,
                            #                                                   res=reservoir, time_failed=str(timezone.now())
                            #                                                   , msg="pH too high in Reservoir %s.")
                            # send_email(email)
                            reservoir.ph_alert = True
                            alert_res_lst.append(reservoir)
                elif not within_range(goal_temp, temp, 5):
                    if not plot.temp_alert:
                        # email, created = AlertEmail.objects.get_or_create(toaddrs=plot.user.email, plot_zone=plot,
                        #                                                   res=reservoir, time_failed=str(timezone.now()),
                        #                                                   msg="Temperature is currently %s which is 5 degrees"
                        #                                                       "out of range of your goal temp of %s")
                        # send_email(email)
                        plot.temp_alert = True
                        alert_plts.append(reservoir)

                elif not light_check(plot, time_now):
                    # email, created = AlertEmail.objects.get_or_create(user=plot.user.email, plot_zone=plot,
                    #                                                   res=reservoir, time_failed=str(timezone.now()),
                    #                                                   msg="Temperature is currently %s which is 5 degrees "
                    #                                                       "out of range of your goal temp of %s")
                    # send_email(email)
                    plot.light_alert = True
                    alert_plts.append(reservoir)
        compile_alerts(user=user, email_plot_list=alert_plts, res_list=alert_res_lst)

if __name__ == '__main__':
    check_stats()