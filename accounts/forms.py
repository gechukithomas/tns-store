from django import forms
from .models import Account, UserProfile, contact_page_messages


class RegistrationForm(forms.ModelForm):
    class Meta:
        model   = Account
        fields  = ['first_name', 'last_name', 'phone_number', 'email', 'password']

class UserForm(forms.ModelForm):
    class Meta:
        model   = Account
        fields  = ('first_name', 'last_name', 'phone_number')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model       = UserProfile
        fields      = ( 'address_line_1', 'address_line_2', 'image', 'bio_description')       

class Contact_page_messages(forms.ModelForm):
    class Meta:
        model       = contact_page_messages
        fields      = ['username', 'email', 'subject', 'message']         