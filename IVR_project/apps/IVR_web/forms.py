from django import forms
from IVR_project.apps.IVR_web.models import Timeline, Event


class AddTimeline(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['day_start'].empty_label = "No"
    
    class Meta:
        model = Timeline
        fields = ['name', 'photo', 'day_start', 'month_start', 'year_start', 'day_end',
                  'month_end', 'year_end', 'content', 'is_private']


class AddEvent(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'photo', 'day_start', 'month_start', 'year_start', 'day_end',
                  'month_end', 'year_end', 'content']


class ContactForm(forms.Form):
    theme = forms.CharField(
        min_length=1,
        widget=forms.TextInput(
        )
    )
    message = forms.CharField(
        min_length=10,
        widget=forms.Textarea(
        )
    )