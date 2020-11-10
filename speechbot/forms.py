from django import forms

from .models import UserDetails
class UserDetailsForm(forms.ModelForm):
    class Meta():
        model=UserDetails
        exclude=["userid", "firstname", "lastname","age", "gender", "email", "address", "statecode" ]
