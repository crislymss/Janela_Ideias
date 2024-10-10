# Use uma imagem base do Python
FROM python:3.12-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instale o Poetry
RUN pip install poetry

# Copie os arquivos do projeto para o container
COPY . .

RUN apt-get update && apt-get install -y libpq-dev

RUN apt-get update && apt-get install -y gcc

# Instale as dependências de compilação
RUN apt-get update && apt-get install -y gcc libpq-dev

# Instale as dependências do projeto
RUN poetry install

# Comando para iniciar a aplicação (ajuste conforme necessário)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8001"]
