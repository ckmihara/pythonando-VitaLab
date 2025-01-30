from django.contrib import admin
from .models import TiposExames
from .models import SolicitacaoExame
from .models import PedidosExames
from .models import AcessoMedico

admin.site.register(TiposExames)
admin.site.register(SolicitacaoExame)
admin.site.register(PedidosExames)
admin.site.register(AcessoMedico)