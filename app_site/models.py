from django.db import models
from datetime import datetime
from django.conf import settings


class Colaboradores(models.Model):
    id_col = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    cpf = models.CharField(unique=True, max_length=11, blank=True, null=True)
    nome_colaborador = models.CharField(max_length=155, blank=True, null=True)
    data_nasc = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=45, blank=True, null=True)
    senha = models.CharField(max_length=255, blank=True, null=True)
    tipo_colaborador = models.CharField(max_length=30, blank=True, null=True)
    delete_flag = models.CharField(max_length=1, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='', blank=True, null=True)

    class Meta:
        db_table = 'Colaboradores'

    def __str__(self):
        return self.nome_colaborador or "Colaborador sem nome"

    def save(self, *args, **kwargs):
        if self.cpf:  # só tenta limpar se houver valor
            self.cpf = ''.join(filter(str.isdigit, self.cpf))
        super().save(*args, **kwargs)

    def format_cpf(self):
        """Retorna o CPF formatado: 000.000.000-00"""
        if self.cpf and len(self.cpf) == 11:
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

    def format_data_nasc(self):
        if not self.data_nasc:
            return ''
    
        data_str = str(self.data_nasc).strip()

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

class Epis(models.Model):
    id_epis = models.AutoField(primary_key=True)
    nome_epi = models.CharField(max_length=45, blank=True, null=True)
    tipo_acessorio = models.CharField(max_length=45, blank=True, null=True)
    fabricante = models.CharField(max_length=45, blank=True, null=True)
    data_validade = models.CharField(max_length=45, blank=True, null=True)
    tamanho = models.CharField(max_length=45, blank=True, null=True)
    qtd_estoque = models.IntegerField(default=0, blank=True, null=True)
    delete_flag  = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'Epis'

    def __str__(self):
        return self.nome_epi

class Emprestimos(models.Model):
    colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    epis = models.ForeignKey(Epis, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(blank=True, null=True)
    data_prevista = models.DateTimeField(blank=True, null=True)
    data_devolver = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    delete_flag  = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'Emprestimos'
        constraints = [
            models.UniqueConstraint(fields=['colaborador', 'epis'], name='unique_colaborador_epis')
        ]

    def __str__(self):
        return f"{self.colaborador.nome_colaborador} - {self.epis.nome_epi}"

class Estoque(models.Model):
    epis = models.OneToOneField(Epis, on_delete=models.CASCADE, primary_key=True)
    quantidade_disponivel = models.IntegerField(blank=True, null=True)
    delete_flag  = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'Estoque'

    def __str__(self):
        return f"{self.epis.nome_epi} - {self.quantidade_disponivel}"

class Setor(models.Model):
    id_setor = models.AutoField(primary_key=True)
    nome_setor = models.CharField(max_length=45, blank=True, null=True)
    epis_necessario = models.CharField(max_length=45, blank=True, null=True)
    delete_flag = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'Setor'

    def __str__(self):
        return self.nome_setor
