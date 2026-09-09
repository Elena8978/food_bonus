from django import forms
from .models import Order, Dish, Client

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

    class Meta:
        model = Client
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class OrderForm(forms.ModelForm):
    use_bonuses = forms.BooleanField(
        required=False,
        label="Списать бонусы",
        help_text="Ваш баланс будет обнулён"
    )

    class Meta:
        model = Order
        fields = ['dish']

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
        self.fields['dish'].queryset = Dish.objects.all()
        self.fields['dish'].label = "Выберите блюдо"
        self.fields['dish'].widget = forms.Select(attrs={'class': 'form-control'})