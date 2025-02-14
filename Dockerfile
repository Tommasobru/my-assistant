FROM python:3.12

WORKDIR /app

# copia il file requirements nel container 
COPY requirements.txt .

# installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variable for the port


# Comando per avviare Chainlit
CMD ["sh", "-c", "chainlit run app.py"]