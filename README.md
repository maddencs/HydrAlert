# HydrAlert
Hydroponics monitoring app.
Receives statistics from pH, ppm, temperature, light, and humidity sensors.
Hydra is the main application. From the main plot page you can create new "plots" which can be viewed as a grow tent or greenhouse.
In each plot you can add multiple reservoirs which and monitor their individual statistics from there. The sensor addition isn't quite
hammered out yet, because I don't actually have the hardware to set it up with. But in theory the data is sent to the URL and my update view updates the database.

To add a new reservoir you can right click on a plot or reservoir and select the new reservoir button. From here you can also move the reservoir to a different plot, modify plot and reservoir goals,  and delete plots and reservoirs.
