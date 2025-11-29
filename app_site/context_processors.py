from app_site.models import Colaboradores

def colaborador_logado_processor(request):
    if request.user.is_authenticated:
        colaborador = Colaboradores.objects.filter(user=request.user).first()
        return {'colaborador_logado': colaborador}
    return {}

def nome_colaborador(request):
    if request.user.is_authenticated:
        try:
            colaborador = Colaboradores.objects.get(user=request.user)
            nome = colaborador.nome_colaborador
        except Colaboradores.DoesNotExist:
            nome = request.user.first_name or request.user.email
    else:
        nome = ''
    return {'nome_colaborador': nome}
