from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AltaUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ModificacionUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']