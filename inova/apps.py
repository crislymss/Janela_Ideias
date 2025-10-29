
"""
Configuração do aplicativo 'inova' do Django.

Este arquivo define a classe de configuração para o aplicativo 'inova',
permitindo a personalização de metadados como o nome de exibição
na área administrativa.
"""

from django.apps import AppConfig


class InovaConfig(AppConfig):
    
    """
    Classe de configuração específica para o aplicativo 'inova'.

    Esta classe herda de AppConfig e permite definir atributos específicos
    do aplicativo.

    Atributos:
        default_auto_field (str): Define o tipo de campo padrão para chaves primárias
            geradas automaticamente.
        name (str): O nome do aplicativo ('inova').
        verbose_name (str): Um nome legível por humanos para o aplicativo, que
            será exibido na interface de administração do Django.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inova' 
    verbose_name = 'Gestão e Controle'