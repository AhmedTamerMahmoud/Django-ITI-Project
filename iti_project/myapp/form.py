from django import forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'photoName']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'photoName': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        }


class ChangePassForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'})
        }


class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'returnTime']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'returnTime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }
