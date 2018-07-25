from django.contrib.auth.forms import UserCreationForm
from usuarios.models import CustomUser


class UsuarioForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
