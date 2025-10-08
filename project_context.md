# Contexto do Projeto - Inova

## Visão Geral
Projeto Django para gestão de startups e notícias da área de inovação. O sistema permite cadastrar startups com informações detalhadas sobre equipe, contato e redes sociais, além de gerenciar notícias categorizadas.

## Estrutura Atual

### Modelos de Dados
- **Startup**: Modelo principal com informações básicas da startup
- **MembroEquipe**: Membros da equipe de cada startup (relacionamento ForeignKey)
- **RedesSociais**: Links das redes sociais (relacionamento OneToOne)
- **Contato**: Informações de contato (relacionamento OneToOne)
- **Noticia**: Sistema de notícias com categorias (STARTUP, INOVACAO, EVENTO)
- **LinkFormulario**: [NOVO] Links de formulários com controle de data de atualização

### Interface de Administração
- StartupAdmin: Configurado com inlines para edição de modelos relacionados
- NoticiaAdmin: Interface completa com filtros e busca
- LinkFormularioAdmin: [NOVO] Interface para gerenciar links de formulários

## Mudanças Recentes

### 2024 - Adição do Modelo LinkFormulario
**Data**: Implementado hoje
**Descrição**: Criado novo modelo para gerenciar links de formulários no painel administrativo.

**Detalhes da Implementação**:
- Modelo `LinkFormulario` criado em `inova/models.py`
- Campos: `link` (URLField) e `data` (DateTimeField com auto_now=True)
- Configurado no admin como `LinkFormularioAdmin`
- Migração `0005_linkformulario` aplicada com sucesso
- Interface administrativa com campos readonly para data
- Navegação hierárquica por data disponível

**Funcionalidades**:
- Cadastro de links de formulários
- Atualização automática de data quando o link é modificado
- Busca por link
- Ordenação por data (mais recente primeiro)
- Interface amigável no painel administrativo

## Próximos Passos Sugeridos
1. Testar a funcionalidade no painel administrativo
2. Considerar adicionar validações específicas para URLs
3. Implementar funcionalidade para acessar os links do frontend
4. Documentar uso para outros desenvolvedores

## Tecnologias
- Django Framework
- SQLite (desenvolvimento)
- Python

## Estrutura de Arquivos
- `app/`: Configurações principais do Django
- `inova/`: Aplicação principal com modelos, views e admin
- `templates/`: Templates HTML
- `static/`: Arquivos estáticos (CSS, JS, imagens)
- `media/`: Uploads de usuários (logos, fotos, etc.)
