from django.db import models
from datetime import datetime

class Colaboradores(models.Model):
    id_col = models.AutoField(primary_key=True)
    nome_Colaborador = models.CharField(max_length=45, blank=True, null=True)
    Data_nasc = models.CharField(max_length=12, blank=True, null=True)
    telefone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=45, blank=True, null=True)
    senha = models.CharField(max_length=45, blank=True, null=True)
    cpf = models.CharField(unique=True, max_length=11, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='media/', blank=True, null=True)

    class Meta:
        db_table = 'colaboradores'

    def __str__(self):
        return self.nome_colaborador
    
    def save(self, *args, **kwargs):
        if self.cpf:  # só tenta limpar se houver valor
            self.cpf = ''.join(filter(str.isdigit, self.cpf))
        super().save(*args, **kwargs)


    def format_cpf(self):
        """Retorna o CPF formatado: 000.000.000-00"""
        if len(self.cpf) == 11:
            return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"
        return self.cpf or ''

    def format_telefone(self):
        """Retorna o telefone formatado: (00) 00000-0000 ou (00) 0000-0000"""
        if not self.telefone:
            return ''
        if len(self.telefone) == 11:
            return f"({self.telefone[:2]}) {self.telefone[2:7]}-{self.telefone[7:]}"
        elif len(self.telefone) == 10:
            return f"({self.telefone[:2]}) {self.telefone[2:6]}-{self.telefone[6:]}"
        return self.telefone

    def format_Data_nasc(self):
        if not self.Data_nasc:
            return ''
    
        data_str = str(self.Data_nasc).strip()

        # Tenta converter de 'YYYY-MM-DD' → 'DD/MM/YYYY'
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d')
            return data.strftime('%d/%m/%Y')
        except ValueError:
            pass

        # Se já estiver em 'DD/MM/YYYY', retorna igual
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return data_str
        except ValueError:
            pass

        # Se estiver em outro formato, retorna o valor cru (sem quebrar)
        return data_str


class Setores(models.Model):
    id_setores = models.AutoField(primary_key=True)
    nome_setor = models.CharField(max_length=45, blank=True, null=True)
    
    class Meta:
        db_table = 'setores'

    def __str__(self):
        return self.nome_setor
    
class Equipamentos(models.Model):
    id_Equipamentos = models.AutoField(primary_key=True)
    nome_equipamento = models.CharField(max_length=45, blank=True, null=True)
    fabricante = models.CharField(max_length=45, blank=True, null=True)
    data_validade = models.CharField(max_length=45, blank=True, null=True)
    estoque = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'equipamentos'

    def __str__(self):
        return self.nome_equipamento
