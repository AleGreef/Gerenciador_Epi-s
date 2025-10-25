from django.db import models

class Setor(models.Model):
    id_setor = models.AutoField(primary_key=True)
    nome_setor = models.CharField(max_length=45, blank=True, null=True)
    epis_necessario = models.CharField(max_length=45, blank=True, null=True)
    delete = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'setor'

    def __str__(self):
        return self.nome_setor


class Colaboradores(models.Model):
    id_col = models.AutoField(primary_key=True)
    nome_Colaborador = models.CharField(max_length=45, blank=True, null=True)
    Data_nasc = models.CharField(max_length=12, blank=True, null=True)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=45, blank=True, null=True)
    senha = models.CharField(max_length=45, blank=True, null=True)
    cpf = models.CharField(unique=True, max_length=11, blank=True, null=True)
  
    class Meta:
        db_table = 'colaboradores'

    def __str__(self):
        return self.nome_colaborador


class Epis(models.Model):
    id_epis = models.AutoField(primary_key=True)
    nome_epi = models.CharField(max_length=45, blank=True, null=True)
    tipo_acessorio = models.CharField(max_length=45, blank=True, null=True)
    fabricante = models.CharField(max_length=45, blank=True, null=True)
    tamanho = models.CharField(max_length=45, blank=True, null=True)
    delete = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'epis'

    def __str__(self):
        return self.nome_epi


class Estoque(models.Model):
    epis = models.OneToOneField(Epis, on_delete=models.CASCADE, primary_key=True)
    quantidade_disponivel = models.IntegerField(blank=True, null=True)
    delete = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'estoque'

    def __str__(self):
        return f"{self.epis.nome_epi} - {self.quantidade_disponivel}"


class Emprestimos(models.Model):
    colaborador = models.ForeignKey(Colaboradores, on_delete=models.CASCADE)
    epis = models.ForeignKey(Epis, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(blank=True, null=True)
    data_devolucao = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    delete = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'emprestimos'
        constraints = [
            models.UniqueConstraint(fields=['colaborador', 'epis'], name='unique_colaborador_epis')
        ]

    def __str__(self):
        return f"{self.colaborador.nome_colaborador} - {self.epis.nome_epi}"
