from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Appointment
from django.contrib.auth.forms import UserChangeForm
from django import forms


class AppointmentForm(ModelForm):
    care_provider = forms.ModelChoiceField(
        queryset=None,  # Set the queryset later in __init__
        label="Care Provider",
        widget=forms.Select(attrs={'class': 'browser-default'}),
        required=False  # Set this to False initially
    )

    def __init__(self, *args, care_provider_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if care_provider_choices:
            self.fields['care_provider'].queryset = care_provider_choices
            self.fields['care_provider'].required = True

    def clean_care_provider(self):
        care_provider = self.cleaned_data['care_provider']
        if care_provider is None or care_provider.name == "---------":
            raise forms.ValidationError("Please select a valid care provider.")

        return care_provider

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'location', 'purpose', 'care_provider']


class AppointmentUpdateForm(forms.ModelForm):
    care_provider = forms.ModelChoiceField(
        queryset=None,  # Set the queryset later in __init__
        label="Care Provider",
        widget=forms.Select(attrs={'class': 'browser-default'}),
        required=False  # Set this to False initially
    )

    def __init__(self, *args, care_provider_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if care_provider_choices:
            print(f"inside if carep {care_provider_choices}")
            self.fields['care_provider'].queryset = care_provider_choices
            self.fields['care_provider'].required = True

    def clean_care_provider(self):
        care_provider = self.cleaned_data['care_provider']
        print(care_provider)
        if care_provider is None or care_provider.name == "---------":
            raise forms.ValidationError("Please select a valid care provider.")

        return care_provider

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'location', 'purpose', 'care_provider']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
