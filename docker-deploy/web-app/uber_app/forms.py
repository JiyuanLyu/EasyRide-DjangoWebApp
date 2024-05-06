from django import forms
from django.forms.widgets import TextInput, DateTimeInput, CheckboxInput, NumberInput
from django.utils import timezone
from .models import Ride, User, RideSharer
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
       
class RideRequestForm(forms.Form):
    destination = forms.CharField(widget=TextInput(attrs={'placeholder': 'Where are you going?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    required_arrival_date_time = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local', 
                                                                                 'class': 'form-control', 
                                                                                 'style': 'width: 100%;'}, format='%Y-%m-%dT%H:%M'))
    vehicle_type = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Want a specified vehicle type?',
                                                                           'class': 'form-control', 
                                                                           'style': 'width: 100%;'}), max_length=255)
    special_request = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Any special requests?',
                                                                              'class': 'form-control',
                                                                              'style': 'width: 100%;'}), max_length=255)
    shared = forms.ChoiceField(choices=[(True, 'Yes'), (False, 'No')],
                               widget=forms.Select(attrs={'class': 'form-control'}), 
                               initial='No')
    owner_passenger_num = forms.IntegerField(widget=NumberInput(attrs={'min': 1}))
    
    # def clean_required_arrival_date_time(self):
    #     data = self.cleaned_data['required_arrival_date_time']
    #     if data < timezone.now():
    #         raise ValidationError('Arrival time cannot be in the past.')
    #     return data

class SharerRequestForm(forms.Form):
    destination = forms.CharField(widget=TextInput(attrs={'placeholder': 'Where are you going?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    earliest_arrival_date_time = forms.DateTimeField(widget=DateTimeInput(attrs={'placeholder': 'The earliest estimate arrival time',
                                                                                 'type': 'datetime-local', 
                                                                                 'class': 'form-control', 
                                                                                 'style': 'width: 100%;'}, format='%Y-%m-%dT%H:%M'))
    latest_arrival_date_time = forms.DateTimeField(widget=DateTimeInput(attrs={'placeholder': 'The latest estimate arrival time',
                                                                                'type': 'datetime-local', 
                                                                                 'class': 'form-control', 
                                                                                 'style': 'width: 100%;'}, format='%Y-%m-%dT%H:%M'))
    sharer_passenger_num = forms.IntegerField(widget=NumberInput(attrs={'min': 1}))


class UserFrom(forms.Form):
    email_address = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are you email adress?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    user_name = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'What is your name?',
                                                                           'class': 'form-control', 
                                                                           'style': 'width: 100%;'}), max_length=255)
    password = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Please type your password',
                                                                              'class': 'form-control',
                                                                              'style': 'width: 100%;'}), max_length=255)


class VehicleForm(forms.Form):
    driver_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your legal name?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    vehicle_type = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your vehicle type?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    license_plate = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your license plate number?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)    
    max_passengers = forms.CharField(widget=NumberInput(attrs={'min': 1}))                                             
    special_vehicle_info = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Do you have some special info want to share?',
                                                                                   'class': 'form-control',
                                                                                   'style': 'width: 100%;'}), max_length=255)


class LoginForm(forms.Form):
    user_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'What is email adress?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    password = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your password?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Account'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SharerEditForm(forms.Form):
    sharer_passenger_num = forms.IntegerField(widget=NumberInput(attrs={'min': 1}))


# class EditUserFrom(forms.Form):
#     email_address = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are you email adress?',
#                                                           'class': 'form-control',
#                                                           'style': 'width: 100%;'}), max_length=255)
#     user_name = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'What is your name?',
#                                                                            'class': 'form-control', 
#                                                                            'style': 'width: 100%;'}), max_length=255)
    # password = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Please type your password',
    #                                                                           'class': 'form-control',
    #                                                                           'style': 'width: 100%;'}), max_length=255)

class EditUserForm(forms.Form):
    email_address = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%;'
    }), max_length=255)
    
    user_name = forms.CharField(required=False, widget=TextInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%;'
    }), max_length=255)

    def __init__(self, *args, **kwargs):
        # If a user instance is passed in, extract it and use its data for placeholders
        user_instance = kwargs.pop('instance', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

        # If an instance is provided, set placeholders to current user info
        if user_instance:
            self.fields['email_address'].widget.attrs['placeholder'] = user_instance.email_address
            self.fields['user_name'].widget.attrs['placeholder'] = user_instance.user_name

class EditDriverForm(forms.Form):
    driver_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your legal name?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    vehicle_type = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your vehicle type?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)
    license_plate = forms.CharField(widget=TextInput(attrs={'placeholder': 'What are your license plate number?',
                                                          'class': 'form-control',
                                                          'style': 'width: 100%;'}), max_length=255)    
    max_passengers = forms.IntegerField(widget=NumberInput(attrs={'min': 1}))                                             
    special_vehicle_info = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Do you have some special info want to share?',
                                                                                   'class': 'form-control',
                                                                                   'style': 'width: 100%;'}), max_length=255)

    def __init__(self, *args, **kwargs):
        # If a user instance is passed in, extract it and use its data for placeholders
        user_instance = kwargs.pop('instance', None)
        super(EditDriverForm, self).__init__(*args, **kwargs)

        # If an instance is provided, set placeholders to current user info
        if user_instance:
            self.fields['driver_name'].widget.attrs['placeholder'] = user_instance.driver_name
            self.fields['vehicle_type'].widget.attrs['placeholder'] = user_instance.vehicle_type

            self.fields['license_plate'].widget.attrs['placeholder'] = user_instance.license_plate
            self.fields['max_passengers'].widget.attrs['placeholder'] = user_instance.max_passengers
            self.fields['special_vehicle_info'].widget.attrs['placeholder'] = user_instance.special_vehicle_info