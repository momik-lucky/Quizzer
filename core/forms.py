from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import AdvUser, Question, Test, TestSortModel


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = AdvUser
        fields = (
            'username', 'first_name', 'last_name', 'avatar', 'email', 'birthday', 'password1', 'password2', 'info'
        )


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'slug', 'description', 'question_quantity')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_quantity': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'question_quantity': _('Number of questions'),
        }
        ordering = ('title', )

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if Test.objects.filter(slug=new_slug).count():
            raise ValidationError("Slug isn't unique!")
        return new_slug


class TestSortForm(forms.ModelForm):
    class Meta:
        model = TestSortModel
        fields = ['sort_by']
        labels = {'sort_by': _('')}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', 'choise_1', 'choise_2', 'choise_3', 'choise_4', 'answer')
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'choise_1': forms.TextInput(attrs={'class': 'form-control'}),
            'choise_2': forms.TextInput(attrs={'class': 'form-control'}),
            'choise_3': forms.TextInput(attrs={'class': 'form-control'}),
            'choise_4': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'question': _('Question text'),
        }


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
