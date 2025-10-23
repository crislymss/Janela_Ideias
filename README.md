#  🪟 Janela de Ideias

A Janela de Ideias é uma iniciativa da Pró-Reitoria de Pesquisa e Inovação da Universidade Federal do Piauí (PROPESQI-UFPI) que visa fortalecer o potencial empreendedor e inovador dentro da universidade. O projeto é uma vitrine das startups que tiveram o seu desenvolvimento iniciado ou fomentado pela UFPI, uma forma de divulgar e incentivar a participação da comunidade acadêmica como um todo.

## Figma

https://www.figma.com/design/LLUXkJv395RlFNxQn9xk9r/Janela-de-Ideias?node-id=4-6&t=blcrqw2MCn4UhOLp-1

---

## Iniciando o Projeto

### 1. Pré-requisitos

Certifique-se de ter instalado:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

### 2. Ativar o ambiente virtual (opcional)

Se estiver usando o ambiente virtual do Python, ative-o:

```bash
source venv/bin/activate
````

---

### 3. Subir os contêineres

Para construir e iniciar os serviços do projeto, execute:

```bash
sudo docker compose -p janela_nova up -d
```

🔹 O parâmetro `-d` faz o Docker rodar em **modo desacoplado** (background).
🔹 O parâmetro `-p janela_nova` define o nome do projeto Docker.

---

### 4. Aplicar migrações do banco de dados

```bash
sudo docker compose -p janela_nova exec web python manage.py migrate
```

---

### 5. Coletar arquivos estáticos

```bash
sudo docker compose -p janela_nova exec web python manage.py collectstatic --noinput
```

---

### 6. Criar superusuário (opcional)

```bash
sudo docker compose -p janela_nova exec web python manage.py createsuperuser
```

---

### 7. Acessar no navegador

Abra no navegador:

👉 [http://localhost:8002](http://localhost:8002)

Painel admin (após criar superusuário):

👉 [http://localhost:8002/admin](http://localhost:8002/admin)

---

## 🧩 Comandos úteis

### Ver logs em tempo real

```bash
sudo docker compose -p janela_nova logs -f web
```

### Ver status dos contêineres

```bash
sudo docker ps
```

---

## ⏸️ Pausar ou parar o projeto

### Parar os contêineres

```bash
sudo docker compose -p janela_nova down
```

> Isso encerra os serviços e remove os contêineres, mas **mantém os volumes** (dados do banco).

---

### Pausar temporariamente (sem remover contêineres)

```bash
sudo docker compose -p janela_nova stop
```

> Use este comando quando quiser **interromper temporariamente** os serviços e retomá-los depois.

---

### Retomar contêineres parados

```bash
sudo docker compose -p janela_nova start
```

---

## 🧹 Limpeza completa (opcional)

Se quiser remover tudo, incluindo volumes e cache:

```bash
sudo docker compose -p janela_nova down -v
```

> ⚠️ Isso apaga o banco de dados e todos os dados persistidos.

---

## 🧠 Dica

Se precisar acessar o shell interativo do Django dentro do container:

```bash
sudo docker compose -p janela_nova exec web python manage.py shell
```

