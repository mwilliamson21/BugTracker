from django import forms
from bugtracker.models import Ticket
# from bugtracker.models import User


class Create_ticket_form(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'filed_by',
            'status'
        ]


class login_form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
