from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

#  Defina a classe CustomUserAdmin
class CustomUserAdmin(UserAdmin):
    # Sobrescreve a ordem de exibição, substituindo 'username' por 'email'
    ordering = ('email',) 

    # Sobrescreve os campos que são exibidos na lista (list_display)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

    # Sobrescreve os campos que podem ser pesquisados
    search_fields = ('email', 'first_name', 'last_name')

    # Sobrescreve o Fieldsets (como os campos são agrupados na página de edição)
    # Remove qualquer referência ao 'username' se ele foi excluído no modelo.
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # Use 'email' no lugar de 'username'
        ('Personal info', {'fields': ('first_name', 'last_name', 'cpf', 'telefone')}), 
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# 2. Registre o Modelo Customizado com a sua Customização Admin
admin.site.register(CustomUser, CustomUserAdmin)