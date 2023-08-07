from django import forms
from leads.models import Agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

user = get_user_model()

class AgentCreateForm(forms.ModelForm):
    class Meta:
        model = user
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',   
        )