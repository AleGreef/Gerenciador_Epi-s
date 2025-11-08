from django import forms
from .models import Emprestimos

class EmprestimosForm(forms.ModelForm):
    class Meta:
        model = Emprestimos
        fields = ['colaborador', 'epis', 'data_emprestimo', 'data_devolucao', 'status']

        widgets = {
            'data_emprestimo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'status': forms.Select(choices=[('EM', 'Emprestado'), ('DV', 'Devolvido')])
        }
