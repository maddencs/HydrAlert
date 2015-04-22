from django import forms
from Hydro.models import Reservoir


class ReservoirForm(forms.ModelForm):
    name = forms.CharField(max_length=128, unique=True, help_text="Please enter a name to identify the reservoir.", )
    upper_ph = forms.IntegerField(widget=forms.HiddenInput(),)
    lower_ph = forms.IntegerField(max_value=14, min_value=0,)
    temp_goal = forms.IntegerField(min_value=0, max_value=120,)

    class Meta:
        model = Reservoir
        fields = ('id',)