from django import forms
from .models import Colaboradores

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaboradores
        fields = ['nome_Colaborador', 'Data_nasc', 'telefone', 'email', 'cpf', 'foto_perfil']
        widgets = {
            'nome_Colaborador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'Data_nasc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Data Nascimento'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cpf'].required = True
