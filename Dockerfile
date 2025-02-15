FROM python:3.12

WORKDIR /app

# copia il file requirements nel container 
COPY requirements.txt .

# installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variable for the port
EXPOSE 8000

# Imposta la porta di Chainlit con una variabile d'ambiente
ENV CHAINLIT_SERVER_HOST=0.0.0.0
ENV CHAINLIT_SERVER_PORT=8000


# Comando per avviare Chainlit
CMD ["chainlit", "run", "app.py"]