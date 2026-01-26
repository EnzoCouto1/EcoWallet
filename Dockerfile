FROM python:3.12-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Impede o Python de criar arquivos .pyc e bufferizar logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=100

COPY . .

# rodar o app (Libera a porta 8000)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]