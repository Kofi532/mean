from django import forms
from .models import use, sch_reg, act, class_fee, classn
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','email','password']

class PostForm(forms.ModelForm):

    class Meta:
        model = use
        fields = ['username']

class RegForm(forms.ModelForm):

    class Meta:
        model = sch_reg
        fields = ['full_sch', 'contact_details']

class ActTerm(forms.ModelForm):

    class Meta:
        model = act
        fields = ['active_term']

class FeeForm(forms.ModelForm):
    class Meta:
        model = class_fee
        fields = ['classes', 'fee']

class ClassnForm(forms.ModelForm):

    class Meta:
        model = classn
        fields = ['classA', 'classB', 'classC', 'classD', 'classE', 'classF', 'classG', 'classH','classI','classJ', 'classK', 'classL', 'classM', 'classN', 'classO']

