from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите электронную почту"}),
    )
    first_name = forms.CharField(
        required=False,
        label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя (опционально)"}),
    )
    last_name = forms.CharField(
        required=False,
        label="Фамилия",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите фамилию (опционально)"}),
    )
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
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя пользователя"}),
        }
        labels = {
            'username': 'Имя пользователя',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя пользователя"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Электронная почта"}),
            'first_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Фамилия"}),
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})
            field.label = field.label

