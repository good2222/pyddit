from django import forms
from .models import Announcement, Comment, User


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Придумайте пароль"}),
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите электронную почту"}),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = self.cleaned_data['password1']
        if commit:
            user.save()
        return user

